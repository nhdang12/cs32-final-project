from kaggle_loader import load_recipes_from_csv, clean_ingredient


def get_ingredient_set(prompt):
    """
    Ask the user for comma-separated ingredients and return a cleaned set.
    """
    user_input = input(prompt).strip()

    if user_input == "":
        return set()

    parts = user_input.split(",")
    ingredients = set()

    for part in parts:
        cleaned = clean_ingredient(part)
        if cleaned != "":
            ingredients.add(cleaned)

    return ingredients


def get_max_time():
    """
    Ask the user for a maximum cooking time.
    Returns an integer or None.
    """
    user_input = input("Enter max cooking time in minutes (or press Enter to skip): ").strip()

    if user_input == "":
        return None

    while not user_input.isdigit():
        user_input = input("Please enter a whole number, or press Enter to skip: ").strip()
        if user_input == "":
            return None

    return int(user_input)


def display_results(results, db):
    """
    Display search results in a numbered list.
    """
    if len(results) == 0:
        print("\nNo matching recipes found.\n")
        return

    print("\nTop recipe matches:\n")

    for i, item in enumerate(results, start=1):
        recipe = item["recipe"]
        favorite_mark = " [FAVORITE]" if db.is_favorite(recipe.recipe_id) else ""

        print(f"{i}. {recipe.name}{favorite_mark}")
        print(f"   Cook time: {recipe.cook_time} minutes")
        print(f"   Score: {item['score']:.2f}")
        print(f"   Matching ingredients: {sorted(item['matching_ingredients'])}")
        print(f"   Missing ingredients: {sorted(item['missing_ingredients'])}")
        print()


def display_recipe(recipe):
    """
    Show full recipe details.
    """
    print("\n" + "=" * 50)
    print(recipe.name)
    print("=" * 50)
    print(f"Cook time: {recipe.cook_time} minutes")

    if recipe.category:
        print(f"Category: {recipe.category}")

    if recipe.source:
        print(f"Source: {recipe.source}")

    print("\nIngredients:")
    for ingredient in recipe.ingredients:
        print(f"- {ingredient}")

    print("\nInstructions:")
    if recipe.instructions:
        print(recipe.instructions)
    else:
        print("No instructions available.")

    print()


def choose_recipe(results):
    """
    Let the user choose a recipe from the results.
    """
    if len(results) == 0:
        return None

    user_input = input(
        "Enter a recipe number to view details, or press Enter to skip: "
    ).strip()

    if user_input == "":
        return None

    while not user_input.isdigit() or not (1 <= int(user_input) <= len(results)):
        user_input = input(
            "Please enter a valid recipe number, or press Enter to skip: "
        ).strip()

        if user_input == "":
            return None

    return results[int(user_input) - 1]["recipe"]


def ask_to_favorite(db, recipe):
    """
    Add/remove a recipe from favorites.
    """
    if db.is_favorite(recipe.recipe_id):
        user_input = input('This recipe is already a favorite. Remove it? (y/n): ').strip().lower()
        if user_input == "y":
            db.remove_favorite(recipe.recipe_id)
            print(f'"{recipe.name}" removed from favorites.\n')
    else:
        user_input = input(f'Add "{recipe.name}" to favorites? (y/n): ').strip().lower()
        if user_input == "y":
            db.add_favorite(recipe.recipe_id)
            print(f'"{recipe.name}" added to favorites.\n')


def show_favorites(db):
    """
    Display all favorite recipes.
    """
    favorites = db.get_favorite_recipes()

    if len(favorites) == 0:
        print("\nYou have no favorite recipes yet.\n")
        return

    print("\nFavorite Recipes:\n")
    for i, recipe in enumerate(favorites, start=1):
        print(f"{i}. {recipe.name} ({recipe.cook_time} min)")
    print()


def run_search(db):
    """
    Run one recipe search using user input.
    """
    print("\nRecipe Search")
    print("-" * 20)

    available_ingredients = get_ingredient_set(
        "Enter ingredients you have (comma separated): "
    )

    excluded_ingredients = get_ingredient_set(
        "Enter ingredients to avoid (comma separated, or press Enter to skip): "
    )

    max_time = get_max_time()

    results = db.search(
        available_ingredients=available_ingredients,
        excluded_ingredients=excluded_ingredients,
        max_time=max_time,
        top_n=5
    )

    display_results(results, db)

    selected = choose_recipe(results)
    if selected:
        display_recipe(selected)
        ask_to_favorite(db, selected)


def main():
    print("Welcome to Recipe Finder!")

    file_path = input("Enter your CSV file name (e.g., recipes.csv): ").strip()
    db = load_recipes_from_csv(file_path)

    while True:
        print("\nMenu")
        print("1. Search for recipes")
        print("2. View favorite recipes")
        print("3. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            run_search(db)
        elif choice == "2":
            show_favorites(db)
        elif choice == "3":
            print("Thanks for using Recipe Finder!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
