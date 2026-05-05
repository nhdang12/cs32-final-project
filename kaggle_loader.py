import csv
import re
from recipe import Recipe
from recipe_database import RecipeDatabase


# Time Parsing
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


# Cleaning ingredients
def clean_ingredient(text):
    if not text:
        return ""

    text = text.lower().strip()

    text = text.replace("½", "0.5").replace("¼", "0.25").replace("¾", "0.75")
    text = text.replace("-", " ")

    text = re.sub(r"\(.*?\)", "", text)

    # remove phrases that are not real ingredients
    text = re.sub(r"\bor as needed\b", "", text)
    text = re.sub(r"\bto taste\b", "", text)
    text = re.sub(r"\bas needed\b", "", text)

    # remove leading quantities
    text = re.sub(r"^\s*\d+(\.\d+)?\s*", "", text)
    text = re.sub(r"^\s*\d+\s*/\s*\d+\s*", "", text)

    # remove common units
    text = re.sub(
        r"\b(cup|cups|tbsp|tsp|tablespoons?|teaspoons?|oz|ounce|ounces|quart|pound|pounds|lb|lbs|slice|slices|clove|cloves|can|cans|package|packages|jar|jars)\b",
        "",
        text,
    )

    # remove descriptive words
    text = re.sub(
        r"\b(fresh|ripe|large|small|medium|chopped|diced|sliced|peeled|crushed|minced|optional|skinless|boneless|low sodium|lowsodium|extra virgin)\b",
        "",
        text,
    )

    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def parse_ingredients(ingredients_str):
    if not ingredients_str:
        return []

    items = ingredients_str.split(",")

    cleaned = []
    ignore_words = {
        "",
        "or as needed",
        "as needed",
        "to taste",
        "skinless",
        "boneless",
        "water", 
        "juiced",
        "divided",
        "thinly",
        "quartered",
        "julienned",
        "pitted"
    }

    for item in items:
        ingredient = clean_ingredient(item)

        if ingredient not in ignore_words and len(ingredient) > 1:
            cleaned.append(ingredient)

    return cleaned


# Cleaning directions
def clean_directions(text):
    if not text:
        return ""

    text = text.strip()

    # remove extra whitespace/newlines
    text = re.sub(r"\s+", " ", text)

    return text

# Main loading function
def load_recipes_from_csv(file_path):
    db = RecipeDatabase()

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print("Columns:", reader.fieldnames)

        for i, row in enumerate(reader):
            try:
                # id
                recipe_id = int(row.get("Row", i))

                # name
                name = (row.get("recipe_name") or "").strip()
                if not name:
                    continue

                # time
                time_str = (
                    row.get("total_time")
                    or row.get("cook_time")
                    or row.get("prep_time")
                    or ""
                )
                cook_time = parse_time_to_minutes(time_str)

                # ingredients
                ingredients = parse_ingredients(row.get("ingredients", ""))
                if not ingredients:
                    continue

                # directions
                instructions = clean_directions(row.get("directions", ""))

                # create recipe
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
