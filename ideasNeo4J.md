# QUERIES 

1. Find Recipes with the Least Additional Ingredients: If you have a set of ingredients, find recipes that require the fewest additional ingredients.
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
1. Find shortest path between recipes through ingredients shared with other recipes
     ```cypher
     MATCH (r1:Recipe {id: '150351'})
     OPTIONAL MATCH (r2:Recipe {id: '521312'})
     WITH r1, r2
     MATCH p = shortestPath((r1)-[:CONTAINS*1..5]-(r2))
     RETURN p
     ```
1. Best paired Ingredients to optimize the shopping list 
     ```cypher
     MATCH (i1:Ingredient)<-[:CONTAINS]-(r:Recipe)-[:CONTAINS]->(i2:Ingredient)
     WHERE i1.name < i2.name
     WITH i1, i2, r
     WHERE NOT i1.name IN ['sugar', 'salt', 'butter', 'flour', 'water', 'eggs', 'baking powder'] 
     AND NOT i2.name IN ['sugar', 'salt', 'butter', 'flour', 'water', 'eggs', 'baking powder']
     RETURN i1.name AS Ingredient1, i2.name AS Ingredient2, COUNT(r) AS CoOccurrenceCount
     ORDER BY CoOccurrenceCount DESC
     ```
1. Fastest ingredients, categories, keywords, etc. 
     > we could also use the median substituting avg() with percentileDisc(totalMinutes,0.5)
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
     ORDER BY CookMinutes ASC, PrepMinutes ASC
     ```
1. Find the set of recipes that offer a complete set of nutrients with the minimum amount of ingredients or cooking time (remember to take into account the servings) 
     > Macronutrient Ratios in Grams per meal:
     > Protein: ~20–30g per meal (for an average person aiming for 1.2–2.2g of protein per kg of body weight daily).
     > Carbohydrates: ~40–60g per meal, depending on activity levels.
     > Fats: ~10–15g per meal.

     - Ingredients
     ```cypher
     MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)
     WHERE r.FatContent >= 10 AND r.FatContent <= 15 
     AND r.ProteinContent >= 20 AND r.ProteinContent <= 30 
     AND r.CarbohydrateContent >= 40 AND r.CarbohydrateContent <= 60
     RETURN r.Name AS RecipeName, COUNT(i) AS NumOfIngredients
     ORDER BY NumOfIngredients ASC
     ```
     - CookTime
     ```cypher
     MATCH (r:Recipe)
     WHERE r.FatContent >= 10 AND r.FatContent <= 15 
     AND r.ProteinContent >= 20 AND r.ProteinContent <= 30 
     AND r.CarbohydrateContent >= 40 AND r.CarbohydrateContent <= 60
     RETURN r.Name AS RecipeName, r.CookTime.minutes AS CookTime
     ORDER BY r.CookTime ASC
     ```
1. Find the ingredients used in the recipes with highest ratings
     ```cypher
     MATCH (i:Ingredient)<-[:CONTAINS]-(r:Recipe)<-[:FOR]-(review:Review)
     WITH i.name AS Ingredient, review.rating AS Rating, review
     RETURN Ingredient, AVG(Rating) AS AvgRating, COUNT(review) AS ReviewCount
     ORDER BY AvgRating DESC, ReviewCount DESC
     ```
1. The least number of ingredients required for X servings 
Note that when the ingredients are not specified in the recipe, the query returns "character(0" as the only required ingredient
     ```cypher
     MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)
     WHERE tointeger(r.RecipeServings) >= 10
     WITH r, COLLECT(i.name) AS Ingredients, COUNT(i) AS RequiredIngredients
     RETURN r.Name AS RecipeName, Ingredients, RequiredIngredients
     ORDER BY RequiredIngredients ASC
     ```
1. Suggest recipes similar to a given one based on shared ingredients.
     ```cypher
     MATCH (r1:Recipe {Name: "Caprese Salad Tomatoes (Italian Marinated Tomatoes)"})-[:CONTAINS]->(i:Ingredient)<-[:CONTAINS]-(r2:Recipe)
     WHERE r1 <> r2
     RETURN r2.Name AS SimilarRecipe, COUNT(DISTINCT i) AS SharedIngredients, COLLECT(DISTINCT i.name) AS SharedIngredientsList
     ORDER BY SharedIngredients DESC
     ```
1. Suggest recipes belonging to the same category of a given recipe within a calorie range similar .
     ```cypher
     MATCH (r1:Recipe {id:"37944"})-[:BELONGS_TO]->(c:RecipeCategory)<-[:BELONGS_TO]-(r2:Recipe)
     WHERE ABS(COALESCE(r1.Calories,0) - COALESCE(r2.Calories,0)) <= 100 AND r1 <> r2
     RETURN r2.Name AS SimilarRecipe,round(ABS(COALESCE(r1.Calories,0) - COALESCE(r2.Calories,0)),1) AS CalorieDifference
     ORDER BY CalorieDifference ASC;
     ```