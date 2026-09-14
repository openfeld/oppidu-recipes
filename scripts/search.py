#!/usr/bin/env python3
"""
Oppidu Recipes — local search engine (+ external fallback hook).

This is the piece meant to eventually sit behind Oppidu's recipe search:
`find_recipe()` looks in the local JSON database FIRST, and only calls
out to `search_external()` when the local database has nothing good
enough. Today `search_external()` is a documented stub — wire in a real
provider (a recipe API, or a web-search-backed generator) when ready;
nothing else in this file needs to change.

No third-party dependencies — stdlib only, so it runs anywhere.

CLI usage:
    python3 scripts/search.py "chickpea curry"
    python3 scripts/search.py "spicy chicken" --cuisine Indian
    python3 scripts/search.py "something with tofu" --dietary vegan
"""
import argparse
import difflib
import json
import os
import unicodedata

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "data", "index.json")
RECIPES_DIR = os.path.join(BASE_DIR, "data", "recipes")

# Below this combined relevance score, local results are considered too
# weak to answer the query and find_recipe() will fall back to external.
LOCAL_MATCH_THRESHOLD = 0.35


def _tokenize(text):
    """Split text into tokens for any script, not just ASCII Latin.

    A plain `[^a-z0-9]+` split (the previous approach) silently drops every
    non-ASCII character, so a German umlaut splits a word in two and a
    Chinese/Arabic/Hindi query tokenizes to nothing at all — the opposite of
    "search in any language". This keeps a character as part of the current
    token when it's a letter or digit (any script) or a combining mark (the
    accent/vowel-sign characters that stack onto a base letter in scripts
    like Hindi's Devanagari), and treats everything else — punctuation,
    whitespace, symbols — as a separator, the same role `[^a-z0-9]+` played
    for ASCII text.
    """
    tokens = []
    current = []
    for ch in text.lower():
        category = unicodedata.category(ch)
        if category[0] in ("L", "N") or category in ("Mn", "Mc"):
            current.append(ch)
        elif current:
            tokens.append("".join(current))
            current = []
    if current:
        tokens.append("".join(current))
    return tokens


def _load_index():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_recipe(recipe_id):
    """Load a full recipe record by id."""
    path = os.path.join(RECIPES_DIR, f"{recipe_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _score_entry(query_tokens, entry):
    """Cheap, dependency-free relevance score in [0, ~1.6].

    Weighted field matching: title > tags/cuisine > ingredients, plus a
    fuzzy bonus so near-misses ("chiken" -> "chicken") still surface.
    """
    haystacks = {
        "title": (_tokenize(entry["title"]), 1.0),
        "tags": (_tokenize(" ".join(entry.get("tags", []))), 0.6),
        "cuisine": (_tokenize(entry.get("cuisine", "")), 0.6),
        "category": (_tokenize(entry.get("category", "")), 0.3),
        "dietary": (_tokenize(" ".join(entry.get("dietary", []))), 0.3),
        "ingredients": (_tokenize(" ".join(entry.get("ingredient_names", []))), 0.4),
    }

    score = 0.0
    for qt in query_tokens:
        # Very short tokens ("a", "in", "e"...) are noise on either side of
        # the comparison: substring or fuzzy containment involving them
        # matches almost anything, so only count them on an exact word match.
        qt_short = len(qt) < 3
        best_field_hit = 0.0
        for tokens, weight in haystacks.values():
            for t in tokens:
                if qt == t:
                    hit = 1.0
                elif qt_short or len(t) < 3:
                    hit = 0.0
                elif (qt in t or t in qt) and min(len(qt), len(t)) / max(len(qt), len(t)) >= 0.5:
                    # Guard against coincidental substrings ("red" sits
                    # inside "ingredient" but has nothing to do with it) by
                    # requiring the shorter token to cover a real portion
                    # of the longer one.
                    hit = 0.7
                else:
                    ratio = difflib.SequenceMatcher(None, qt, t).ratio()
                    hit = ratio if ratio > 0.82 else 0.0
                best_field_hit = max(best_field_hit, hit * weight)
        score += best_field_hit

    return score / max(len(query_tokens), 1)


def search_local(query, cuisine=None, dietary=None, category=None, max_results=10):
    """Search the local recipe database. Returns a list of
    {id, title, cuisine, category, score} sorted by descending score.
    """
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    results = []
    for entry in _load_index():
        if cuisine and entry.get("cuisine", "").lower() != cuisine.lower():
            continue
        if dietary and dietary.lower() not in [d.lower() for d in entry.get("dietary", [])]:
            continue
        if category and entry.get("category", "").lower() != category.lower():
            continue

        score = _score_entry(query_tokens, entry)
        if score > 0:
            results.append({
                "id": entry["id"],
                "title": entry["title"],
                "cuisine": entry["cuisine"],
                "category": entry["category"],
                "score": round(score, 3),
            })

    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:max_results]


def search_external(query, cuisine=None, dietary=None, category=None):
    """Fallback when the local database doesn't have a good match.

    STUB — not yet implemented. Intended integration points (pick one
    when Oppidu wires this up for real):
      1. A recipe API (e.g. Spoonacular, Edamam) — call it here, map
         its response into the same schema as schema/recipe.schema.json
         (ingredient `grocery_category` will need inferring), and
         optionally write the result into data/recipes/ so it's cached
         locally for next time.
      2. An LLM generation call (see scripts/generate_recipe.py) —
         generate a fresh recipe on demand for queries the local DB and
         any recipe API both miss.

    Returns an empty list today; callers should treat that as
    "no external source configured yet", not "no recipe exists".
    """
    return []


def find_recipe(query, cuisine=None, dietary=None, category=None, max_results=10):
    """Orchestrator: local database first, external sources on a weak/empty
    local result. This is the function a future Oppidu integration calls.
    """
    local_results = search_local(query, cuisine=cuisine, dietary=dietary,
                                  category=category, max_results=max_results)

    if local_results and local_results[0]["score"] >= LOCAL_MATCH_THRESHOLD:
        return {"source": "local", "results": local_results}

    external_results = search_external(query, cuisine=cuisine, dietary=dietary, category=category)
    if external_results:
        return {"source": "external", "results": external_results}

    # Nothing external configured yet — still return whatever weak local
    # matches exist rather than nothing at all.
    return {"source": "local-weak" if local_results else "none", "results": local_results}


def main():
    parser = argparse.ArgumentParser(description="Search the Oppidu Recipes database.")
    parser.add_argument("query", help="Free-text search query")
    parser.add_argument("--cuisine", help="Filter by cuisine, e.g. Indian")
    parser.add_argument("--dietary", help="Filter by dietary tag, e.g. vegan")
    parser.add_argument("--category", help="Filter by category, e.g. main")
    parser.add_argument("--full", action="store_true", help="Print full recipe JSON for the top match")
    args = parser.parse_args()

    outcome = find_recipe(args.query, cuisine=args.cuisine, dietary=args.dietary, category=args.category)
    print(f"source: {outcome['source']}")
    for r in outcome["results"]:
        print(f"  {r['score']:.3f}  {r['id']:<28} {r['title']} [{r['cuisine']} / {r['category']}]")

    if args.full and outcome["results"]:
        top = load_recipe(outcome["results"][0]["id"])
        print("\n--- top match, full record ---")
        print(json.dumps(top, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
