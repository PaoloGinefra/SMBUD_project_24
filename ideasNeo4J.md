# QUERIES 

1. Find Recipes with the Least Additional Ingredients: If you have a set of ingredients, find recipes that require the fewest additional ingredients.     
     > insert input

     ```cypher
     MATCH (i:Ingredient)<-[:CONTAINS]-(r:Recipe)
     WHERE i.name IN ["egg", "flour", "milk"]
     WITH r, COLLECT(i.name) AS available_ingredients
     MATCH (r)-[:CONTAINS]->(missing:Ingredient)
     WHERE NOT missing.name IN available_ingredients
     RETURN r.Name AS Recipe, 
          COLLECT(missing.name) AS MissingIngredients,
          SIZE(COLLECT(missing.name)) AS MissingIngredientsCount
     ORDER BY MissingIngredientsCount ASC
     ```
1. Best paired Ingredients to optimize the shopping list (removing from the list of ingredients the most frequent ones)
     ```cypher
     MATCH (i:Ingredient)<-[:CONTAINS]-(r:Recipe)
     WITH i.name AS Ingredient, COUNT(r) AS Frequency
     ORDER BY Frequency DESC LIMIT  10
     WITH COLLECT(Ingredient) AS FilteredIngredients 
     MATCH (i1:Ingredient)<-[:CONTAINS]-(r:Recipe)-[:CONTAINS]->(i2:Ingredient)
     WHERE i1.name < i2.name AND NOT i1.name  IN FilteredIngredients AND NOT i2.name IN FilteredIngredients
     WITH i1, i2, r
     RETURN i1.name AS Ingredient1, i2.name AS Ingredient2, COUNT(r) AS CoOccurrenceCount
     ORDER BY CoOccurrenceCount DESC
     ```
1. Match a user to recipes based on recipes the user reviewed with a high rating
     ```cypher
     MATCH (u:User)-[:WROTE]->(review:Review)-[:FOR]->(r:Recipe)-[:CONTAINS]->(i:Ingredient)
     WHERE review.rating > 4 AND u.name='Donna Tomko'
     MATCH (suggested:Recipe)-[:CONTAINS]->(i)
     WHERE NOT (u)-[:WROTE]->()-[:FOR]->(suggested)
     WITH suggested, COUNT(DISTINCT i) AS matchingIngredients
     RETURN suggested.Name AS recipeName, matchingIngredients
     ORDER BY matchingIngredients DESC LIMIT 5;
     ```
1. Find categories that require the minimum amount of time
     ```cypher
     MATCH (r:Recipe)-[:BELONGS_TO]->(c:RecipeCategory)
     WHERE r.TotalTime IS NOT NULL
     RETURN c.name AS category, tointeger(AVG(r.TotalTime.minutes)) AS avgTotalTimeMinutes
     ORDER BY avgTotalTimeMinutes ASC
     ```
1. The most diversified ingredients 
     ```cypher
     MATCH (i:Ingredient)<-[:CONTAINS]-(r:Recipe)-[:BELONGS_TO]->(c:RecipeCategory)
     RETURN i.name AS IngredientName, COUNT(DISTINCT c) AS NumOfCategories
     ORDER BY NumOfCategories DESC
     ```
1. Recipes classified by cooking time and prep time 
     ```cypher
     MATCH (r:Recipe)
     WHERE r.CookTime IS NOT NULL AND r.PrepTime IS NOT NULL
     RETURN r.Name, 
          r.CookTime.minutes AS CookMinutes, r.PrepTime.minutes AS PrepMinutes
     ORDER BY  PrepMinutes ASC, CookMinutes ASC
     ```
1. Find the ingredients used in the recipes with highest ratings
     ```cypher
     MATCH (i:Ingredient)<-[:CONTAINS]-(r:Recipe)<-[:FOR]-(review:Review)
     WITH i.name AS Ingredient, review.rating AS Rating, review
     RETURN Ingredient, AVG(Rating) AS AvgRating, COUNT(review) AS ReviewCount
     ORDER BY AvgRating DESC, ReviewCount DESC
     ```
1. Find recipes with the least number of ingredients required for X servings 
     >insert input
     ```cypher
     MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)
     WHERE tointeger(r.RecipeServings) >= 10
     WITH r, COLLECT(i.name) AS Ingredients, COUNT(i) AS RequiredIngredients
     RETURN r.Name AS RecipeName, Ingredients, RequiredIngredients
     ORDER BY RequiredIngredients ASC
     ```
1. Suggest recipes similar to a given one based on shared ingredients.
     > insert input
     ```cypher
     MATCH (r1:Recipe {Name: "Caprese Salad Tomatoes (Italian Marinated Tomatoes)"})-[:CONTAINS]->(i:Ingredient)<-[:CONTAINS]-(r2:Recipe)
     WHERE r1 <> r2
     RETURN r2.Name AS SimilarRecipe, COUNT(DISTINCT i) AS SharedIngredients, COLLECT(DISTINCT i.name) AS SharedIngredientsList
     ORDER BY SharedIngredients DESC
     ```
1. Suggest recipes belonging to the same category of a given recipe within a calorie range similar .
     > insert input 
     ```cypher
     MATCH (r1:Recipe {Name: "Caprese Salad Tomatoes (Italian Marinated Tomatoes)"})-[:BELONGS_TO]->(c:RecipeCategory)<-[:BELONGS_TO]-(r2:Recipe)
     WHERE ABS(COALESCE(r1.Calories,0) - COALESCE(r2.Calories,0)) <= 100 AND r1 <> r2
     RETURN r2.Name AS SimilarRecipe,round(ABS(COALESCE(r1.Calories,0) - COALESCE(r2.Calories,0)),1) AS CalorieDifference
     ORDER BY CalorieDifference ASC;
     ```


1. Find the set of recipes that offer a complete set of nutrients with the minimum amount of ingredients.
     > Protein: ~20–30g per meal (for an average person aiming for 1.2–2.2g of protein per kg of body weight daily).
     > Carbohydrates: ~40–60g per meal, depending on activity levels.
     > Fats: ~10–15g per meal.

     ```cypher
     MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)
     WHERE r.FatContent >= 10 AND r.FatContent <= 15 
     AND r.ProteinContent >= 20 AND r.ProteinContent <= 30 
     AND r.CarbohydrateContent >= 40 AND r.CarbohydrateContent <= 60
     RETURN r.Name AS RecipeName, COUNT(i) AS NumOfIngredients
     ORDER BY NumOfIngredients ASC
     ```