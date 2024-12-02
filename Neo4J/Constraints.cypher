CREATE CONSTRAINT FOR (recipe:Recipe) REQUIRE recipe.id IS UNIQUE;

CREATE CONSTRAINT FOR (ingredient:Ingredient) REQUIRE ingredient.name IS UNIQUE;

CREATE CONSTRAINT FOR (keyword:Keyword) REQUIRE keyword.name IS UNIQUE;

CREATE CONSTRAINT FOR (recipeCategory:RecipeCategory) REQUIRE recipeCategory.name IS UNIQUE;

CREATE CONSTRAINT FOR (user:User) REQUIRE user.id IS UNIQUE;

CREATE CONSTRAINT FOR (review:Review) REQUIRE review.id IS UNIQUE;
