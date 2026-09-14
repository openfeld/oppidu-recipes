"""
Oppidu Recipes — curated nutrition reference data.

Hand-authored, approximate, per-100g macros for every base ingredient
currently in data/ingredients.json (see `ingredients_db.base_name()` for
how a raw ingredient name reduces to the keys used here — the same
reduction `nutrition.py` uses to look a typed ingredient up in this table).

These are rough, commonly-cited averages (the same kind of figure a
household nutrition label or recipe site would show), not a lab analysis —
intentionally so: `nutrition.py`'s whole estimate is explicitly presented
to the user as an estimate, never a precise fact. Where a name says
"dried"/"cooked" the value matches that state (e.g. "dried chickpeas" is
the raw dry-weight figure, "canned chickpeas" and "cooked short-grain
rice" are the already-prepared figure) — matching how a recipe actually
states the quantity for that ingredient.

Extending the database: add a recipe's ingredients to data/recipes/, run
`python3 scripts/ingredients_db.py` so the name lands in data/ingredients.json,
then add its macros here using the same base-name key. Nothing else needs
to change — nutrition.py and the wizard's live estimate both read this
table directly.
"""

# kcal, fat_g, carbs_g, protein_g per 100g.
NUTRITION_PER_100G = {
    # -- vegetables --
    "onion": {"kcal": 40, "fat_g": 0.1, "carbs_g": 9.3, "protein_g": 1.1},
    "red onion": {"kcal": 40, "fat_g": 0.1, "carbs_g": 9.3, "protein_g": 1.1},
    "white onion": {"kcal": 40, "fat_g": 0.1, "carbs_g": 9.3, "protein_g": 1.1},
    "spring onion": {"kcal": 32, "fat_g": 0.2, "carbs_g": 7.3, "protein_g": 1.8},
    "garlic": {"kcal": 149, "fat_g": 0.5, "carbs_g": 33.0, "protein_g": 6.4},
    "garlic clove": {"kcal": 149, "fat_g": 0.5, "carbs_g": 33.0, "protein_g": 6.4},
    "garlic cloves": {"kcal": 149, "fat_g": 0.5, "carbs_g": 33.0, "protein_g": 6.4},
    "garlic paste": {"kcal": 149, "fat_g": 0.5, "carbs_g": 33.0, "protein_g": 6.4},
    "ginger": {"kcal": 80, "fat_g": 0.8, "carbs_g": 18.0, "protein_g": 1.8},
    "ginger paste": {"kcal": 80, "fat_g": 0.8, "carbs_g": 18.0, "protein_g": 1.8},
    "ginger-garlic paste": {"kcal": 115, "fat_g": 0.65, "carbs_g": 25.0, "protein_g": 4.1},
    "potatoes": {"kcal": 77, "fat_g": 0.1, "carbs_g": 17.0, "protein_g": 2.0},
    "tomato": {"kcal": 18, "fat_g": 0.2, "carbs_g": 3.9, "protein_g": 0.9},
    "tomatoes": {"kcal": 18, "fat_g": 0.2, "carbs_g": 3.9, "protein_g": 0.9},
    "cauliflower": {"kcal": 25, "fat_g": 0.3, "carbs_g": 5.0, "protein_g": 1.9},
    "bell pepper": {"kcal": 31, "fat_g": 0.3, "carbs_g": 6.0, "protein_g": 1.0},
    "bell peppers": {"kcal": 31, "fat_g": 0.3, "carbs_g": 6.0, "protein_g": 1.0},
    "cucumber": {"kcal": 15, "fat_g": 0.1, "carbs_g": 3.6, "protein_g": 0.7},
    "eggplant": {"kcal": 25, "fat_g": 0.2, "carbs_g": 6.0, "protein_g": 1.0},
    "jalapeno": {"kcal": 29, "fat_g": 0.4, "carbs_g": 6.5, "protein_g": 0.9},
    "green chili": {"kcal": 40, "fat_g": 0.2, "carbs_g": 9.0, "protein_g": 2.0},
    "lettuce leaves": {"kcal": 15, "fat_g": 0.2, "carbs_g": 2.9, "protein_g": 1.4},
    "spinach": {"kcal": 23, "fat_g": 0.4, "carbs_g": 3.6, "protein_g": 2.9},
    "zucchini": {"kcal": 17, "fat_g": 0.3, "carbs_g": 3.1, "protein_g": 1.2},
    "thai eggplant or zucchini": {"kcal": 20, "fat_g": 0.25, "carbs_g": 4.0, "protein_g": 1.1},
    "bean sprouts": {"kcal": 30, "fat_g": 0.2, "carbs_g": 5.9, "protein_g": 3.0},
    "shiitake mushrooms": {"kcal": 34, "fat_g": 0.5, "carbs_g": 6.8, "protein_g": 2.2},
    "carrot": {"kcal": 41, "fat_g": 0.2, "carbs_g": 10.0, "protein_g": 0.9},

    # -- fruits --
    "lemon juice": {"kcal": 22, "fat_g": 0.2, "carbs_g": 6.9, "protein_g": 0.4},
    "lime juice": {"kcal": 25, "fat_g": 0.2, "carbs_g": 8.4, "protein_g": 0.4},
    "ripe avocados": {"kcal": 160, "fat_g": 15.0, "carbs_g": 8.5, "protein_g": 2.0},
    "pineapple": {"kcal": 50, "fat_g": 0.1, "carbs_g": 13.0, "protein_g": 0.5},

    # -- fresh herbs --
    "cilantro": {"kcal": 23, "fat_g": 0.5, "carbs_g": 3.7, "protein_g": 2.1},
    "parsley": {"kcal": 36, "fat_g": 0.8, "carbs_g": 6.3, "protein_g": 3.0},
    "thai basil leaves": {"kcal": 22, "fat_g": 0.6, "carbs_g": 2.6, "protein_g": 3.2},
    "fresh basil leaves": {"kcal": 23, "fat_g": 0.6, "carbs_g": 2.7, "protein_g": 3.2},
    "kaffir lime leaves": {"kcal": 65, "fat_g": 1.0, "carbs_g": 15.0, "protein_g": 2.0},
    "kasuri methi": {"kcal": 320, "fat_g": 6.0, "carbs_g": 47.0, "protein_g": 27.0},

    # -- meat & poultry --
    "chicken breast": {"kcal": 165, "fat_g": 3.6, "carbs_g": 0.0, "protein_g": 31.0},
    "chicken thighs": {"kcal": 209, "fat_g": 10.9, "carbs_g": 0.0, "protein_g": 26.0},
    "boneless chicken thighs": {"kcal": 209, "fat_g": 10.9, "carbs_g": 0.0, "protein_g": 26.0},
    "beef sirloin": {"kcal": 183, "fat_g": 8.7, "carbs_g": 0.0, "protein_g": 26.0},
    "ground beef": {"kcal": 250, "fat_g": 20.0, "carbs_g": 0.0, "protein_g": 17.0},

    # -- dairy --
    "butter": {"kcal": 717, "fat_g": 81.0, "carbs_g": 0.1, "protein_g": 0.9},
    "buttermilk": {"kcal": 40, "fat_g": 1.0, "carbs_g": 4.8, "protein_g": 3.3},
    "cheddar cheese slices": {"kcal": 402, "fat_g": 33.0, "carbs_g": 1.3, "protein_g": 25.0},
    "eggs": {"kcal": 155, "fat_g": 11.0, "carbs_g": 1.1, "protein_g": 13.0},
    "feta cheese block": {"kcal": 264, "fat_g": 21.0, "carbs_g": 4.1, "protein_g": 14.0},
    "fresh mozzarella": {"kcal": 280, "fat_g": 22.0, "carbs_g": 2.2, "protein_g": 18.0},
    "heavy cream": {"kcal": 340, "fat_g": 36.0, "carbs_g": 2.8, "protein_g": 2.1},
    "parmesan cheese": {"kcal": 431, "fat_g": 29.0, "carbs_g": 4.1, "protein_g": 38.0},
    "plain yogurt": {"kcal": 59, "fat_g": 3.3, "carbs_g": 4.7, "protein_g": 3.5},

    # -- grains & rice --
    # "rice" uses the COOKED value: in an ingredient list it's near-always
    # a already-cooked amount measured by cup/g in a finished dish (fried
    # rice, a rice bowl) — base_name() reduces "rice, cooked and cooled"
    # to plain "rice" too, so the bare key has to carry that meaning.
    "rice": {"kcal": 130, "fat_g": 0.3, "carbs_g": 28.0, "protein_g": 2.7},
    "cooked short-grain rice": {"kcal": 130, "fat_g": 0.3, "carbs_g": 28.0, "protein_g": 2.7},
    # Pasta is the opposite convention — a recipe states dry weight before
    # cooking ("300g spaghetti"), so this is the dry/raw figure.
    "spaghetti": {"kcal": 371, "fat_g": 1.5, "carbs_g": 75.0, "protein_g": 13.0},

    # -- lentils & pulses --
    "dried chickpeas": {"kcal": 364, "fat_g": 6.0, "carbs_g": 61.0, "protein_g": 19.0},

    # -- flour & baking --
    "00 flour or bread flour": {"kcal": 361, "fat_g": 1.5, "carbs_g": 73.0, "protein_g": 12.0},
    "active dry yeast": {"kcal": 325, "fat_g": 7.0, "carbs_g": 41.0, "protein_g": 40.0},
    "all-purpose flour": {"kcal": 364, "fat_g": 1.0, "carbs_g": 76.0, "protein_g": 10.0},
    "baking powder": {"kcal": 53, "fat_g": 0.0, "carbs_g": 28.0, "protein_g": 0.0},
    "baking soda": {"kcal": 0, "fat_g": 0.0, "carbs_g": 0.0, "protein_g": 0.0},
    "cornstarch": {"kcal": 381, "fat_g": 0.1, "carbs_g": 91.0, "protein_g": 0.3},

    # -- condiments & sauces --
    "achiote paste": {"kcal": 250, "fat_g": 5.0, "carbs_g": 45.0, "protein_g": 5.0},
    "black vinegar": {"kcal": 30, "fat_g": 0.0, "carbs_g": 6.0, "protein_g": 1.0},
    "fish sauce": {"kcal": 35, "fat_g": 0.0, "carbs_g": 3.6, "protein_g": 5.1},
    "gochujang": {"kcal": 220, "fat_g": 2.0, "carbs_g": 44.0, "protein_g": 5.0},
    "green curry paste": {"kcal": 90, "fat_g": 4.0, "carbs_g": 12.0, "protein_g": 2.0},
    "ketchup": {"kcal": 112, "fat_g": 0.1, "carbs_g": 27.0, "protein_g": 1.2},
    "maple syrup": {"kcal": 260, "fat_g": 0.1, "carbs_g": 67.0, "protein_g": 0.0},
    "mirin": {"kcal": 225, "fat_g": 0.0, "carbs_g": 43.2, "protein_g": 0.2},
    "miso paste": {"kcal": 199, "fat_g": 6.0, "carbs_g": 26.0, "protein_g": 12.0},
    "mustard": {"kcal": 66, "fat_g": 3.3, "carbs_g": 7.1, "protein_g": 4.4},
    "soy sauce": {"kcal": 53, "fat_g": 0.1, "carbs_g": 4.9, "protein_g": 8.1},
    "tahini": {"kcal": 595, "fat_g": 54.0, "carbs_g": 21.0, "protein_g": 17.0},

    # -- oils & fats --
    "extra virgin olive oil": {"kcal": 884, "fat_g": 100.0, "carbs_g": 0.0, "protein_g": 0.0},
    "olive oil": {"kcal": 884, "fat_g": 100.0, "carbs_g": 0.0, "protein_g": 0.0},
    "sesame oil": {"kcal": 884, "fat_g": 100.0, "carbs_g": 0.0, "protein_g": 0.0},
    "vegetable oil": {"kcal": 884, "fat_g": 100.0, "carbs_g": 0.0, "protein_g": 0.0},

    # -- nuts & seeds --
    "roasted peanuts": {"kcal": 585, "fat_g": 50.0, "carbs_g": 21.0, "protein_g": 24.0},
    "sesame seeds": {"kcal": 573, "fat_g": 50.0, "carbs_g": 23.0, "protein_g": 18.0},

    # -- canned & jarred --
    "canned san marzano tomatoes": {"kcal": 18, "fat_g": 0.2, "carbs_g": 4.0, "protein_g": 0.9},
    "canned chickpeas": {"kcal": 164, "fat_g": 2.6, "carbs_g": 27.0, "protein_g": 8.9},
    "coconut milk": {"kcal": 230, "fat_g": 24.0, "carbs_g": 5.5, "protein_g": 2.3},
    "kalamata olives": {"kcal": 115, "fat_g": 11.0, "carbs_g": 6.0, "protein_g": 0.8},
    "pickles": {"kcal": 11, "fat_g": 0.2, "carbs_g": 2.3, "protein_g": 0.3},
    "tomato puree": {"kcal": 38, "fat_g": 0.2, "carbs_g": 8.8, "protein_g": 1.9},

    # -- frozen --
    "peas": {"kcal": 81, "fat_g": 0.4, "carbs_g": 14.0, "protein_g": 5.4},

    # -- spices (small quantities, but filled in for completeness) --
    "chana masala spice blend": {"kcal": 300, "fat_g": 10.0, "carbs_g": 45.0, "protein_g": 10.0},
    "coriander powder": {"kcal": 298, "fat_g": 13.0, "carbs_g": 55.0, "protein_g": 12.0},
    "cumin powder": {"kcal": 375, "fat_g": 22.0, "carbs_g": 44.0, "protein_g": 18.0},
    "cumin seeds": {"kcal": 375, "fat_g": 22.0, "carbs_g": 44.0, "protein_g": 18.0},
    "dried oregano": {"kcal": 265, "fat_g": 4.3, "carbs_g": 69.0, "protein_g": 9.0},
    "dried red chilies": {"kcal": 282, "fat_g": 14.0, "carbs_g": 50.0, "protein_g": 12.0},
    "garam masala": {"kcal": 379, "fat_g": 15.0, "carbs_g": 58.0, "protein_g": 14.0},
    "herbes de provence": {"kcal": 260, "fat_g": 5.0, "carbs_g": 55.0, "protein_g": 10.0},
    "kashmiri chili powder": {"kcal": 282, "fat_g": 14.0, "carbs_g": 50.0, "protein_g": 12.0},
    "red chili flakes": {"kcal": 282, "fat_g": 14.0, "carbs_g": 50.0, "protein_g": 12.0},
    "sichuan peppercorns": {"kcal": 260, "fat_g": 8.0, "carbs_g": 55.0, "protein_g": 8.0},
    "turmeric powder": {"kcal": 312, "fat_g": 3.2, "carbs_g": 65.0, "protein_g": 8.0},
    # Listed explicitly (most recipes use "to taste", which is excluded
    # from every estimate regardless) so that a recipe giving one of these
    # an actual gram quantity counts as *covered* rather than unknown —
    # salt genuinely has ~0 macros; black pepper is a real dried spice.
    "salt": {"kcal": 0, "fat_g": 0.0, "carbs_g": 0.0, "protein_g": 0.0},
    "black pepper": {"kcal": 251, "fat_g": 3.3, "carbs_g": 64.0, "protein_g": 10.0},

    # -- other --
    "dried wakame seaweed": {"kcal": 45, "fat_g": 0.6, "carbs_g": 9.0, "protein_g": 3.0},
    "palm sugar": {"kcal": 383, "fat_g": 0.0, "carbs_g": 98.0, "protein_g": 0.0},
    "silken tofu": {"kcal": 55, "fat_g": 3.0, "carbs_g": 2.0, "protein_g": 6.0},
    "sugar": {"kcal": 387, "fat_g": 0.0, "carbs_g": 100.0, "protein_g": 0.0},

    # -- bakery --
    "burger buns": {"kcal": 264, "fat_g": 5.0, "carbs_g": 47.0, "protein_g": 9.0},
    "corn tortillas": {"kcal": 218, "fat_g": 2.9, "carbs_g": 45.0, "protein_g": 5.7},

    # -- beverages --
    "dashi stock": {"kcal": 3, "fat_g": 0.0, "carbs_g": 0.3, "protein_g": 0.5},
    "ice water": {"kcal": 0, "fat_g": 0.0, "carbs_g": 0.0, "protein_g": 0.0},
    "orange juice": {"kcal": 45, "fat_g": 0.2, "carbs_g": 10.4, "protein_g": 0.7},
    "sake": {"kcal": 134, "fat_g": 0.0, "carbs_g": 5.0, "protein_g": 0.5},
    "water": {"kcal": 0, "fat_g": 0.0, "carbs_g": 0.0, "protein_g": 0.0},
}

# Average grams for one "piece" of ingredients commonly measured that way —
# used only when an ingredient's unit is "piece", since that unit alone
# doesn't say whether a "piece" is a whole cauliflower or a single garlic
# clove. Anything not listed falls back to PIECE_GRAMS_DEFAULT.
PIECE_GRAMS = {
    "onion": 110, "red onion": 110, "white onion": 110, "spring onion": 15,
    "garlic": 5, "garlic clove": 5, "garlic cloves": 5,
    "bell pepper": 120, "bell peppers": 120,
    "carrot": 60, "cauliflower": 600, "cucumber": 300, "eggplant": 250,
    "jalapeno": 14, "green chili": 5, "lettuce leaves": 10,
    "potatoes": 150, "tomato": 120, "tomatoes": 120, "zucchini": 200,
    "burger buns": 60, "cheddar cheese slices": 20, "corn tortillas": 25,
    "dried red chilies": 2, "eggs": 50, "fresh basil leaves": 1,
    "kaffir lime leaves": 0.5, "pickles": 30, "ripe avocados": 200,
}
PIECE_GRAMS_DEFAULT = 50

# Grams per unit for everything that isn't "piece". "to taste" has no
# sensible gram conversion and is deliberately left out — an ingredient
# measured that way (salt, pepper) is excluded from every estimate, the
# same way an unrecognized unit would be.
UNIT_TO_GRAMS = {
    "g": 1.0, "kg": 1000.0,
    "ml": 1.0, "l": 1000.0,
    "tsp": 5.0, "tbsp": 15.0, "cup": 240.0, "pinch": 0.3,
}
