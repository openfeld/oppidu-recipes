#!/usr/bin/env python3
"""
Validate every recipe in data/recipes/ against schema/recipe.schema.json,
and sanity-check that data/index.json is in sync with the recipe files.

Usage:
    python3 scripts/validate.py
Exit code 0 if everything is valid, 1 otherwise.
"""
import json
import os
import sys

import jsonschema

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(BASE_DIR, "schema", "recipe.schema.json")
RECIPES_DIR = os.path.join(BASE_DIR, "data", "recipes")
INDEX_PATH = os.path.join(BASE_DIR, "data", "index.json")


def main():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    errors = []
    recipe_ids = set()

    filenames = sorted(f for f in os.listdir(RECIPES_DIR) if f.endswith(".json"))
    for filename in filenames:
        path = os.path.join(RECIPES_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            recipe = json.load(f)

        try:
            jsonschema.validate(instance=recipe, schema=schema)
        except jsonschema.ValidationError as e:
            errors.append(f"{filename}: {e.message} (at {'/'.join(str(p) for p in e.path)})")
            continue

        expected_id = filename[:-5]
        if recipe["id"] != expected_id:
            errors.append(f"{filename}: id field '{recipe['id']}' doesn't match filename")

        recipe_ids.add(recipe["id"])

    # Check index sync.
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            index = json.load(f)
        index_ids = {e["id"] for e in index}
        missing_from_index = recipe_ids - index_ids
        stale_in_index = index_ids - recipe_ids
        if missing_from_index:
            errors.append(f"index.json is missing: {sorted(missing_from_index)}")
        if stale_in_index:
            errors.append(f"index.json has stale entries not in data/recipes/: {sorted(stale_in_index)}")
    else:
        errors.append("data/index.json does not exist")

    print(f"Checked {len(filenames)} recipe files.")
    if errors:
        print(f"\n{len(errors)} problem(s) found:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("All recipes valid, index in sync.")
    sys.exit(0)


if __name__ == "__main__":
    main()
