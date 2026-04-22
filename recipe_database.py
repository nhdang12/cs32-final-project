from recipe import Recipe


class RecipeDatabase:
    """
    Stores and searches a collection of Recipe objects.
    """

    def __init__(self):
        self.recipes = []
        self.recipes_by_id = {}
        self.ingredient_index = {}
        self.favorite_recipe_ids = set()

    def add_recipe(self, recipe):
        """
        Adds a Recipe object to the database and updates indexes.
        """
        self.recipes.append(recipe)
        self.recipes_by_id[recipe.recipe_id] = recipe

        for ingredient in recipe.ingredient_set:
            if ingredient not in self.ingredient_index:
                self.ingredient_index[ingredient] = set()
            self.ingredient_index[ingredient].add(recipe.recipe_id)

    def add_favorite(self, recipe_id):
        """
        Add a favorite recipe to the bookmarked list
        """
        self.favorite_recipe_ids.add(recipe_id)

    def is_favorite(self, recipe_id):
        """
        Boolean flag if a recipe is a favorite
        """
        return recipe_id in self.favorite_recipe_ids

    def get_recipe_by_id(self, recipe_id):
        """
        Returns a recipe by its ID, or None if not found.
        """
        return self.recipes_by_id.get(recipe_id)

    def search_by_ingredient(self, ingredient):
        """
        Returns all recipes containing a specific ingredient.
        """
        ingredient = ingredient.strip().lower()

        if ingredient not in self.ingredient_index:
            return []

        recipe_ids = self.ingredient_index[ingredient]
        return [self.recipes_by_id[recipe_id] for recipe_id in recipe_ids]

    def similarity_to(self, other_recipe):
        """
        Similarity score between two recipes based on shared ingredients
        """
        intersection = self.ingredient_set & other_recipe.ingredient_set
        union = self.ingredient_set | other_recipe.ingredient_set

        if len(union) == 0:
            return 0

    return len(intersection) / len(union)

    def search(
        self,
        available_ingredients=None,
        excluded_ingredients=None,
        max_time=None,
        top_n=None
    ):
        """
        Main search function.

        Filters recipes by:
        - excluded ingredients
        - max cook time

        Then ranks remaining recipes by match score.
        """
        if available_ingredients is None:
            available_ingredients = set()
        if excluded_ingredients is None:
            excluded_ingredients = set()

        # Normalize input sets
        available_ingredients = {item.strip().lower() for item in available_ingredients}
        excluded_ingredients = {item.strip().lower() for item in excluded_ingredients}

        results = []

        for recipe in self.recipes:
            if recipe.contains_excluded(excluded_ingredients):
                continue

            if max_time is not None and not recipe.matches_time(max_time):
                continue

            score = recipe.match_score(available_ingredients)
            matching = recipe.get_matching_ingredients(available_ingredients)
            missing = recipe.get_missing_ingredients(available_ingredients)

            results.append({
                "recipe": recipe,
                "score": score,
                "matching_ingredients": matching,
                "missing_ingredients": missing
            })

        # Higher score first, then shorter cook time, then alphabetical name
        def sort_key(item):
            return (-item["score"], item["recipe"].cook_time, item["recipe"].name.lower())

        results.sort(key=sort_key)

        if top_n is not None:
            return results[:top_n]

        return results

    def __len__(self):
        return len(self.recipes)
