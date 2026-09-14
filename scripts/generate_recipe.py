#!/usr/bin/env python3
"""
Oppidu Recipes — on-demand recipe generation.

Generates a new recipe conforming to schema/recipe.schema.json and saves
it into data/recipes/ (updating data/index.json). This is the piece that
lets the database grow over time instead of staying fixed at the seed set.

Two modes:

1. --llm  (needs `pip install anthropic` and an ANTHROPIC_API_KEY env var)
   Calls the Claude API with a prompt that forces structured JSON output
   matching the schema, validates the result, and saves it.

2. --from-file <path.json>
   Takes a recipe you already have as JSON (e.g. one you asked Claude to
   write in chat and saved locally) and slots it into the database after
   validating it against the schema. This is the practical path inside a
   Cowork session, since a live Anthropic API key usually isn't available
   in the workspace itself.

Usage:
    python3 scripts/generate_recipe.py --llm "a quick vegan weeknight lentil soup"
    python3 scripts/generate_recipe.py --from-file my_new_recipe.json
"""
import argparse
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(BASE_DIR, "schema", "recipe.schema.json")
RECIPES_DIR = os.path.join(BASE_DIR, "data", "recipes")
INDEX_PATH = os.path.join(BASE_DIR, "data", "index.json")

GENERATION_SYSTEM_PROMPT = """You generate a single recipe as strict JSON conforming exactly to this \
JSON Schema. Output ONLY the JSON object, no prose, no markdown fences.

{schema}
"""


def _load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_recipe(recipe):
    import jsonschema
    schema = _load_schema()
    jsonschema.validate(instance=recipe, schema=schema)


def save_recipe(recipe):
    os.makedirs(RECIPES_DIR, exist_ok=True)
    path = os.path.join(RECIPES_DIR, f"{recipe['id']}.json")
    if os.path.exists(path):
        raise FileExistsError(f"Recipe id '{recipe['id']}' already exists at {path}. "
                               f"Choose a different id or delete the existing file first.")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(recipe, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Update the index.
    index = []
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            index = json.load(f)
    index.append({
        "id": recipe["id"],
        "title": recipe["title"],
        "cuisine": recipe["cuisine"],
        "category": recipe["category"],
        "tags": recipe.get("tags", []),
        "dietary": recipe.get("dietary", []),
        "ingredient_names": [i["name"] for i in recipe["ingredients"]],
    })
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return path


def generate_via_llm(prompt_text):
    try:
        import anthropic
    except ImportError:
        print("The 'anthropic' package isn't installed. Run:\n"
              "    pip install anthropic --break-system-packages\n"
              "and set ANTHROPIC_API_KEY, then retry.", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY is not set. Export it and retry:\n"
              "    export ANTHROPIC_API_KEY=sk-ant-...", file=sys.stderr)
        sys.exit(1)

    schema = _load_schema()
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        system=GENERATION_SYSTEM_PROMPT.format(schema=json.dumps(schema)),
        messages=[{"role": "user", "content": f"Generate a recipe for: {prompt_text}"}],
    )
    raw = message.content[0].text.strip()
    recipe = json.loads(raw)
    recipe.setdefault("source", "ai-generated")
    recipe.setdefault("generated_by", "claude-sonnet-4-5")
    return recipe


def main():
    parser = argparse.ArgumentParser(description="Generate or import a new recipe into the database.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--llm", metavar="PROMPT", help="Generate a recipe from a text prompt via the Claude API")
    group.add_argument("--from-file", metavar="PATH", help="Import an already-written recipe JSON file")
    args = parser.parse_args()

    if args.llm:
        recipe = generate_via_llm(args.llm)
    else:
        with open(args.from_file, "r", encoding="utf-8") as f:
            recipe = json.load(f)

    validate_recipe(recipe)
    path = save_recipe(recipe)
    print(f"Saved and indexed: {path}")


if __name__ == "__main__":
    main()
