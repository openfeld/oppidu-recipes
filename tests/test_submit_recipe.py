#!/usr/bin/env python3
"""
Sanity tests for scripts/ingredients_db.py and scripts/submit_recipe.py.
Runs standalone (python3 tests/test_submit_recipe.py) or via pytest.
"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

import ingredients_db  # noqa: E402
import submit_recipe as sr  # noqa: E402


def test_autocomplete_matches_prefix():
    results = ingredients_db.autocomplete("chick")
    names = [e["name"] for e in results]
    assert "chicken breast" in names
    assert all(n.startswith("chick") or "chick" in n for n in names)


def test_autocomplete_empty_prefix_returns_nothing():
    assert ingredients_db.autocomplete("") == []


def test_suggest_quantity_scales_linearly_with_servings():
    qty4, unit4 = ingredients_db.suggest_quantity("chicken breast", 4)
    qty8, unit8 = ingredients_db.suggest_quantity("chicken breast", 8)
    assert unit4 == unit8
    assert qty8 > qty4  # roughly double, allowing for rounding

    ratio = qty8 / qty4
    assert 1.7 <= ratio <= 2.3


def test_suggest_quantity_unknown_ingredient_returns_none():
    qty, unit = ingredients_db.suggest_quantity("unobtainium dust", 4)
    assert qty is None


def test_suggest_quantity_piece_unit_is_a_whole_number():
    qty, unit = ingredients_db.suggest_quantity("garlic", 4)
    assert unit == "piece"
    assert qty == int(qty)
    assert qty >= 1


def test_start_submission_requires_positive_servings():
    try:
        sr.start_submission("Test Dish", 0)
        assert False, "expected ValueError for servings < 1"
    except ValueError:
        pass


def test_add_ingredient_autofills_from_reference_db():
    draft = sr.start_submission("Test Dish", servings=4, cuisine="American", category="main")
    ing = sr.add_ingredient(draft, "chicken breast")
    assert ing["quantity"] > 0
    assert ing["unit"] == "g"
    assert ing["grocery_category"] == "meat-poultry"


def test_add_ingredient_respects_manual_override():
    draft = sr.start_submission("Test Dish", servings=4)
    ing = sr.add_ingredient(draft, "fresh thyme", quantity=2, unit="tsp")
    assert ing["quantity"] == 2
    assert ing["unit"] == "tsp"


def test_add_step_flags_key_steps_by_keyword():
    draft = sr.start_submission("Test Dish", servings=4)
    _, is_key_chop = sr.add_step(draft, "Finely chop the onions.")
    _, is_key_roast = sr.add_step(draft, "Roast the whole spices until fragrant.")
    assert is_key_chop is False
    assert is_key_roast is True
    assert "step-2" in draft["photos_needed"]
    assert "step-1" not in draft["photos_needed"]


def test_finalize_produces_schema_valid_submission():
    draft = sr.start_submission("Test Dish", servings=2, cuisine="Test", category="main")
    sr.add_ingredient(draft, "chicken breast")
    sr.add_step(draft, "Sear the chicken until golden.")
    sr.mark_ingredients_photo_needed(draft)
    sr.mark_final_photo_needed(draft)
    draft["dietary"] = ["gluten-free"]

    finalized = sr.finalize(draft)  # raises on schema violation
    assert finalized["status"] == "submitted"
    assert finalized["submitted_by"] is None
    assert finalized["source"] == "user-submitted"
    assert "ingredients" in finalized["photos_needed"]
    assert "final" in finalized["photos_needed"]
    assert finalized["id"] == "test-dish"


def test_start_submission_with_kitchen_name_is_schema_valid():
    draft = sr.start_submission("Test Dish", servings=2, cuisine="Test", category="main",
                                 kitchen_name="Nina's Kitchen")
    assert draft["submitted_kitchen"] == "Nina's Kitchen"
    sr.add_ingredient(draft, "chicken breast")
    sr.add_step(draft, "Sear the chicken until golden.")
    finalized = sr.finalize(draft)  # raises on schema violation
    assert finalized["submitted_kitchen"] == "Nina's Kitchen"


def test_start_submission_without_kitchen_name_omits_field():
    draft = sr.start_submission("Test Dish", servings=2)
    assert "submitted_kitchen" not in draft


def test_finalize_rejects_missing_ingredients():
    draft = sr.start_submission("Empty Dish", servings=2)
    sr.add_step(draft, "Do something.")
    try:
        sr.finalize(draft)
        assert False, "expected a validation error for zero ingredients"
    except Exception:
        pass


def test_save_submission_persists_locally_and_list_submissions_finds_it():
    """save_submission()/list_submissions() write to and read from
    data/submissions/ — redirect that to a scratch directory for the
    duration of this test so it never touches the real project folder."""
    original_dir = sr.SUBMISSIONS_DIR
    scratch = tempfile.mkdtemp()
    sr.SUBMISSIONS_DIR = scratch
    try:
        draft = sr.start_submission("Test Save Dish", servings=2, cuisine="Test", category="main")
        sr.add_ingredient(draft, "chicken breast")
        sr.add_step(draft, "Sear the chicken until golden.")
        finalized = sr.finalize(draft)

        path = sr.save_submission(finalized)
        assert os.path.exists(path)
        assert path.endswith("test-save-dish.json")

        with open(path, "r", encoding="utf-8") as f:
            on_disk = json.load(f)
        assert on_disk["id"] == "test-save-dish"
        assert on_disk["status"] == "submitted"

        found = sr.list_submissions()
        assert any(r["id"] == "test-save-dish" for r in found)
    finally:
        sr.SUBMISSIONS_DIR = original_dir
        shutil.rmtree(scratch, ignore_errors=True)


def test_list_submissions_empty_when_directory_missing():
    original_dir = sr.SUBMISSIONS_DIR
    sr.SUBMISSIONS_DIR = os.path.join(tempfile.mkdtemp(), "does-not-exist")
    try:
        assert sr.list_submissions() == []
    finally:
        sr.SUBMISSIONS_DIR = original_dir


def _run_all():
    tests = [obj for name, obj in list(globals().items()) if name.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    _run_all()
