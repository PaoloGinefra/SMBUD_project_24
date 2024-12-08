# Ideas

**Neo4j** = 📊
- Find Recipes with the Least Additional Ingredients: If you have a set of ingredients, find recipes that require the fewest additional ingredients.

MATCH (i:Ingredient)-[:USED_IN]->(r:Recipe)
WHERE i.name IN ["egg", "flour", "milk"] // Replace with your ingredients
WITH r, COLLECT(i.name) AS available_ingredients, COUNT(i) AS used_ingredients
MATCH (r)-[:USES]->(missing:Ingredient)
WHERE NOT missing.name IN available_ingredients
RETURN r.name AS Recipe, COUNT(missing) AS MissingIngredients
ORDER BY MissingIngredients ASC

- Find Closest Substitutions for Ingredients: Use a graph of dietary restrictions or ingredient alternatives to find the shortest substitution chain.

MATCH p = shortestPath((i1:Ingredient)-[:SUBSTITUTES_FOR*]-(i2:Ingredient))
WHERE i1.name = "milk" // Replace with the ingredient to substitute
RETURN i1.name AS OriginalIngredient, i2.name AS Substitute, length(p) AS Steps
ORDER BY Steps ASC LIMIT 5

- Best paired Ingredients to otimize the shopping list 📊
- Fastest ingredients, categories, keywords, etc. 🔍📊
- The most diversified ingredients 📊
- Recipes classified by cooking time and prep time 🔍
- Find the set of recipes that offer a complete set of nutrients with the minimum ammout of ingredients or cooking time (remember to take into account the servings) 📊
- Find the ingredients used in the recipes with highest ratios 📊
- The least number of ingredients required for X servings 📊

**Elasticsearch** = 🔍
- Find the recipes fit for meal prep 🔍
- Romantic dinner recipes 🔍
- Recipes for a party with a lot of servings🔍📊
- Recipes without an oven with air fryer🔍📊
- Recipes inspired by pop culture (movies, books, TV shows). 
- Recipes with whatever I have in my fridge 🔍
- Find the recipes with the best protein/calory ratio 🔍
- Recipes for Specific Dietary Restrictions 🔍
- Seasonal Recipes (Based on Ingredients or Holidays) 🔍
- Best Meal Plan for Nutritional Balance and Minimum Overlap 📊