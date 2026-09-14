#!/usr/bin/env python3
"""
Sanity tests for scripts/search.py. Runs standalone (python3 tests/test_search.py)
or via pytest.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

import search  # noqa: E402


def test_exact_title_word_match_ranks_first():
    result = search.find_recipe("chickpea curry")
    assert result["source"] == "local"
    assert result["results"][0]["id"] == "chana-masala"


def test_cuisine_filter_excludes_other_cuisines():
    result = search.find_recipe("curry", cuisine="Indian")
    assert result["source"] == "local"
    for r in result["results"]:
        assert r["cuisine"] == "Indian"


def test_dietary_filter_applies():
    results = search.search_local("curry", dietary="vegan")
    for r in results:
        recipe = search.load_recipe(r["id"])
        assert "vegan" in recipe["dietary"]


def test_nonsense_query_returns_no_source():
    result = search.find_recipe("zzz_not_a_real_ingredient_zzz")
    assert result["source"] == "none"
    assert result["results"] == []


def test_external_stub_returns_empty_list():
    assert search.search_external("anything") == []


def test_load_recipe_missing_id_returns_none():
    assert search.load_recipe("does-not-exist") is None


def test_load_recipe_returns_full_schema_fields():
    recipe = search.load_recipe("butter-chicken")
    assert recipe is not None
    for field in ("id", "title", "cuisine", "ingredients", "instructions", "source"):
        assert field in recipe


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
