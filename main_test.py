from kaggle_loader import load_recipes_from_csv

def main():
    db = load_recipes_from_csv("recipes.csv")

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
