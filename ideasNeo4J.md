# Queries ideas
## Determine which ingredients are most often found in recipes with high average ratings.
## Investigate if higher or lower calorie recipes tend to get better ratings.
## Compare the average ratings of recipes grouped by cook time intervals.
## Identify clusters of users who frequently review recipes with similar keywords or categories.
## Find pairs of ingredients that frequently co-occur in recipes
```cypher
MATCH (i1:Ingredient)<-[:Contains]-(r:Recipe)-[:Contains]->(i2:Ingredient)
WHERE i1.name < i2.name
RETURN i1.name AS Ingredient1, i2.name AS Ingredient2, COUNT(r) AS CoOccurrenceCount
ORDER BY CoOccurrenceCount DESC
LIMIT 10
```
## Find recipes with the highest average rating and the most reviews
```
MATCH (r:Recipe)<-[:For]-(rev:Review)
WITH r, AVG(rev.rating) AS AverageRating, COUNT(rev) AS ReviewCount
RETURN r.name AS RecipeName, AverageRating, ReviewCount
ORDER BY AverageRating DESC, ReviewCount DESC
LIMIT 10
```
## Find users who have reviewed the most recipes
```
MATCH (u:User)-[:By]->(rev:Review)
RETURN u.id AS UserId, COUNT(rev) AS ReviewCount
ORDER BY ReviewCount DESC
LIMIT 10
```
## Find recipes that share the most keywords
```
MATCH (r1:Recipe)-[:Described_by]->(k:Keyword)<-[:Described_by]-(r2:Recipe)
WHERE r1 <> r2
RETURN r1.name AS Recipe1, r2.name AS Recipe2, COUNT(k) AS SharedKeywords
ORDER BY SharedKeywords DESC
LIMIT 10
```
## Suggest recipes similar to a given one based on shared ingredients.
```
MATCH (r1:Recipe {name: "Pasta Carbonara"})-[:Contains]->(i:Ingredient)<-[:Contains]-(r2:Recipe)
WHERE r1 <> r2
RETURN r2.name AS SimilarRecipe, COUNT(i) AS SharedIngredients
ORDER BY SharedIngredients DESC
LIMIT 5;
```
## Find ingredients that are rarely used together but appear in similar recipes.
```MATCH (i1:Ingredient)<-[:Contains]-(r:Recipe)-[:Contains]->(i2:Ingredient)
WHERE NOT (i1)-[:Contains]->(r2:Recipe)-[:Contains]->(i2)
RETURN i1.name AS Ingredient1, i2.name AS Ingredient2, COUNT(r) AS SharedRecipes
ORDER BY SharedRecipes DESC
LIMIT 10;
```
## Find users whose reviews cover a large number of recipes
```
MATCH (u:User)-[:By]->(rev:Review)-[:For]->(r:Recipe)
RETURN u.id AS UserId, COUNT(DISTINCT r) AS ReviewedRecipes
ORDER BY ReviewedRecipes DESC
LIMIT 10;
```
## Track how often an ingredient is used in recipes over time.
```
MATCH (i:Ingredient)<-[:Contains]-(r:Recipe)
RETURN i.name AS Ingredient, r.creationDate.year AS Year, COUNT(r) AS RecipeCount
ORDER BY Year, RecipeCount DESC;
```
## Recommend recipes in different categories but with shared keywords or ingredients.
```
MATCH (r1:Recipe)-[:Belongs_to]->(c1:RecipeCategory), 
      (r2:Recipe)-[:Belongs_to]->(c2:RecipeCategory), 
      (r1)-[:Described_by]->(k:Keyword)<-[:Described_by]-(r2)
WHERE c1 <> c2
RETURN r1.name AS Recipe1, r2.name AS Recipe2, COUNT(k) AS SharedKeywords
ORDER BY SharedKeywords DESC
LIMIT 10;
```
## Suggest recipes within a calorie range similar to a given recipe.
```
MATCH (r1:Recipe {name: "Avocado Salad"}), (r2:Recipe)
WHERE ABS(r1.calories - r2.calories) <= 100 AND r1 <> r2
RETURN r2.name AS SimilarRecipe, r2.calories AS Calories
ORDER BY Calories;
```