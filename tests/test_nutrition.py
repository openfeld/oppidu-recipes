#!/usr/bin/env python3
"""
Sanity tests for scripts/nutrition.py. Runs standalone (python3 tests/test_nutrition.py)
or via pytest.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

import nutrition  # noqa: E402
import search  # noqa: E402


def _recipe(ingredients, servings=1):
    return {"servings": servings, "ingredients": ingredients}


def test_grams_for_converts_common_units():
    assert nutrition.grams_for({"name": "sugar", "quantity": 2, "unit": "tbsp"}) == 30.0
    assert nutrition.grams_for({"name": "water", "quantity": 1, "unit": "l"}) == 1000.0
    assert nutrition.grams_for({"name": "butter", "quantity": 250, "unit": "g"}) == 250.0


def test_grams_for_piece_uses_curated_average_weight():
    assert nutrition.grams_for({"name": "onion", "quantity": 2, "unit": "piece"}) == 220.0


def test_grams_for_piece_falls_back_to_default_weight():
    grams = nutrition.grams_for({"name": "some unlisted piece-measured thing", "quantity": 1, "unit": "piece"})
    assert grams == nutrition.PIECE_GRAMS_DEFAULT


def test_grams_for_unconvertible_unit_returns_none():
    assert nutrition.grams_for({"name": "salt", "quantity": 1, "unit": "to taste"}) is None


def test_estimate_scales_by_servings():
    recipe = _recipe([{"name": "sugar", "quantity": 100, "unit": "g", "grocery_category": "other"}], servings=2)
    result = nutrition.estimate_recipe_nutrition(recipe)
    assert result["total"]["kcal"] == 387.0
    assert result["per_serving"]["kcal"] == 193.5


def test_estimate_reports_partial_coverage_for_unknown_ingredient():
    recipe = _recipe([
        {"name": "sugar", "quantity": 50, "unit": "g", "grocery_category": "other"},
        {"name": "some completely unknown ingredient", "quantity": 1, "unit": "piece", "grocery_category": "other"},
    ], servings=1)
    result = nutrition.estimate_recipe_nutrition(recipe)
    assert result["ingredients_total"] == 2
    assert result["ingredients_covered"] == 1
    # Only sugar's macros should be counted — the unknown ingredient contributes nothing.
    assert result["total"]["kcal"] == round(50 * 387.0 / 100, 1)


def test_estimate_excludes_to_taste_ingredients():
    recipe = _recipe([
        {"name": "salt", "quantity": 1, "unit": "to taste", "grocery_category": "spices"},
    ], servings=1)
    result = nutrition.estimate_recipe_nutrition(recipe)
    assert result["ingredients_covered"] == 0
    assert result["total"]["kcal"] == 0.0


def test_seed_recipes_have_full_or_near_full_nutrition_coverage():
    """Every seed recipe should resolve nutrition data for all of its
    ingredients — a coverage gap here means nutrition_data.py is missing
    an entry that ingredients_db.py's base_name() would otherwise resolve."""
    for filename in sorted(os.listdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "recipes"))):
        if not filename.endswith(".json"):
            continue
        recipe_id = filename[:-5]
        recipe = search.load_recipe(recipe_id)
        result = nutrition.estimate_recipe_nutrition(recipe)
        assert result["ingredients_covered"] == result["ingredients_total"], (
            f"{recipe_id}: only {result['ingredients_covered']}/{result['ingredients_total']} "
            f"ingredients had nutrition data"
        )


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
