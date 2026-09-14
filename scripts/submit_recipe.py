#!/usr/bin/env python3
"""
Oppidu Recipes — user recipe submission workflow.

Implements the intake flow as a small, testable state machine:

    start_submission(title, servings)          # servings asked first
      -> add_ingredient(draft, name, quantity=None, unit=None)
           # autocomplete_ingredient() + suggest_quantity() help fill this in
      -> add_step(draft, text)                  # free text, or from STEP_TEMPLATES
      -> finalize(draft)                        # validates against the schema

No user-account system exists yet (by design — see README), so every draft
carries `submitted_by: None` and comes out with `status: "submitted"` rather
than `"published"`; promoting it is a future editorial/account step.

No image-generation pipeline exists yet either. finalize() still records
*which* shots the submission would need — an ingredients mise-en-place
photo, a photo for any step flagged "key" (roasting, searing, ...), and a
final plated shot — as plain TODO markers in `photos_needed`, with no
attempt to generate or fake them.
"""
import json
import os
import re

import jsonschema

import ingredients_db

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(BASE_DIR, "schema", "recipe.schema.json")

# Where a finalized submission is persisted locally — deliberately separate
# from the curated data/recipes/ seed set, the same way the browser wizard
# (preview_template.html's RecipeStore) keeps locally-saved submissions
# apart from the seed RECIPES array. See finalize()/save_submission() below
# and the README's "Local persistence today, Supabase later" section.
SUBMISSIONS_DIR = os.path.join(BASE_DIR, "data", "submissions")

# Quick-insert phrases for the "how do I phrase this step" problem, grouped
# the way a cook thinks about them. The submission UI offers these as
# one-click inserts; the user can always type their own text instead.
STEP_TEMPLATES = {
    "knife-work": [
        "Finely chop the {ingredient}.",
        "Dice the {ingredient} into even cubes.",
        "Julienne the {ingredient} into thin strips.",
        "Mince the {ingredient}.",
        "Thinly slice the {ingredient}.",
    ],
    "heat": [
        "Dry-roast the {ingredient} until fragrant, 1-2 minutes.",
        "Temper the {ingredient} in hot oil until it crackles.",
        "Saute the {ingredient} until golden.",
        "Sear the {ingredient} on high heat until browned on all sides.",
        "Simmer gently, stirring occasionally.",
        "Bring to a boil, then reduce to a simmer.",
    ],
    "assembly": [
        "Fold in gently to combine.",
        "Let rest for 10 minutes before serving.",
        "Garnish with {ingredient}.",
        "Adjust seasoning to taste.",
        "Transfer to a serving dish.",
    ],
}

# A step whose text contains one of these verbs gets flagged as a "key step"
# worth its own photo — this is a plain keyword check, not an LLM call.
KEY_STEP_KEYWORDS = [
    "roast", "sear", "fry", "grill", "temper", "caramelize", "caramelise",
    "bake", "flambe", "char", "toast", "brown",
]


def autocomplete_ingredient(prefix, limit=8):
    """Thin pass-through to the ingredient reference DB — kept here so the
    submission module is the one public surface the UI/CLI talks to."""
    return ingredients_db.autocomplete(prefix, limit=limit)


def suggest_quantity(name, servings):
    return ingredients_db.suggest_quantity(name, servings)


def start_submission(title, servings, cuisine="", category="main", description="", kitchen_name=""):
    """Servings is asked for first in the actual UI flow; it's a required
    argument here for the same reason — everything else scales off it.

    `kitchen_name` is the optional "Nina's Kitchen"-style label a submitter
    organizes their own recipes under (see schema's submitted_kitchen) —
    independent of accounts, which don't exist yet. Left out of the draft
    entirely when blank, matching how add_ingredient() omits `notes`/
    `optional` rather than writing empty placeholders.
    """
    if servings < 1:
        raise ValueError("servings must be at least 1")
    draft = {
        "id": _slugify(title) if title else "",
        "title": title,
        "description": description,
        "cuisine": cuisine,
        "category": category,
        "servings": servings,
        "prep_time_minutes": 0,
        "cook_time_minutes": 0,
        "difficulty": "medium",
        "ingredients": [],
        "instructions": [],
        "tags": [],
        "dietary": [],
        "source": "user-submitted",
        "status": "draft",
        "submitted_by": None,  # no account system yet
        "photos_needed": [],
    }
    if kitchen_name.strip():
        draft["submitted_kitchen"] = kitchen_name.strip()
    return draft


def add_ingredient(draft, name, quantity=None, unit=None, notes=None, optional=False):
    """If quantity/unit are omitted, suggest_quantity() fills them in from
    the reference database, scaled to draft['servings']. The caller (UI or
    test) can always override what comes back."""
    if quantity is None or unit is None:
        sugg_qty, sugg_unit = suggest_quantity(name, draft["servings"])
        quantity = quantity if quantity is not None else (sugg_qty if sugg_qty is not None else 0)
        unit = unit or sugg_unit or "piece"

    base = ingredients_db.base_name(name)
    reference = next((e for e in ingredients_db.load() if e["name"] == base), None)
    category = reference["grocery_category"] if reference else "other"

    ingredient = {
        "name": name,
        "quantity": quantity,
        "unit": unit,
        "grocery_category": category,
    }
    if notes:
        ingredient["notes"] = notes
    if optional:
        ingredient["optional"] = True

    draft["ingredients"].append(ingredient)
    return ingredient


def add_step(draft, text, key_step=None):
    """Appends an instruction. `key_step` auto-detects from KEY_STEP_KEYWORDS
    when left as None; pass True/False to override the auto-detection."""
    draft["instructions"].append(text)
    step_index = len(draft["instructions"])  # 1-indexed, matches schema note

    is_key = key_step if key_step is not None else _looks_like_key_step(text)
    if is_key:
        marker = f"step-{step_index}"
        if marker not in draft["photos_needed"]:
            draft["photos_needed"].append(marker)
    return step_index, is_key


def mark_ingredients_photo_needed(draft):
    if "ingredients" not in draft["photos_needed"]:
        draft["photos_needed"].insert(0, "ingredients")


def mark_final_photo_needed(draft):
    if "final" not in draft["photos_needed"]:
        draft["photos_needed"].append("final")


def finalize(draft):
    """Locks in id/status and validates against the schema. Raises
    jsonschema.ValidationError if the draft is incomplete."""
    if not draft["id"]:
        draft["id"] = _slugify(draft["title"])
    draft["status"] = "submitted"

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    jsonschema.validate(instance=draft, schema=schema)
    return draft


def save_submission(finalized):
    """Persist a finalized submission locally as its own file under
    data/submissions/<id>.json, so a recipe created through this workflow
    doesn't vanish once the process exits — the same "local now, a real
    database later" pattern the browser wizard uses (RecipeStore in
    preview_template.html). This is a plain, swappable write: replace the
    body with a Supabase upsert later and callers don't need to change.
    Does NOT run automatically inside finalize() — call it explicitly once
    you're happy with the draft, same as the "Save recipe" button in the
    browser wizard.
    """
    os.makedirs(SUBMISSIONS_DIR, exist_ok=True)
    path = os.path.join(SUBMISSIONS_DIR, f"{finalized['id']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(finalized, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return path


def list_submissions():
    """All locally-saved submissions (data/submissions/*.json), sorted by
    id. Empty list if nothing has been saved yet or the directory doesn't
    exist."""
    if not os.path.isdir(SUBMISSIONS_DIR):
        return []
    out = []
    for filename in sorted(os.listdir(SUBMISSIONS_DIR)):
        if not filename.endswith(".json"):
            continue
        with open(os.path.join(SUBMISSIONS_DIR, filename), "r", encoding="utf-8") as f:
            out.append(json.load(f))
    return out


def _looks_like_key_step(text):
    lowered = text.lower()
    return any(re.search(rf"\b{kw}\w*", lowered) for kw in KEY_STEP_KEYWORDS)


def _slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "untitled-recipe"


def _demo():
    """Deterministic walkthrough proving the pieces fit together end to end."""
    draft = start_submission(
        title="Weeknight Lemon Garlic Chicken",
        servings=4,
        cuisine="American",
        category="main",
        description="A fast, punchy pan-seared chicken with a lemon-garlic pan sauce.",
    )

    print("Autocomplete 'chick':", [e["name"] for e in autocomplete_ingredient("chick")])

    add_ingredient(draft, "chicken breast")  # quantity/unit auto-suggested
    add_ingredient(draft, "garlic")
    add_ingredient(draft, "lemon juice")
    add_ingredient(draft, "olive oil")
    add_ingredient(draft, "fresh thyme", quantity=2, unit="tsp", notes="not in reference DB yet, entered manually")

    mark_ingredients_photo_needed(draft)
    add_step(draft, "Season the chicken breast on both sides.")
    add_step(draft, "Sear the chicken in olive oil until golden and cooked through.")  # auto key step
    add_step(draft, "Add garlic and saute until fragrant.")  # auto key step
    add_step(draft, "Deglaze with lemon juice, scraping up the browned bits.")
    add_step(draft, "Fold in gently to combine, then transfer to a serving dish.")
    mark_final_photo_needed(draft)

    draft["dietary"] = ["gluten-free", "dairy-free"]
    draft["tags"] = ["weeknight", "quick", "pan-sauce"]
    draft["prep_time_minutes"] = 10
    draft["cook_time_minutes"] = 15

    finalized = finalize(draft)
    print(json.dumps(finalized, indent=2))
    print("\nphotos_needed:", finalized["photos_needed"], "  <- TODO, no generation pipeline yet")

    path = save_submission(finalized)
    print(f"\nSaved locally -> {path}  (see data/submissions/ — not the curated seed set)")


if __name__ == "__main__":
    _demo()
