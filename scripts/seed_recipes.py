#!/usr/bin/env python3
"""
Seed script for the Oppidu Recipes database.

These 18 recipes were AI-generated (by Claude) as the initial seed set for
the local recipe database, spanning a deliberately wide range of cuisines.
Each recipe conforms to schema/recipe.schema.json. Ingredients carry a
`grocery_category` so that a downstream consumer (e.g. Oppidu) can later
map them onto a grocery store's catalog for price comparison.

Run: python3 scripts/seed_recipes.py
Writes one JSON file per recipe into data/recipes/<id>.json.
"""
import json
import os

RECIPES = [
    {
        "id": "butter-chicken",
        "title": "Butter Chicken (Murgh Makhani)",
        "description": "Creamy, tomato-based North Indian curry with tandoori-spiced chicken.",
        "cuisine": "Indian",
        "category": "main",
        "servings": 4,
        "prep_time_minutes": 30,
        "cook_time_minutes": 40,
        "difficulty": "medium",
        "ingredients": [
            {"name": "boneless chicken thighs", "quantity": 700, "unit": "g", "grocery_category": "meat-poultry"},
            {"name": "plain yogurt", "quantity": 150, "unit": "g", "grocery_category": "dairy"},
            {"name": "garlic paste", "quantity": 1, "unit": "tbsp", "grocery_category": "vegetables"},
            {"name": "ginger paste", "quantity": 1, "unit": "tbsp", "grocery_category": "vegetables"},
            {"name": "garam masala", "quantity": 2, "unit": "tsp", "grocery_category": "spices"},
            {"name": "kashmiri chili powder", "quantity": 1, "unit": "tsp", "grocery_category": "spices"},
            {"name": "butter", "quantity": 60, "unit": "g", "grocery_category": "dairy"},
            {"name": "tomato puree", "quantity": 400, "unit": "g", "grocery_category": "canned-jarred"},
            {"name": "heavy cream", "quantity": 100, "unit": "ml", "grocery_category": "dairy"},
            {"name": "kasuri methi (dried fenugreek leaves)", "quantity": 1, "unit": "tsp", "grocery_category": "herbs-fresh"},
            {"name": "sugar", "quantity": 1, "unit": "tsp", "grocery_category": "other"}
        ],
        "instructions": [
            "Marinate chicken in yogurt, garlic, ginger, garam masala and chili powder for at least 1 hour (overnight is best).",
            "Sear the marinated chicken in a hot pan or grill until charred at the edges; set aside.",
            "Melt butter in a pan, add remaining garlic and ginger, cook 1 minute.",
            "Add tomato puree and simmer 15 minutes until thickened and the raw smell is gone.",
            "Blend the sauce smooth, return to the pan, stir in cream, sugar and kasuri methi.",
            "Add the seared chicken and simmer 10 minutes until cooked through.",
            "Finish with a swirl of cream and serve with naan or rice."
        ],
        "tags": ["curry", "creamy", "weeknight", "restaurant-style"],
        "dietary": ["non-vegetarian"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "chana-masala",
        "title": "Chana Masala (Spiced Chickpea Curry)",
        "description": "Punchy, tangy chickpea curry from North India, naturally vegan.",
        "cuisine": "Indian",
        "category": "main",
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 30,
        "difficulty": "easy",
        "ingredients": [
            {"name": "canned chickpeas", "quantity": 2, "unit": "cup", "grocery_category": "canned-jarred"},
            {"name": "onion, finely chopped", "quantity": 1, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "tomatoes, pureed", "quantity": 2, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "ginger-garlic paste", "quantity": 1, "unit": "tbsp", "grocery_category": "vegetables"},
            {"name": "chana masala spice blend", "quantity": 2, "unit": "tsp", "grocery_category": "spices"},
            {"name": "cumin seeds", "quantity": 1, "unit": "tsp", "grocery_category": "spices"},
            {"name": "vegetable oil", "quantity": 2, "unit": "tbsp", "grocery_category": "oils-fats"},
            {"name": "cilantro, chopped", "quantity": 2, "unit": "tbsp", "grocery_category": "herbs-fresh"},
            {"name": "lemon juice", "quantity": 1, "unit": "tbsp", "grocery_category": "fruits"}
        ],
        "instructions": [
            "Heat oil, temper cumin seeds until fragrant.",
            "Add onion, cook until golden, then add ginger-garlic paste.",
            "Add tomato puree and spice blend, cook until oil separates.",
            "Add chickpeas with a splash of water, simmer 15 minutes, mashing a few for body.",
            "Finish with lemon juice and cilantro; serve with rice or roti."
        ],
        "tags": ["vegan", "budget-friendly", "one-pot", "weeknight"],
        "dietary": ["vegan", "vegetarian", "gluten-free"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "aloo-gobi",
        "title": "Aloo Gobi (Potato & Cauliflower Curry)",
        "description": "Dry-spiced potato and cauliflower stir-fry, a North Indian staple.",
        "cuisine": "Indian",
        "category": "side",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 25,
        "difficulty": "easy",
        "ingredients": [
            {"name": "cauliflower, cut into florets", "quantity": 1, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "potatoes, cubed", "quantity": 3, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "turmeric powder", "quantity": 0.5, "unit": "tsp", "grocery_category": "spices"},
            {"name": "cumin seeds", "quantity": 1, "unit": "tsp", "grocery_category": "spices"},
            {"name": "coriander powder", "quantity": 1, "unit": "tsp", "grocery_category": "spices"},
            {"name": "vegetable oil", "quantity": 3, "unit": "tbsp", "grocery_category": "oils-fats"},
            {"name": "green chili, slit", "quantity": 1, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "cilantro, chopped", "quantity": 2, "unit": "tbsp", "grocery_category": "herbs-fresh"}
        ],
        "instructions": [
            "Heat oil, temper cumin seeds.",
            "Add potatoes, cook 5 minutes stirring occasionally.",
            "Add cauliflower, turmeric, coriander powder and chili; mix well.",
            "Cover and cook on low heat 15-18 minutes until tender, stirring occasionally.",
            "Garnish with cilantro and serve with roti."
        ],
        "tags": ["vegan", "dry-curry", "everyday"],
        "dietary": ["vegan", "vegetarian", "gluten-free"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "spaghetti-aglio-e-olio",
        "title": "Spaghetti Aglio e Olio",
        "description": "Classic Roman pasta of garlic, olive oil and chili flakes.",
        "cuisine": "Italian",
        "category": "main",
        "servings": 2,
        "prep_time_minutes": 5,
        "cook_time_minutes": 15,
        "difficulty": "easy",
        "ingredients": [
            {"name": "spaghetti", "quantity": 200, "unit": "g", "grocery_category": "grains-rice"},
            {"name": "garlic, thinly sliced", "quantity": 6, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "extra virgin olive oil", "quantity": 80, "unit": "ml", "grocery_category": "oils-fats"},
            {"name": "red chili flakes", "quantity": 1, "unit": "tsp", "grocery_category": "spices"},
            {"name": "parsley, chopped", "quantity": 2, "unit": "tbsp", "grocery_category": "herbs-fresh"},
            {"name": "parmesan cheese, grated", "quantity": 30, "unit": "g", "grocery_category": "dairy", "optional": True}
        ],
        "instructions": [
            "Cook spaghetti in salted water until al dente; reserve 1 cup pasta water.",
            "Gently warm olive oil with garlic and chili flakes until garlic is golden, not browned.",
            "Toss drained pasta into the pan with a splash of pasta water to emulsify.",
            "Stir in parsley, season with salt, and serve with parmesan if desired."
        ],
        "tags": ["quick", "pantry", "weeknight", "vegetarian-optional"],
        "dietary": ["vegetarian"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "margherita-pizza",
        "title": "Margherita Pizza",
        "description": "Neapolitan-style pizza with tomato, mozzarella and basil.",
        "cuisine": "Italian",
        "category": "main",
        "servings": 2,
        "prep_time_minutes": 90,
        "cook_time_minutes": 12,
        "difficulty": "medium",
        "ingredients": [
            {"name": "00 flour or bread flour", "quantity": 300, "unit": "g", "grocery_category": "flour-baking"},
            {"name": "active dry yeast", "quantity": 3, "unit": "g", "grocery_category": "flour-baking"},
            {"name": "water", "quantity": 200, "unit": "ml", "grocery_category": "beverages"},
            {"name": "salt", "quantity": 6, "unit": "g", "grocery_category": "spices"},
            {"name": "canned San Marzano tomatoes, crushed", "quantity": 200, "unit": "g", "grocery_category": "canned-jarred"},
            {"name": "fresh mozzarella, torn", "quantity": 150, "unit": "g", "grocery_category": "dairy"},
            {"name": "fresh basil leaves", "quantity": 10, "unit": "piece", "grocery_category": "herbs-fresh"},
            {"name": "olive oil", "quantity": 2, "unit": "tbsp", "grocery_category": "oils-fats"}
        ],
        "instructions": [
            "Mix flour, yeast, water and salt into a dough; knead 10 minutes until smooth.",
            "Let rise covered for 1-1.5 hours until doubled.",
            "Preheat oven with a pizza stone or tray as hot as it will go (250C+).",
            "Stretch dough into a round, top with crushed tomatoes, mozzarella and a drizzle of oil.",
            "Bake 8-12 minutes until the crust is charred in spots.",
            "Top with fresh basil before serving."
        ],
        "tags": ["baking", "weekend-project", "crowd-pleaser"],
        "dietary": ["vegetarian"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "chicken-tacos",
        "title": "Chicken Tacos al Pastor Style",
        "description": "Achiote-marinated chicken tacos with pineapple, onion and cilantro.",
        "cuisine": "Mexican",
        "category": "main",
        "servings": 4,
        "prep_time_minutes": 30,
        "cook_time_minutes": 20,
        "difficulty": "medium",
        "ingredients": [
            {"name": "chicken thighs, boneless", "quantity": 600, "unit": "g", "grocery_category": "meat-poultry"},
            {"name": "achiote paste", "quantity": 2, "unit": "tbsp", "grocery_category": "condiments-sauces"},
            {"name": "orange juice", "quantity": 60, "unit": "ml", "grocery_category": "beverages"},
            {"name": "lime juice", "quantity": 30, "unit": "ml", "grocery_category": "fruits"},
            {"name": "pineapple, diced", "quantity": 150, "unit": "g", "grocery_category": "fruits"},
            {"name": "corn tortillas", "quantity": 12, "unit": "piece", "grocery_category": "bakery"},
            {"name": "white onion, diced", "quantity": 0.5, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "cilantro, chopped", "quantity": 3, "unit": "tbsp", "grocery_category": "herbs-fresh"}
        ],
        "instructions": [
            "Whisk achiote paste with orange and lime juice; marinate chicken 1-2 hours.",
            "Sear chicken in a hot pan until charred and cooked through; rest and slice.",
            "Warm tortillas; fill with chicken, pineapple, onion and cilantro.",
            "Serve with extra lime wedges."
        ],
        "tags": ["street-food", "grill", "party"],
        "dietary": ["non-vegetarian", "gluten-free"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "guacamole",
        "title": "Classic Guacamole",
        "description": "Fresh avocado dip with lime, onion and cilantro.",
        "cuisine": "Mexican",
        "category": "snack",
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 0,
        "difficulty": "easy",
        "ingredients": [
            {"name": "ripe avocados", "quantity": 3, "unit": "piece", "grocery_category": "fruits"},
            {"name": "lime juice", "quantity": 2, "unit": "tbsp", "grocery_category": "fruits"},
            {"name": "red onion, finely diced", "quantity": 0.25, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "tomato, diced", "quantity": 1, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "cilantro, chopped", "quantity": 2, "unit": "tbsp", "grocery_category": "herbs-fresh"},
            {"name": "jalapeno, minced", "quantity": 1, "unit": "piece", "grocery_category": "vegetables", "optional": True},
            {"name": "salt", "quantity": 0.5, "unit": "tsp", "grocery_category": "spices"}
        ],
        "instructions": [
            "Mash avocados to desired texture in a bowl.",
            "Fold in lime juice, onion, tomato, cilantro and jalapeno.",
            "Season with salt and serve immediately with tortilla chips."
        ],
        "tags": ["no-cook", "quick", "party", "vegan"],
        "dietary": ["vegan", "vegetarian", "gluten-free"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "thai-green-curry",
        "title": "Thai Green Curry with Chicken",
        "description": "Aromatic, coconut-based curry with green chilies, Thai basil and vegetables.",
        "cuisine": "Thai",
        "category": "main",
        "servings": 4,
        "prep_time_minutes": 20,
        "cook_time_minutes": 25,
        "difficulty": "medium",
        "ingredients": [
            {"name": "chicken breast, sliced", "quantity": 500, "unit": "g", "grocery_category": "meat-poultry"},
            {"name": "green curry paste", "quantity": 3, "unit": "tbsp", "grocery_category": "condiments-sauces"},
            {"name": "coconut milk", "quantity": 400, "unit": "ml", "grocery_category": "canned-jarred"},
            {"name": "fish sauce", "quantity": 1, "unit": "tbsp", "grocery_category": "condiments-sauces"},
            {"name": "palm sugar", "quantity": 1, "unit": "tbsp", "grocery_category": "other"},
            {"name": "Thai eggplant or zucchini, chopped", "quantity": 150, "unit": "g", "grocery_category": "vegetables"},
            {"name": "bell pepper, sliced", "quantity": 1, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "Thai basil leaves", "quantity": 0.5, "unit": "cup", "grocery_category": "herbs-fresh"},
            {"name": "kaffir lime leaves", "quantity": 3, "unit": "piece", "grocery_category": "herbs-fresh"}
        ],
        "instructions": [
            "Fry curry paste in a splash of coconut milk until fragrant.",
            "Add chicken, cook until sealed on all sides.",
            "Pour in remaining coconut milk, fish sauce and palm sugar; simmer 10 minutes.",
            "Add vegetables and kaffir lime leaves; simmer until tender.",
            "Stir in Thai basil and serve with jasmine rice."
        ],
        "tags": ["curry", "coconut", "spicy"],
        "dietary": ["non-vegetarian", "gluten-free", "dairy-free"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "kung-pao-chicken",
        "title": "Kung Pao Chicken",
        "description": "Sichuan stir-fry with chicken, peanuts and dried chilies.",
        "cuisine": "Chinese",
        "category": "main",
        "servings": 4,
        "prep_time_minutes": 20,
        "cook_time_minutes": 15,
        "difficulty": "medium",
        "ingredients": [
            {"name": "chicken breast, diced", "quantity": 500, "unit": "g", "grocery_category": "meat-poultry"},
            {"name": "roasted peanuts", "quantity": 80, "unit": "g", "grocery_category": "nuts-seeds"},
            {"name": "dried red chilies", "quantity": 8, "unit": "piece", "grocery_category": "spices"},
            {"name": "sichuan peppercorns", "quantity": 1, "unit": "tsp", "grocery_category": "spices"},
            {"name": "soy sauce", "quantity": 2, "unit": "tbsp", "grocery_category": "condiments-sauces"},
            {"name": "black vinegar", "quantity": 1, "unit": "tbsp", "grocery_category": "condiments-sauces"},
            {"name": "garlic, minced", "quantity": 3, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "spring onion, chopped", "quantity": 3, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "cornstarch", "quantity": 1, "unit": "tbsp", "grocery_category": "flour-baking"},
            {"name": "vegetable oil", "quantity": 3, "unit": "tbsp", "grocery_category": "oils-fats"}
        ],
        "instructions": [
            "Toss chicken with cornstarch and a splash of soy sauce; marinate 10 minutes.",
            "Stir-fry dried chilies and sichuan peppercorns in hot oil until fragrant.",
            "Add chicken, stir-fry until cooked through.",
            "Add garlic, soy sauce and black vinegar; toss to coat.",
            "Stir in peanuts and spring onion; serve with steamed rice."
        ],
        "tags": ["stir-fry", "spicy", "weeknight"],
        "dietary": ["non-vegetarian", "dairy-free"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "vegetable-fried-rice",
        "title": "Vegetable Fried Rice",
        "description": "Wok-fried rice with mixed vegetables, egg and soy sauce.",
        "cuisine": "Chinese",
        "category": "main",
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 15,
        "difficulty": "easy",
        "ingredients": [
            {"name": "cooked, cooled rice", "quantity": 4, "unit": "cup", "grocery_category": "grains-rice"},
            {"name": "eggs, beaten", "quantity": 2, "unit": "piece", "grocery_category": "dairy"},
            {"name": "carrot, diced", "quantity": 1, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "peas", "quantity": 0.5, "unit": "cup", "grocery_category": "frozen"},
            {"name": "spring onion, chopped", "quantity": 3, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "soy sauce", "quantity": 3, "unit": "tbsp", "grocery_category": "condiments-sauces"},
            {"name": "sesame oil", "quantity": 1, "unit": "tsp", "grocery_category": "oils-fats"},
            {"name": "vegetable oil", "quantity": 2, "unit": "tbsp", "grocery_category": "oils-fats"}
        ],
        "instructions": [
            "Scramble eggs in a hot wok with a little oil; set aside.",
            "Stir-fry carrot and peas 2-3 minutes.",
            "Add rice, breaking up clumps, stir-fry 5 minutes until slightly crisp.",
            "Return eggs, add soy sauce and sesame oil, toss well.",
            "Garnish with spring onion and serve."
        ],
        "tags": ["quick", "leftovers", "one-pan", "budget-friendly"],
        "dietary": ["vegetarian"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "hummus",
        "title": "Classic Hummus",
        "description": "Smooth chickpea and tahini dip from the Levant.",
        "cuisine": "Middle Eastern",
        "category": "snack",
        "servings": 6,
        "prep_time_minutes": 10,
        "cook_time_minutes": 0,
        "difficulty": "easy",
        "ingredients": [
            {"name": "canned chickpeas", "quantity": 400, "unit": "g", "grocery_category": "canned-jarred"},
            {"name": "tahini", "quantity": 60, "unit": "g", "grocery_category": "condiments-sauces"},
            {"name": "lemon juice", "quantity": 3, "unit": "tbsp", "grocery_category": "fruits"},
            {"name": "garlic clove", "quantity": 1, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "olive oil", "quantity": 2, "unit": "tbsp", "grocery_category": "oils-fats"},
            {"name": "cumin powder", "quantity": 0.5, "unit": "tsp", "grocery_category": "spices"},
            {"name": "ice water", "quantity": 3, "unit": "tbsp", "grocery_category": "beverages"}
        ],
        "instructions": [
            "Blend chickpeas, tahini, lemon juice, garlic and cumin until coarse.",
            "Stream in ice water while blending until smooth and creamy.",
            "Season with salt, drizzle with olive oil and serve with pita."
        ],
        "tags": ["no-cook", "dip", "vegan", "meal-prep"],
        "dietary": ["vegan", "vegetarian", "gluten-free"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "greek-salad",
        "title": "Greek Salad (Horiatiki)",
        "description": "Rustic salad of tomato, cucumber, olives and feta.",
        "cuisine": "Greek",
        "category": "salad",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 0,
        "difficulty": "easy",
        "ingredients": [
            {"name": "tomatoes, cut into wedges", "quantity": 4, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "cucumber, sliced", "quantity": 1, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "red onion, thinly sliced", "quantity": 0.5, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "kalamata olives", "quantity": 100, "unit": "g", "grocery_category": "canned-jarred"},
            {"name": "feta cheese block", "quantity": 150, "unit": "g", "grocery_category": "dairy"},
            {"name": "extra virgin olive oil", "quantity": 3, "unit": "tbsp", "grocery_category": "oils-fats"},
            {"name": "dried oregano", "quantity": 1, "unit": "tsp", "grocery_category": "spices"}
        ],
        "instructions": [
            "Combine tomato, cucumber, onion and olives in a bowl.",
            "Top with a whole block of feta, drizzle with olive oil and sprinkle oregano.",
            "Season with salt and pepper; serve with crusty bread."
        ],
        "tags": ["no-cook", "fresh", "summer", "vegetarian"],
        "dietary": ["vegetarian", "gluten-free"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "chicken-teriyaki",
        "title": "Chicken Teriyaki",
        "description": "Pan-glazed chicken thighs in a sweet-savory soy sauce glaze.",
        "cuisine": "Japanese",
        "category": "main",
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 20,
        "difficulty": "easy",
        "ingredients": [
            {"name": "chicken thighs, skin-on", "quantity": 600, "unit": "g", "grocery_category": "meat-poultry"},
            {"name": "soy sauce", "quantity": 60, "unit": "ml", "grocery_category": "condiments-sauces"},
            {"name": "mirin", "quantity": 60, "unit": "ml", "grocery_category": "condiments-sauces"},
            {"name": "sake", "quantity": 30, "unit": "ml", "grocery_category": "beverages", "optional": True},
            {"name": "sugar", "quantity": 1, "unit": "tbsp", "grocery_category": "other"},
            {"name": "ginger, grated", "quantity": 1, "unit": "tsp", "grocery_category": "vegetables"},
            {"name": "sesame seeds", "quantity": 1, "unit": "tsp", "grocery_category": "nuts-seeds", "optional": True}
        ],
        "instructions": [
            "Sear chicken thighs skin-side down until crisp; flip and cook through.",
            "Whisk soy sauce, mirin, sake, sugar and ginger together.",
            "Pour sauce into the pan, simmer until it reduces to a glaze coating the chicken.",
            "Slice, sprinkle with sesame seeds, and serve with steamed rice."
        ],
        "tags": ["glazed", "weeknight", "umami"],
        "dietary": ["non-vegetarian", "dairy-free"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "miso-soup",
        "title": "Miso Soup",
        "description": "Light Japanese soup with dashi, miso, tofu and seaweed.",
        "cuisine": "Japanese",
        "category": "soup",
        "servings": 4,
        "prep_time_minutes": 5,
        "cook_time_minutes": 10,
        "difficulty": "easy",
        "ingredients": [
            {"name": "dashi stock", "quantity": 1, "unit": "l", "grocery_category": "beverages"},
            {"name": "miso paste", "quantity": 3, "unit": "tbsp", "grocery_category": "condiments-sauces"},
            {"name": "silken tofu, cubed", "quantity": 200, "unit": "g", "grocery_category": "other"},
            {"name": "dried wakame seaweed", "quantity": 1, "unit": "tbsp", "grocery_category": "other"},
            {"name": "spring onion, sliced", "quantity": 2, "unit": "piece", "grocery_category": "vegetables"}
        ],
        "instructions": [
            "Bring dashi to a gentle simmer (do not boil).",
            "Whisk a ladle of hot dashi with miso paste until dissolved, then stir back into the pot.",
            "Add tofu and rehydrated wakame, warm through.",
            "Garnish with spring onion and serve immediately."
        ],
        "tags": ["light", "quick", "comfort"],
        "dietary": ["vegetarian", "dairy-free"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "classic-beef-burger",
        "title": "Classic Beef Burger",
        "description": "Juicy diner-style beef burger with cheese and all the fixings.",
        "cuisine": "American",
        "category": "main",
        "servings": 4,
        "prep_time_minutes": 15,
        "cook_time_minutes": 10,
        "difficulty": "easy",
        "ingredients": [
            {"name": "ground beef (80/20)", "quantity": 600, "unit": "g", "grocery_category": "meat-poultry"},
            {"name": "burger buns", "quantity": 4, "unit": "piece", "grocery_category": "bakery"},
            {"name": "cheddar cheese slices", "quantity": 4, "unit": "piece", "grocery_category": "dairy"},
            {"name": "lettuce leaves", "quantity": 4, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "tomato, sliced", "quantity": 1, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "red onion, sliced", "quantity": 0.5, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "pickles", "quantity": 8, "unit": "piece", "grocery_category": "canned-jarred"},
            {"name": "ketchup", "quantity": 2, "unit": "tbsp", "grocery_category": "condiments-sauces"},
            {"name": "mustard", "quantity": 1, "unit": "tbsp", "grocery_category": "condiments-sauces"}
        ],
        "instructions": [
            "Divide beef into 4 patties, season generously with salt and pepper.",
            "Sear on a hot pan or grill 3-4 minutes per side, adding cheese in the last minute.",
            "Toast the buns lightly.",
            "Assemble with lettuce, tomato, onion, pickles, ketchup and mustard."
        ],
        "tags": ["grill", "weekend", "crowd-pleaser"],
        "dietary": ["non-vegetarian"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "buttermilk-pancakes",
        "title": "Fluffy Buttermilk Pancakes",
        "description": "Classic breakfast pancakes, light and fluffy.",
        "cuisine": "American",
        "category": "breakfast",
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 15,
        "difficulty": "easy",
        "ingredients": [
            {"name": "all-purpose flour", "quantity": 250, "unit": "g", "grocery_category": "flour-baking"},
            {"name": "baking powder", "quantity": 2, "unit": "tsp", "grocery_category": "flour-baking"},
            {"name": "baking soda", "quantity": 0.5, "unit": "tsp", "grocery_category": "flour-baking"},
            {"name": "sugar", "quantity": 2, "unit": "tbsp", "grocery_category": "other"},
            {"name": "buttermilk", "quantity": 400, "unit": "ml", "grocery_category": "dairy"},
            {"name": "eggs", "quantity": 2, "unit": "piece", "grocery_category": "dairy"},
            {"name": "butter, melted", "quantity": 40, "unit": "g", "grocery_category": "dairy"},
            {"name": "maple syrup", "quantity": 60, "unit": "ml", "grocery_category": "condiments-sauces", "optional": True}
        ],
        "instructions": [
            "Whisk dry ingredients together in a bowl.",
            "In another bowl, whisk buttermilk, eggs and melted butter.",
            "Combine wet and dry ingredients, mixing just until no dry streaks remain (lumps are fine).",
            "Cook 1/4-cup portions on a buttered griddle until bubbles form, flip and cook through.",
            "Serve stacked with maple syrup and butter."
        ],
        "tags": ["breakfast", "weekend", "kid-friendly"],
        "dietary": ["vegetarian"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "falafel",
        "title": "Crispy Baked Falafel",
        "description": "Herb-packed chickpea fritters, oven-baked for a lighter finish.",
        "cuisine": "Middle Eastern",
        "category": "main",
        "servings": 4,
        "prep_time_minutes": 20,
        "cook_time_minutes": 25,
        "difficulty": "medium",
        "ingredients": [
            {"name": "dried chickpeas, soaked overnight", "quantity": 250, "unit": "g", "grocery_category": "lentils-pulses"},
            {"name": "parsley", "quantity": 1, "unit": "cup", "grocery_category": "herbs-fresh"},
            {"name": "cilantro", "quantity": 0.5, "unit": "cup", "grocery_category": "herbs-fresh"},
            {"name": "onion, roughly chopped", "quantity": 0.5, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "garlic cloves", "quantity": 4, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "cumin powder", "quantity": 1, "unit": "tsp", "grocery_category": "spices"},
            {"name": "coriander powder", "quantity": 1, "unit": "tsp", "grocery_category": "spices"},
            {"name": "baking powder", "quantity": 1, "unit": "tsp", "grocery_category": "flour-baking"},
            {"name": "olive oil", "quantity": 2, "unit": "tbsp", "grocery_category": "oils-fats"}
        ],
        "instructions": [
            "Note: use dried, soaked (not canned) chickpeas for proper texture.",
            "Pulse chickpeas, herbs, onion, garlic and spices in a food processor until finely ground but not pureed.",
            "Mix in baking powder, chill mixture 30 minutes.",
            "Shape into small patties, brush with olive oil.",
            "Bake at 200C for 12-14 minutes per side until golden and crisp.",
            "Serve in pita with tahini sauce and salad."
        ],
        "tags": ["vegan", "meal-prep", "baked"],
        "dietary": ["vegan", "vegetarian"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "ratatouille",
        "title": "Ratatouille",
        "description": "Provencal stewed vegetable dish of eggplant, zucchini, pepper and tomato.",
        "cuisine": "French",
        "category": "side",
        "servings": 4,
        "prep_time_minutes": 20,
        "cook_time_minutes": 40,
        "difficulty": "medium",
        "ingredients": [
            {"name": "eggplant, diced", "quantity": 1, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "zucchini, diced", "quantity": 2, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "bell peppers, diced", "quantity": 2, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "tomatoes, chopped", "quantity": 4, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "onion, chopped", "quantity": 1, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "garlic cloves, minced", "quantity": 3, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "herbes de Provence", "quantity": 1, "unit": "tsp", "grocery_category": "spices"},
            {"name": "olive oil", "quantity": 4, "unit": "tbsp", "grocery_category": "oils-fats"}
        ],
        "instructions": [
            "Saute onion and garlic in olive oil until soft.",
            "Add eggplant, cook 5 minutes, then add peppers and zucchini.",
            "Stir in tomatoes and herbes de Provence.",
            "Cover and simmer 25-30 minutes, stirring occasionally, until vegetables are tender and stew-like.",
            "Season and serve warm or at room temperature."
        ],
        "tags": ["vegan", "make-ahead", "summer"],
        "dietary": ["vegan", "vegetarian", "gluten-free"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    },
    {
        "id": "bibimbap",
        "title": "Bibimbap (Mixed Rice Bowl)",
        "description": "Korean rice bowl topped with seasoned vegetables, beef and a fried egg.",
        "cuisine": "Korean",
        "category": "main",
        "servings": 4,
        "prep_time_minutes": 30,
        "cook_time_minutes": 20,
        "difficulty": "medium",
        "ingredients": [
            {"name": "cooked short-grain rice", "quantity": 4, "unit": "cup", "grocery_category": "grains-rice"},
            {"name": "beef sirloin, thinly sliced", "quantity": 300, "unit": "g", "grocery_category": "meat-poultry"},
            {"name": "spinach", "quantity": 150, "unit": "g", "grocery_category": "vegetables"},
            {"name": "bean sprouts", "quantity": 150, "unit": "g", "grocery_category": "vegetables"},
            {"name": "carrot, julienned", "quantity": 1, "unit": "piece", "grocery_category": "vegetables"},
            {"name": "shiitake mushrooms, sliced", "quantity": 100, "unit": "g", "grocery_category": "vegetables"},
            {"name": "eggs", "quantity": 4, "unit": "piece", "grocery_category": "dairy"},
            {"name": "gochujang (Korean chili paste)", "quantity": 3, "unit": "tbsp", "grocery_category": "condiments-sauces"},
            {"name": "sesame oil", "quantity": 2, "unit": "tbsp", "grocery_category": "oils-fats"},
            {"name": "soy sauce", "quantity": 2, "unit": "tbsp", "grocery_category": "condiments-sauces"}
        ],
        "instructions": [
            "Marinate beef in soy sauce and a little sesame oil; stir-fry until browned.",
            "Blanch spinach and bean sprouts separately; season each with sesame oil and salt.",
            "Saute carrot and mushrooms separately until just tender.",
            "Fry eggs sunny-side up.",
            "Assemble rice in bowls, arrange beef and vegetables in sections, top with a fried egg.",
            "Serve with gochujang on the side to mix in."
        ],
        "tags": ["rice-bowl", "meal-prep", "customizable"],
        "dietary": ["non-vegetarian"],
        "source": "ai-generated",
        "generated_by": "claude-sonnet-5"
    }
]


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    recipes_dir = os.path.join(base_dir, "data", "recipes")
    os.makedirs(recipes_dir, exist_ok=True)

    written = []
    for recipe in RECIPES:
        path = os.path.join(recipes_dir, f"{recipe['id']}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(recipe, f, indent=2, ensure_ascii=False)
            f.write("\n")
        written.append(recipe["id"])

    # Build a lightweight index for fast search without reading every file.
    index = [
        {
            "id": r["id"],
            "title": r["title"],
            "cuisine": r["cuisine"],
            "category": r["category"],
            "tags": r["tags"],
            "dietary": r["dietary"],
            "ingredient_names": [ing["name"] for ing in r["ingredients"]],
        }
        for r in RECIPES
    ]
    index_path = os.path.join(base_dir, "data", "index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote {len(written)} recipes to {recipes_dir}")
    print(f"Wrote index ({len(index)} entries) to {index_path}")


if __name__ == "__main__":
    main()
