# Oppidu Recipes

An AI-generated recipe database, built as a standalone project for now with
a clear path to plugging into [Oppidu](https://oppidu.de)'s search: Oppidu's
"paste a recipe → compare grocery prices" flow can check this database
*first*, and only reach for external sources when nothing local matches.

## What's here

```
recipe-creator/
├── schema/recipe.schema.json   # the recipe data contract
├── data/
│   ├── recipes/*.json          # one file per recipe (the "database")
│   ├── index.json              # lightweight search index, generated from data/recipes/
│   └── ingredients.json        # per-ingredient reference (unit, grocery category, qty/serving)
├── scripts/
│   ├── seed_recipes.py         # (re)writes the 19 seed recipes into data/recipes/
│   ├── search.py               # local search engine + external-fallback hook
│   ├── generate_recipe.py      # add new recipes (via LLM call, or from a JSON file)
│   ├── ingredients_db.py       # builds data/ingredients.json; autocomplete + quantity suggestion
│   ├── nutrition_data.py       # curated per-100g macros + unit/piece-weight conversion tables
│   ├── nutrition.py            # estimates calories/fat/carbs/protein per serving from ingredients
│   ├── submit_recipe.py        # the recipe-submission workflow (servings → ingredients → steps)
│   └── validate.py             # schema-validates every recipe + checks index sync
├── tests/
│   ├── test_search.py          # sanity tests for search.py
│   ├── test_nutrition.py       # sanity tests for nutrition.py, incl. full-coverage check on seed data
│   └── test_submit_recipe.py   # sanity tests for ingredients_db.py + submit_recipe.py
├── preview.html                # the published artifact — Browse + Submit-a-Recipe prototype
└── requirements.txt
```

## Why this structure

**Recipes are individual JSON files, not one big database file.** Each
recipe is independently readable, diffable, and easy to hand-edit or drop
in from elsewhere. `data/index.json` is a derived, lightweight summary
(title/cuisine/tags/ingredients) that `search.py` reads instead of opening
all 19+ files on every query — regenerate it any time with
`seed_recipes.py` or `generate_recipe.py` (which updates it automatically
when adding one recipe at a time).

**Every ingredient carries a `grocery_category`** (spices, vegetables,
dairy, lentils-pulses, etc.) — see `schema/recipe.schema.json`. This is the
field a future Oppidu integration will use to map a recipe's ingredient
list onto a grocery store's product catalog for price comparison, without
having to re-derive it from free-text ingredient names.

**Search is local-first, external-fallback by design.** `find_recipe()` in
`scripts/search.py` is the single entry point: it scores matches against
the local database, and only calls `search_external()` (currently a
documented stub) when the local result is weak or empty. That's the same
shape Oppidu's own search should have when this gets wired in — swap the
stub for a real recipe API or an LLM generation call, nothing else needs
to change.

## Submitting a recipe

A user can walk through submitting their own recipe — both as a clickable
prototype (open `preview.html`, tab to "Submit a Recipe") and as a Python
workflow (`scripts/submit_recipe.py`) that produces the same schema-valid
record. The flow, in order:

1. **Servings, first.** Everything downstream scales off this number.
2. **Basics** — an optional **kitchen name** (e.g. "Nina's Kitchen" —
   `submitted_kitchen` in the schema), title, description, cuisine,
   category, difficulty, times, dietary tags. Typing the dish name
   auto-suggests a **cuisine** (`suggestCuisine()`: a curated dish-keyword
   dictionary merged with a live frequency table built from the current
   recipe pool, so "Chicken Tikka Masala" guesses Indian without the user
   typing it) — it only fills the field while the user hasn't touched it
   themselves, and a small hint explains it's a guess. **Tags** get a row
   of the most-used tags across the current recipe pool
   (`computePopularTags()`) as one-click chips, kept in sync with the
   free-text field in both directions. The kitchen name is remembered
   per-browser (`localStorage`, `recipe-creator:lastKitchen:v1`) and
   prefilled next time, since one person's submissions usually share it.
3. **Ingredients**, with autocomplete and quantity suggestions, grouped on
   screen by grocery category — each group heading carries an emoji
   (poultry & meat 🍗, dairy 🧀, fresh vegetables 🥦, spices 🌶️, etc. — see
   `GROCERY_CATEGORY_ORDER` / `CATEGORY_EMOJI` in `preview_template.html`)
   so a long list stays scannable, and each ingredient row shows its own
   closer-to-specific emoji where one is known (`INGREDIENT_EMOJI`,
   falling back to the category's). Each added ingredient gets an **Edit**
   button (ahead of Remove) that reloads it into the add-row for editing in
   place, rather than remove-and-re-add, plus an **Optional** checkbox
   (unchecked — mandatory — by default) that shows as an "(optional)" note
   throughout. Typing a prep descriptor into the name field ("tomato,
   diced") is caught and split apart: the ingredient is stored as the
   plain name ("tomato") — matching how a shopping list actually reads —
   and the descriptor is carried forward as a ready-made step suggestion
   in step 5 (`stripDescriptor()` / `phraseFromDescriptor()`), with an
   inline confirmation note showing what happened. `scripts/ingredients_db.py`
   aggregates every ingredient across `data/recipes/*.json` into a typical
   unit + quantity-per-serving, so typing "chicken breast" with servings=4
   suggests "500 g" — scaled from whatever the seed database shows a
   similar dish using per person. This is a *starting point*, not a rule:
   with only 19 seed recipes some suggestions will be rough (a single
   garlic-heavy pasta recipe currently pulls the "garlic" suggestion higher
   than most dishes would want), and it gets better as more recipes go in.
   Any ingredient not yet in the reference database just asks the user for
   a quantity directly.
4. **Ingredients photo** — where a mise-en-place shot (all ingredients
   measured into bowls/plates) would be generated. See "Photos" below.
5. **Method**, laid out as two columns. On the left, quick-insert step
   phrases — in order: **your own saved phrases** (free text you've
   submitted before, on any recipe, remembered per-browser via
   `localStorage`'s `recipe-creator:savedSteps:v1` so repeat wording is one
   click instead of a retype), phrases **from your ingredients** (the prep
   descriptors caught back in step 3 — never offered for something that
   was never given one, so a plain "vegetable oil" entry never gets a
   nonsensical "slice the vegetable oil" suggestion), then the generic
   groups grouped by technique (knife work / heat / assembly). Every chip
   is free text, an **Edit** button (ahead of Remove) sits on every step,
   and ↑/↓ reorder arrows let a forgotten step be added at the end and
   moved into place rather than requiring a rebuild of the list. A step
   whose text contains a keyword like "roast", "sear", "fry", "grill", or
   "temper" (or the German equivalents when the page is in German) is
   auto-flagged as a **key step** worth its own photo — the user can
   untick or tick this manually. On the right: a live sidebar listing
   every ingredient from step 3, grouped by category (with its emoji too),
   with a filled dot once an ingredient's name turns up in the steps typed
   so far, a running note when some aren't mentioned yet, a remove button
   per ingredient, and a category-aware **prep-technique picker** (produce
   gets chop/dice/slice/julienne/mince/grate/peel, with size options like
   "dice → small" vs. "dice → large"; meat gets dice/slice/mince/
   butterfly/pound/trim; dairy gets grate/slice/cube/crumble/melt;
   everything else — spices, oils, condiments — gets toast/grind/soak/
   measure, which is what actually keeps "slice the vegetable oil" from
   ever being offered: the bucket an ingredient's grocery category maps to
   decides which verbs are even on the list — see `PREP_TECHNIQUES` /
   `techniqueGroupFor()` in `preview_template.html`) that inserts a
   ready-made instruction phrase into the step text box for the user to
   add, tweak, or ignore.
6. **Review & submit** — shows the exact record a submission would
   produce, including a banner explaining that sign-in isn't built yet, so
   nothing here actually publishes, and — if any ingredient never turned
   up in a step — a second banner naming exactly which ones, so nothing
   gets forgotten right before saving. A "Copy recipe JSON" button and a
   visible `<pre>` block let the user grab the output directly. Right
   above the ingredient list sits a **Nutrition (estimated)** block — see
   "Nutrition estimate" below — and it appears the same way on every
   recipe's Browse detail view, not just here.

## Nutrition estimate

Every recipe — seed, saved, or still being drafted in the wizard — shows
an estimated **calories / fat / carbs / protein per serving**, computed
live from its ingredient list. This is deliberately an offline, estimated
figure rather than a call to a nutrition API (see "Ingredients" above for
the same "no third-party dependency" preference and the general project
design principle):

- `scripts/nutrition_data.py` hand-curates per-100g macros for every
  ingredient in `data/ingredients.json`, plus a unit→grams table (`g`,
  `tbsp`, `cup`, …) and an average-weight table for ingredients measured
  in `piece`s (a "piece" of garlic and a "piece" of cauliflower obviously
  aren't the same mass). Growing this alongside `ingredients_db.py`'s own
  database keeps the two in step — see that file's docstring for how to
  add an entry.
- `scripts/nutrition.py`'s `estimate_recipe_nutrition()` converts every
  ingredient's quantity+unit to grams, scales that ingredient's per-100g
  macros, sums across the recipe, then divides by servings. An ingredient
  with no reference entry (or measured "to taste", which has no sensible
  gram conversion) is silently excluded rather than guessed at — the
  result's `ingredients_covered` / `ingredients_total` says how much of
  the recipe the number actually accounts for, and a partial estimate
  says so on screen ("Based on 7/8 ingredients…") instead of presenting
  itself as complete. Try it directly: `python3 scripts/nutrition.py
  butter-chicken`.
- `preview_template.html`'s `estimateRecipeNutrition()` is a hand-kept JS
  mirror of that same function — the same relationship `suggestQuantity()`
  already has with `ingredients_db.py`'s `suggest_quantity()`. Only the
  *calculation* is duplicated: the actual numbers (`NUTRITION_DATA`) are
  authored once in `nutrition_data.py` and bundled into `preview.html` by
  `build_preview.py`, the same way `data/ingredients.json` already is.
- However precisely-curated the per-100g figures are, this is still an
  **estimate** — every place it's shown says so, right next to the
  numbers, on purpose. A future upgrade path exists if more precision is
  wanted later: swap the hand-curated table for a live nutrition API call
  (USDA FoodData Central, Edamam) behind the same `estimate_recipe_nutrition()`
  signature — nothing calling it needs to change.

## Importing a recipe from a PDF

Step 1 of the submission wizard (`preview.html`) has an alternative to typing
a recipe in by hand: **"Upload a PDF instead."** It's a browser-only
feature — nothing is uploaded to a server, the file is read and parsed
entirely client-side, and there's no matching Python entry point (unlike the
wizard itself, which has both a browser and a `scripts/submit_recipe.py`
version).

**Scope, on purpose.** This reads **typed or exported PDFs only** — a page
printed from a website, or exported from Word/Google Docs/a recipe app —
anything with a real, selectable text layer. It does **not** do OCR, so a
scanned photo of a cookbook page won't work; the importer detects that case
(almost no extractable text) and says so plainly rather than guessing at
garbage.

How it works:

1. **Extraction** — [pdf.js](https://mozilla.github.io/pdf.js/) is loaded
   lazily from cdnjs (only once someone actually picks a file) and reads the
   text layer, reconstructing line breaks from each text item's position on
   the page (pdf.js's own text extraction returns a flat bag of positioned
   fragments, not lines).
2. **Heuristic parsing** — plain regex/keyword rules look for an
   "Ingredients" heading and an "Instructions"/"Method"/"Directions" heading,
   a leading quantity + unit on each ingredient line (handles fractions like
   "1 1/2" and "½", ranges like "1-2", and common unit words/abbreviations),
   a leading number or bullet on each step, and `Servings:` / `Prep time:` /
   `Cook time:` lines anywhere in the text. The first line is taken as the
   title; the lines between the title and the ingredients list (minus any
   metadata lines) become the description.
3. **Straight into the normal wizard** — a successful import fills in
   servings, title, description, prep/cook time, ingredients (each one
   looked up against `data/ingredients.json` the same way a manually-typed
   ingredient is, for its grocery category and a fallback unit), and steps
   (run through the same key-step keyword detection as a hand-typed step),
   then drops the user on step 2 with a dismissible banner reminding them
   this is a best-effort reading. Every field is then just wizard state —
   editable through the exact same Edit buttons, category grouping, sidebar,
   and reorder arrows as a recipe typed in by hand, and saved the same way
   via the "Save recipe" button.

Recipe PDFs vary enormously in layout, so this is deliberately best-effort
rather than something that tries to be clever about every possible format —
the same "honest, clearly-labeled, no faking it" approach as the photo
placeholders below. A PDF with an unusual layout might land with a mangled
description or a missed ingredient; the point is that reviewing and fixing
that through the existing wizard steps is fast, not that the first pass has
to be perfect.

Errors are surfaced inline on step 1: choosing a non-PDF file, a PDF over
20 MB, a PDF pdf.js can't parse at all, or a PDF with no extractable text
layer (the scanned-photo case) each show a specific message and leave the
wizard on step 1, untouched.

## Accounts + a shared database (Supabase)

`preview_template.html` now has full Supabase wiring — sign-up/sign-in,
row-level security, and a real shared `recipes` table — but it ships with
`SUPABASE_URL`/`SUPABASE_ANON_KEY` left blank, which keeps it in
**local-only mode**: every submission still just goes to that one
browser's `localStorage` via `RecipeStore` (`list()`/`save()`/`remove()`),
same as before, until a project is actually wired in.

**To go live with real, shared accounts**, see
[`supabase/README.md`](supabase/README.md) — create a Supabase project,
run [`supabase/schema.sql`](supabase/schema.sql), drop the URL + anon key
into those two constants, and rebuild. From that point on:

- Anyone can sign up and submit — `RecipeStore` talks to Supabase instead
  of `localStorage`, so a submission is visible to every visitor, not just
  the browser that made it. `submitted_by` becomes a real user id instead
  of always `null`.
- A slug collision (two different people naming a dish the same thing) is
  now a genuine race, not just a same-browser repeat — `RecipeStore.save()`
  retries against the database's own unique-constraint error rather than
  trusting a client-side guess alone.
- Signing in gates the submission wizard (Browse stays open to everyone,
  signed in or not); an admin (a role granted via one SQL statement — see
  the linked README) gets a **Delete recipe** button on any recipe, not
  just their own, for moderation.

**In `scripts/submit_recipe.py`**, the equivalent is still
`save_submission(draft)` (and `list_submissions()` to read them back),
writing to `data/submissions/<id>.json` — deliberately separate from the
curated `data/recipes/` seed set, and not yet wired to Supabase itself
(only the browser wizard is, for now). Like the browser wizard, saving is
opt-in: it's not called automatically inside `finalize()`.

## English / German

`preview.html` has an EN/DE toggle in the header (`setLanguage()` in the
script). It translates two independent things: all interface chrome (the
`STR` dictionary + `t()`/`tf()` helpers, and display-label maps for
category/dietary/difficulty/grocery-category/cuisine that translate what's
*shown* while leaving the underlying English enum values — and therefore
schema validity — untouched), and recipe content, via an optional
`translations.de` block on a recipe (`title`, `description`,
`ingredient_names[]` and `instructions[]`, positionally aligned with the
English arrays) that the `locTitle()`/`locDescription()`/
`locIngredientName()`/`locInstructions()` helpers read when in German mode
and fall back to English for anything a translation omits. All 19 seed
recipes carry a German translation today. A submission built in the wizard
is always shown back in whatever language the person typed it in — the
chrome around the wizard translates, but nothing auto-translates a user's
own text — so a recipe added later needs its own `translations.de` written
by hand (or, eventually, machine-translated) if it should appear in German
too.

Both a recipe's detail view (Browse tab) and the review step above carry a
small action row: **Download** (a plain-text recipe card), **Print**
(browser print, scoped to just the recipe so app chrome doesn't print —
also how most browsers offer "Save as PDF"), and **Compare & buy
ingredients**, which is intentionally just a button for now — see "Not yet
wired up" below.

**Accounts exist in code, pending real credentials** — see "Accounts + a
shared database" above. Until `SUPABASE_URL`/`SUPABASE_ANON_KEY` are
filled in, every submission still carries `submitted_by: null` and comes
out with `status: "submitted"` rather than `"published"` (there's no
review/approval step yet — a Supabase-backed submission is visible the
moment it's saved). See the optional fields in `schema/recipe.schema.json`.
The optional `submitted_kitchen` field (e.g. "Nina's Kitchen") stays
useful even with real accounts — a user id groups recipes by *account*,
`submitted_kitchen` groups them by a *name the person chose*, and the two
coexist (someone might run more than one named kitchen under one account).

**Photos are intentionally not built.** No image-generation API is wired
up. What *is* built is the bookkeeping: `photos_needed` on a finalized
submission lists exactly which shots it would need — `"ingredients"`, one
`"step-<n>"` per key step, and `"final"` — and both `preview.html` and
`submit_recipe.py` mark these as plain, honest placeholders (never a faked
photo). To wire up real generation later: implement a function that takes
a `photos_needed` entry plus the relevant recipe context, calls an image
API (e.g. one that takes a text prompt — the ingredient list and dish
title are enough to construct one), and stores the result's URL. The
natural place for it is alongside `generate_recipe.py`, following the same
"documented, ready-to-wire" pattern used there for text generation.

## Not yet wired up

**"Compare & buy ingredients"** appears on every recipe (Browse detail and
the submission review step) but only shows a "coming soon" note — this is
the Oppidu hook: once wired, its click should take a recipe's ingredient
list (each already tagged with a `grocery_category`, see below) and open
Oppidu's price comparison for exactly those items.

**Download** uses the artifact platform's `downloads` capability when the
page is running as a published Claude artifact (the viewer's sandbox
otherwise silently blocks a page's own file saves), and falls back to a
normal browser download when running standalone — e.g. `preview.html`
opened directly from this project, or once this becomes a real page inside
Oppidu.

**OCR for scanned recipe PDFs** — the PDF importer (see "Importing a recipe
from a PDF" above) only reads a PDF's existing text layer; a scanned photo
of a printed page has no text layer to read, so it's out of scope for now.
Adding OCR later would mean running a scanned page's image through a
text-recognition step before the same heuristic parser can take over.

## Quickstart

```bash
pip install -r requirements.txt

# Validate the database
python3 scripts/validate.py

# Search it
python3 scripts/search.py "spicy chicken curry" --cuisine Indian
python3 scripts/search.py "chickpea curry" --full   # print the full top match

# Add a recipe you already have as JSON
python3 scripts/generate_recipe.py --from-file my_new_recipe.json

# Add a recipe via the Claude API (needs `pip install anthropic` + ANTHROPIC_API_KEY)
python3 scripts/generate_recipe.py --llm "a quick vegan weeknight lentil soup"

# Build/refresh the ingredient reference database (autocomplete + quantity suggestions)
python3 scripts/ingredients_db.py

# Estimate calories/fat/carbs/protein per serving for a recipe
python3 scripts/nutrition.py butter-chicken

# Try the submission workflow end to end (prints a demo submission as JSON)
python3 scripts/submit_recipe.py

# Run the test suite
python3 -m pytest tests/ -v   # or: python3 tests/test_search.py tests/test_submit_recipe.py
```

## Current seed database

19 recipes AI-generated as the initial seed set, spanning Indian, Italian,
Mexican, Thai, Chinese, Middle Eastern, Greek, Japanese, American, French
and Korean cuisines, across breakfast/main/side/soup/salad/snack
categories, with vegan/vegetarian/gluten-free/dairy-free tagging throughout.

## Growing the database

Two ways to add recipes without touching the code:

1. Ask Claude (in this workspace or in chat) to write a new recipe as JSON
   matching `schema/recipe.schema.json`, save it, then run
   `python3 scripts/generate_recipe.py --from-file <path>` to validate and
   index it.
2. Once you have your own `ANTHROPIC_API_KEY`, use
   `scripts/generate_recipe.py --llm "<what you want>"` to generate and
   index a recipe in one step.

Either way, always finish with `python3 scripts/validate.py` before
treating new entries as part of the database.

## Path to Oppidu integration

This is intentionally decoupled from Oppidu's codebase for now. When
you're ready to wire it in:

1. Copy (or `pip install -e`) this project alongside/into the Oppidu
   backend, or expose `find_recipe()` as an internal API endpoint.
2. Point Oppidu's "paste a recipe" flow at `find_recipe(query)` instead of
   (or before) whatever it currently uses to interpret pasted recipes.
3. Implement `search_external()` in `scripts/search.py` for the queries
   the local database can't answer — a recipe API, or an on-demand LLM
   generation call — and optionally have it *save* what it finds back into
   `data/recipes/` so the local database grows from real usage.
4. Use each ingredient's `grocery_category` to narrow which of Oppidu's
   store catalog sections to price-match against, before falling back to
   full-catalog fuzzy matching on the ingredient name.
5. Once Oppidu has real user accounts, point `submit_recipe.py`'s
   `submitted_by` at the logged-in user id, add an approval/review step
   that flips `status` from `"submitted"` to `"published"`, and wire in
   image generation for the `photos_needed` list (see "Submitting a
   recipe" above) so published recipes come with real photos.
