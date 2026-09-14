#!/usr/bin/env python3
"""
Oppidu Recipes — ingredient reference database.

Aggregates every ingredient occurrence across data/recipes/*.json into a
per-ingredient reference: its usual grocery category, its usual unit, and
a typical quantity-per-serving so a new submission can be auto-suggested
a quantity once the user says how many people it's for.

This is intentionally built FROM the recipe database itself rather than
hand-curated, so it grows automatically as more recipes are added — run
`python3 scripts/ingredients_db.py` again after adding recipes to refresh
data/ingredients.json. A small curated supplement (PANTRY_STAPLES below)
fills in a few very common items that don't scale linearly with servings
(salt, pepper, water) so autocomplete still offers them.

Used by scripts/submit_recipe.py for:
  - autocomplete(prefix): ingredient-name suggestions as the user types
  - suggest_quantity(name, servings): a starting quantity to prefill
Neither is a hard rule — both are just a starting point the user edits.
"""
import json
import os
import re
from collections import defaultdict, Counter

from de_ingredient_names import DE_INGREDIENT_NAMES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPES_DIR = os.path.join(BASE_DIR, "data", "recipes")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "ingredients.json")

# Items that show up in almost every dish but are seasoned "to taste" rather
# than scaled per person — no reliable quantity-per-serving exists for these,
# so they're offered for autocomplete with unit "to taste" and no auto-fill.
PANTRY_STAPLES = [
    {"name": "salt", "grocery_category": "spices"},
    {"name": "black pepper", "grocery_category": "spices"},
    {"name": "water", "grocery_category": "beverages"},
]


def base_name(raw_name):
    """'onion, finely chopped' -> 'onion'; 'gochujang (Korean chili paste)' -> 'gochujang'.

    Public — scripts/submit_recipe.py reuses this to look up an ingredient
    the user typed against this reference database.
    """
    name = re.sub(r"\([^)]*\)", "", raw_name)  # drop parenthetical
    name = name.split(",")[0]
    return name.strip().lower()


# Old name kept as an alias in case anything still imports it privately.
_base_name = base_name


def build():
    # (base_name, unit) -> list of (quantity / servings)
    per_serving = defaultdict(list)
    categories = defaultdict(Counter)
    units = defaultdict(Counter)
    example_names = defaultdict(Counter)

    for filename in sorted(os.listdir(RECIPES_DIR)):
        if not filename.endswith(".json"):
            continue
        with open(os.path.join(RECIPES_DIR, filename), "r", encoding="utf-8") as f:
            recipe = json.load(f)

        servings = recipe.get("servings") or 1
        for ing in recipe["ingredients"]:
            base = base_name(ing["name"])
            if not base:
                continue
            units[base][ing["unit"]] += 1
            categories[base][ing["grocery_category"]] += 1
            example_names[base][ing["name"]] += 1
            per_serving[(base, ing["unit"])].append(ing["quantity"] / servings)

    entries = {}
    for base in units:
        best_unit, _ = units[base].most_common(1)[0]
        best_category, _ = categories[base].most_common(1)[0]
        best_example, _ = example_names[base].most_common(1)[0]
        samples = per_serving[(base, best_unit)]
        avg_qty = round(sum(samples) / len(samples), 3) if samples else None

        entries[base] = {
            "name": base,
            "example_name": best_example,
            "name_de": DE_INGREDIENT_NAMES.get(base),
            "grocery_category": best_category,
            "default_unit": best_unit,
            "qty_per_serving": avg_qty,
            "sample_count": len(samples),
        }

    for staple in PANTRY_STAPLES:
        if staple["name"] not in entries:
            entries[staple["name"]] = {
                "name": staple["name"],
                "example_name": staple["name"],
                "name_de": DE_INGREDIENT_NAMES.get(staple["name"]),
                "grocery_category": staple["grocery_category"],
                "default_unit": "to taste",
                "qty_per_serving": None,
                "sample_count": 0,
            }

    ordered = [entries[k] for k in sorted(entries)]

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(ordered, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return ordered


_CACHE = None


def load():
    global _CACHE
    if _CACHE is None:
        if not os.path.exists(OUTPUT_PATH):
            build()
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            _CACHE = json.load(f)
    return _CACHE


def autocomplete(prefix, limit=8):
    """Ingredient-name suggestions for the given (possibly partial) prefix."""
    prefix = prefix.strip().lower()
    if not prefix:
        return []
    starts = [e for e in load() if e["name"].startswith(prefix)]
    contains = [e for e in load() if prefix in e["name"] and not e["name"].startswith(prefix)]
    return (starts + contains)[:limit]


def suggest_quantity(name, servings):
    """Return (quantity, unit) suggested for `name` scaled to `servings`, or
    (None, None) if this ingredient isn't in the reference database yet —
    the caller should fall back to asking the user for a quantity directly.
    """
    base = base_name(name)
    entry = next((e for e in load() if e["name"] == base), None)
    if not entry or entry["qty_per_serving"] is None:
        return None, entry["default_unit"] if entry else None
    qty = entry["qty_per_serving"] * servings
    # Round to something a person would actually measure out.
    if entry["default_unit"] in ("g", "ml"):
        qty = round(qty / 5) * 5 or round(qty, 1)
    elif entry["default_unit"] == "piece":
        qty = max(1, round(qty))  # you can't measure out 7.5 cloves of garlic
    else:
        qty = round(qty * 4) / 4  # nearest quarter for tsp/tbsp/cup etc.
    return qty, entry["default_unit"]


if __name__ == "__main__":
    entries = build()
    print(f"Built {len(entries)} ingredient reference entries -> {OUTPUT_PATH}")
    for e in entries[:10]:
        print(f"  {e['name']:<24} {e['qty_per_serving']} {e['default_unit']:<10} ({e['grocery_category']}, n={e['sample_count']})")
    print("  ...")
