#!/usr/bin/env python3
"""
Oppidu Recipes — builds preview.html from preview_template.html.

preview_template.html contains three literal placeholder tokens,
/*__RECIPES_JSON__*/, /*__INGREDIENTS_JSON__*/, and /*__NUTRITION_JSON__*/,
inside its <script> block. This script substitutes real data (every recipe
in data/recipes/, the ingredient reference database, and the nutrition
reference database) in their place and writes the result to preview.html —
the file actually published as the prototype.

Run this any time preview_template.html, data/recipes/*.json,
data/ingredients.json, or scripts/nutrition_data.py changes.
"""
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPES_DIR = os.path.join(BASE_DIR, "data", "recipes")
INGREDIENTS_PATH = os.path.join(BASE_DIR, "data", "ingredients.json")
TEMPLATE_PATH = os.path.join(BASE_DIR, "preview_template.html")
OUTPUT_PATH = os.path.join(BASE_DIR, "preview.html")

sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))
from nutrition_data import NUTRITION_PER_100G, PIECE_GRAMS, PIECE_GRAMS_DEFAULT, UNIT_TO_GRAMS  # noqa: E402


def build():
    recipes = []
    for filename in sorted(os.listdir(RECIPES_DIR)):
        if filename.endswith(".json"):
            with open(os.path.join(RECIPES_DIR, filename), encoding="utf-8") as f:
                recipes.append(json.load(f))

    with open(INGREDIENTS_PATH, encoding="utf-8") as f:
        ingredients = json.load(f)

    # Same shape scripts/nutrition.py reads directly in Python — bundled
    # here for the JS twin (estimateRecipeNutrition() in preview_template.html)
    # to read at render time, so the two never need to be kept in sync by hand
    # beyond editing nutrition_data.py itself.
    nutrition = {
        "per100g": NUTRITION_PER_100G,
        "pieceGrams": PIECE_GRAMS,
        "pieceGramsDefault": PIECE_GRAMS_DEFAULT,
        "unitToGrams": UNIT_TO_GRAMS,
    }

    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = f.read()

    template = template.replace("/*__RECIPES_JSON__*/", json.dumps(recipes))
    template = template.replace("/*__INGREDIENTS_JSON__*/", json.dumps(ingredients))
    template = template.replace("/*__NUTRITION_JSON__*/", json.dumps(nutrition))

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(template)

    return recipes, ingredients, nutrition


if __name__ == "__main__":
    recipes, ingredients, nutrition = build()
    print(f"Wrote {OUTPUT_PATH}: {len(recipes)} recipes, {len(ingredients)} ingredient entries, "
          f"{len(nutrition['per100g'])} nutrition entries")
