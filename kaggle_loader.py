import csv
import re
from recipe import Recipe
from recipe_database import RecipeDatabase


# -----------------------------
# TIME PARSING
# -----------------------------
def parse_time_to_minutes(time_str):
    if not time_str:
        return 0

    time_str = time_str.lower()

    hours = 0
    minutes = 0

    hr_match = re.search(r"(\d+)\s*hr", time_str)
    min_match = re.search(r"(\d+)\s*min", time_str)

    if hr_match:
        hours = int(hr_match.group(1))
    if min_match:
        minutes = int(min_match.group(1))

    return hours * 60 + minutes


# -----------------------------
# INGREDIENT CLEANING
# -----------------------------
def clean_ingredient(text):
    if not text:
        return ""

    text = text.lower().strip()

    # unicode fractions
    text = text.replace("½", "0.5").replace("¼", "0.25").replace("¾", "0.75")

    # remove parentheses content
    text = re.sub(r"\(.*?\)", "", text)

    # remove leading quantities (fractions, decimals, ints)
    text = re.sub(r"^\s*\d+(\.\d+)?\s*", "", text)
    text = re.sub(r"^\s*\d+\s*/\s*\d+\s*", "", text)

    # remove common units
    text = re.sub(
        r"\b(cup|cups|tbsp|tsp|tablespoons?|teaspoons?|oz|ounce|ounces|pound|pounds|lb|lbs|slice|slices|clove|cloves)\b",
        "",
        text,
    )

    # remove noisy adjectives
    text = re.sub(
        r"\b(fresh|ripe|large|small|medium|chopped|diced|sliced|peeled|crushed|minced|optional)\b",
        "",
        text,
    )

    # remove extra punctuation
    text = re.sub(r"[^a-z\s]", "", text)

    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def parse_ingredients(ingredients_str):
    if not ingredients_str:
        return []

    # split on commas (works for your dataset format)
    items = ingredients_str.split(",")

    cleaned = [clean_ingredient(i) for i in items]
    return [c for c in cleaned if c]


# -----------------------------
# DIRECTIONS CLEANING
# -----------------------------
def clean_directions(text):
    if not text:
        return ""

    text = text.strip()

    # remove extra whitespace/newlines
    text = re.sub(r"\s+", " ", text)

    return text


# -----------------------------
# MAIN LOADER
# -----------------------------
def load_recipes_from_csv(file_path):
    db = RecipeDatabase()

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print("Columns:", reader.fieldnames)

        for i, row in enumerate(reader):
            try:
                # -----------------------------
                # ID
                # -----------------------------
                recipe_id = int(row.get("Row", i))

                # -----------------------------
                # NAME
                # -----------------------------
                name = (row.get("recipe_name") or "").strip()
                if not name:
                    continue

                # -----------------------------
                # TIME (prefer total_time)
                # -----------------------------
                time_str = (
                    row.get("total_time")
                    or row.get("cook_time")
                    or row.get("prep_time")
                    or ""
                )
                cook_time = parse_time_to_minutes(time_str)

                # -----------------------------
                # INGREDIENTS
                # -----------------------------
                ingredients = parse_ingredients(row.get("ingredients", ""))
                if not ingredients:
                    continue

                # -----------------------------
                # DIRECTIONS
                # -----------------------------
                instructions = clean_directions(row.get("directions", ""))

                # -----------------------------
                # CREATE RECIPE
                # -----------------------------
                recipe = Recipe(
                    recipe_id=recipe_id,
                    name=name,
                    ingredients=ingredients,
                    cook_time=cook_time,
                    category=None,
                    instructions=instructions,
                    source="AllRecipes",
                )

                db.add_recipe(recipe)

            except Exception as e:
                print(f"Skipping row {i}: {e}")

    print("Loaded recipes:", len(db))
    return db
