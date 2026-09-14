#!/usr/bin/env python3
"""
Oppidu Recipes — builds preview.html (and index.html) from preview_template.html.

preview_template.html contains three literal placeholder tokens,
/*__RECIPES_JSON__*/, /*__INGREDIENTS_JSON__*/, and /*__NUTRITION_JSON__*/,
inside its <script> block. This script substitutes real data (every recipe
in data/recipes/, the ingredient reference database, and the nutrition
reference database) in their place and writes the identical result to both
preview.html (the name referenced throughout this README, and what the
Claude Artifact publish points at) and index.html (the name GitHub Pages
requires at the repo root to serve the site) — two files, same content, so
neither goes stale relative to the other.

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
PAGES_OUTPUT_PATH = os.path.join(BASE_DIR, "index.html")

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

    # index.html is served directly by GitHub Pages with no wrapper at
    # all, unlike preview.html's Claude Artifact publish (which supplies
    # its own <!doctype html>...<head>...<body> skeleton, charset meta
    # included — deliberately NOT added to the template itself, since the
    # Artifact platform wraps the content and asks that the source not
    # include one). Without a leading doctype, a browser loading
    # index.html directly falls back to Quirks Mode — confirmed live in
    # real Firefox via Playwright
    # ("This page is in Quirks Mode" console warning). Quirks Mode's
    # layout differences are real but weren't reproduced causing the
    # reported sign-in bug specifically in that same session; fixing it
    # removes a genuine source of cross-browser inconsistency regardless.
    with open(PAGES_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write('<!DOCTYPE html>\n<meta charset="utf-8">\n' + template)

    return recipes, ingredients, nutrition


if __name__ == "__main__":
    recipes, ingredients, nutrition = build()
    print(f"Wrote {OUTPUT_PATH} and {PAGES_OUTPUT_PATH}: {len(recipes)} recipes, "
          f"{len(ingredients)} ingredient entries, {len(nutrition['per100g'])} nutrition entries")
