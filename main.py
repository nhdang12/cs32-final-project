from recipe import Recipe
from recipe_database import RecipeDatabase


def main():
    db = RecipeDatabase()

    r1 = Recipe(
        recipe_id=1,
        name="Garlic Butter Pasta",
        ingredients=["pasta", "garlic", "butter", "parmesan"],
        cook_time=20,
        category="Dinner"
    )

    r2 = Recipe(
        recipe_id=2,
        name="Chicken Rice Bowl",
        ingredients=["chicken", "rice", "soy sauce", "garlic"],
        cook_time=30,
        category="Lunch"
    )

    r3 = Recipe(
        recipe_id=3,
        name="Veggie Omelette",
        ingredients=["eggs", "spinach", "cheese", "onion"],
        cook_time=10,
        category="Breakfast"
    )

    db.add_recipe(r1)
    db.add_recipe(r2)
    db.add_recipe(r3)

    available = {"garlic", "butter", "pasta", "cheese"}
    excluded = {"soy sauce"}
    max_time = 25

    results = db.search(
        available_ingredients=available,
        excluded_ingredients=excluded,
        max_time=max_time,
        top_n=5
    )

    for item in results:
        recipe = item["recipe"]
        print(recipe)
        print("  Score:", item["score"])
        print("  Matching:", sorted(item["matching_ingredients"]))
        print("  Missing:", sorted(item["missing_ingredients"]))
        print()


if __name__ == "__main__":
    main()
