class Recipe:
    """
    Represents a single recipe and provides helper methods
    for filtering and scoring.
    """

    def __init__(self, recipe_id, name, ingredients, cook_time, category=None, instructions = "", source=None):
        self.recipe_id = recipe_id
        self.name = name
        self.ingredients = ingredients
        self.cook_time = cook_time
        self.category = category
        self.instructions = instructions
        self.source = source

        # Normalized ingredient set for fast searching
        self.ingredient_set = set()
        for ingredient in ingredients:
            normalized = self._normalize_text(ingredient)
            if normalized:
                self.ingredient_set.add(normalized)

    def _normalize_text(self, text):
        """
        Converts text to lowercase and removes extra spaces.
        Example: '  Olive Oil ' -> 'olive oil'
        """
        return text.strip().lower()

    def contains_excluded(self, excluded_ingredients):
        """
        Returns True if the recipe contains any excluded ingredient.
        excluded_ingredients should be a set of normalized strings.
        """
        return len(self.ingredient_set.intersection(excluded_ingredients)) > 0

    def matches_time(self, max_time):
        """
        Returns True if the recipe cook time is less than or equal to max_time.
        """
        return self.cook_time <= max_time

    def get_matching_ingredients(self, available_ingredients):
        """
        Returns a set of ingredients the user has that are used in this recipe.
        """
        return self.ingredient_set.intersection(available_ingredients)

    def get_missing_ingredients(self, available_ingredients):
        """
        Returns a set of ingredients needed by the recipe that the user does not have.
        """
        return self.ingredient_set.difference(available_ingredients)

    def match_score(self, available_ingredients, max_time=None, favorite_recipes=None):
        """
        Calculates an overall match score for this recipe.

        Score includes:
        - ingredient matches
        - missing ingredient penalty
        - time bonus
        - similarity bonus based on user's favorite recipes
        """
    
        matches = len(self.get_matching_ingredients(available_ingredients))
        missing = len(self.get_missing_ingredients(available_ingredients))
        total_ingredients = len(self.ingredient_set)
    
        if total_ingredients == 0:
            match_ratio = 0
        else:
            match_ratio = matches / total_ingredients
    
        ratio_score = match_ratio * 20
        missing_penalty = missing
        ingredient_score = ratio_score - missing_penalty
    
        time_bonus = 0
        if max_time is not None and self.cook_time <= max_time:
            time_bonus = 5
    
        similarity_bonus = 0
        if favorite_recipes:
            total_similarity = 0
            count = 0
    
            for favorite in favorite_recipes:
                if favorite.recipe_id != self.recipe_id:
                    total_similarity += self.similarity_to(favorite)
                    count += 1
    
            if count > 0:
                average_similarity = total_similarity / count
                similarity_bonus = average_similarity * 10
    
        return ingredient_score + time_bonus + similarity_bonus

    def similarity_to(self, other_recipe):
        """
        Similarity score between two recipes based on shared ingredients
        """
        intersection = self.ingredient_set & other_recipe.ingredient_set
        union = self.ingredient_set | other_recipe.ingredient_set

        if len(union) == 0:
            return 0

        return len(intersection) / len(union)
        
    def to_dict(self):
        """
        Converts the Recipe object into a dictionary.
        """
        return {
            "recipe_id": self.recipe_id,
            "name": self.name,
            "ingredients": self.ingredients,
            "cook_time": self.cook_time,
            "category": self.category,
            "source": self.source
        }

    def __str__(self):
        return f"{self.name} ({self.cook_time} min)"
