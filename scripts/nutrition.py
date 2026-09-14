#!/usr/bin/env python3
"""
Oppidu Recipes — offline nutrition estimate.

Sums each ingredient's macros (calories, fat, carbs, protein) scaled by its
quantity, then divides by servings. Nothing here is stored on a recipe
record — it's cheap to recompute from `ingredients`, so both this CLI and
the wizard's live JS estimate (see NUTRITION_DATA / estimateRecipeNutrition
in preview_template.html, a hand-kept mirror of this file, the same
relationship ingredients_db.py's suggest_quantity() has with its JS twin)
derive it fresh every time rather than risk it going stale.

This is explicitly an ESTIMATE:
  - NUTRITION_PER_100G (nutrition_data.py) is hand-curated from commonly
    cited average figures, not a lab analysis.
  - "piece"-unit ingredients use an average weight per piece (PIECE_GRAMS),
    which varies in reality (a large vs. small onion).
  - An ingredient measured "to taste", or missing from NUTRITION_PER_100G
    entirely, is silently excluded rather than guessed at — the returned
    `ingredients_covered` / `ingredients_total` tells the caller how much
    of the recipe the estimate actually accounts for, so a low-coverage
    estimate can be shown as rougher than a high-coverage one.

CLI usage:
    python3 scripts/nutrition.py aloo-gobi
    python3 scripts/nutrition.py butter-chicken
"""
import sys

import ingredients_db
from nutrition_data import NUTRITION_PER_100G, PIECE_GRAMS, PIECE_GRAMS_DEFAULT, UNIT_TO_GRAMS

MACROS = ("kcal", "fat_g", "carbs_g", "protein_g")


def grams_for(ingredient):
    """Best-effort conversion of one ingredient's quantity+unit to grams.
    Returns None for a unit with no sensible gram equivalent ("to taste"
    or anything else not in UNIT_TO_GRAMS) — the caller excludes it.
    """
    unit = ingredient["unit"].strip().lower()
    qty = ingredient["quantity"]
    if unit == "piece":
        base = ingredients_db.base_name(ingredient["name"])
        return qty * PIECE_GRAMS.get(base, PIECE_GRAMS_DEFAULT)
    grams_per_unit = UNIT_TO_GRAMS.get(unit)
    if grams_per_unit is None:
        return None
    return qty * grams_per_unit


def estimate_recipe_nutrition(recipe):
    """Returns {per_serving, total, ingredients_covered, ingredients_total}.
    per_serving/total are {kcal, fat_g, carbs_g, protein_g} dicts, rounded
    to one decimal place.
    """
    servings = recipe.get("servings") or 1
    totals = {m: 0.0 for m in MACROS}
    covered = 0

    for ing in recipe["ingredients"]:
        base = ingredients_db.base_name(ing["name"])
        profile = NUTRITION_PER_100G.get(base)
        grams = grams_for(ing)
        if profile is None or grams is None:
            continue
        covered += 1
        factor = grams / 100.0
        for m in MACROS:
            totals[m] += profile[m] * factor

    return {
        "total": {m: round(v, 1) for m, v in totals.items()},
        "per_serving": {m: round(v / servings, 1) for m, v in totals.items()},
        "ingredients_covered": covered,
        "ingredients_total": len(recipe["ingredients"]),
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/nutrition.py <recipe-id>", file=sys.stderr)
        sys.exit(1)

    import search  # local import: avoids a circular/unused import when this module is used as a library
    recipe = search.load_recipe(sys.argv[1])
    if not recipe:
        print(f"No recipe found with id '{sys.argv[1]}'", file=sys.stderr)
        sys.exit(1)

    result = estimate_recipe_nutrition(recipe)
    ps = result["per_serving"]
    print(f"{recipe['title']} — estimated nutrition per serving ({recipe['servings']} servings total):")
    print(f"  {ps['kcal']:.0f} kcal   {ps['fat_g']:.1f} g fat   {ps['carbs_g']:.1f} g carbs   {ps['protein_g']:.1f} g protein")
    print(f"  based on {result['ingredients_covered']}/{result['ingredients_total']} ingredients "
          f"({'full coverage' if result['ingredients_covered'] == result['ingredients_total'] else 'partial — some ingredients had no nutrition data'})")


if __name__ == "__main__":
    main()
