## Most Common Ingredients
<!-- too simple -->
```cypher
MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)
RETURN i.name AS ingredient, COUNT(r) AS usageCount
ORDER BY usageCount DESC
LIMIT 10
```
## Find pairs of ingredients that frequently co-occur in recipes
```cypher
MATCH (i1:Ingredient)<-[:CONTAINS]-(r:Recipe)-[:CONTAINS]->(i2:Ingredient)
WHERE i1.name <  i2.name
RETURN i1.name AS Ingredient1, i2.name AS Ingredient2, COUNT(r) AS CoOccurrenceCount
ORDER BY CoOccurrenceCount DESC
LIMIT 10
```
## Find recipes with the highest average rating and the most reviews
```cypher
MATCH (r:Recipe)<-[:FOR]-(rev:Review)
WITH r, AVG(rev.rating) AS AverageRating, COUNT(rev) AS ReviewCount
RETURN r.Name AS RecipeName, AverageRating, ReviewCount
ORDER BY AverageRating DESC, ReviewCount DESC
LIMIT 10
```
## Suggest recipes similar to a given one based on shared ingredients.
<!-- name of the recipe needed -->
```cypher
MATCH (r1:Recipe {Name: "Caprese Salad Tomatoes (Italian Marinated Tomatoes)"})-[:CONTAINS]->(i:Ingredient)<-[:CONTAINS]-(r2:Recipe)
WHERE r1 <> r2
RETURN r2.Name AS SimilarRecipe, COUNT(i) AS SharedIngredients
ORDER BY SharedIngredients DESC
LIMIT 10;
```
## Suggest recipes belonging to the same category of a given recipe within a calorie range similar .
<!-- name of the recipe needed -->
```cypher
MATCH (r1:Recipe {Name: "Bruschetta"})-[:BELONGS_TO]->(c:RecipeCategory)<-[:BELONGS_TO]-(r2:Recipe)
WHERE ABS(r1.Calories - r2.Calories) <= 100 AND r1 <> r2
RETURN r2.Name AS SimilarRecipe, r2.Calories AS Calories
ORDER BY Calories;
```
## Find users who have reviewed the most recipes
<!-- not that interesting -->
```cypher
MATCH (u:User)-[:WROTE]->(rev:Review)
RETURN u.name AS Username, COUNT(rev) AS ReviewCount
ORDER BY ReviewCount DESC
LIMIT 10
```
## Recipes with the Most Ingredients
<!-- too simple -->
```cypher
MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)
RETURN r.Name AS RecipeName, COUNT(i) AS IngredientCount
ORDER BY IngredientCount DESC
LIMIT 10
```
## Most Common Keywords
<!-- too simple -->
```cypher
MATCH (k:Keyword)<-[:DESCRIBED_BY]-(r:Recipe)
RETURN k.name AS Keyword, COUNT(r) AS RecipeCount
ORDER BY RecipeCount DESC
LIMIT 10
```
## Most popular recipe categories
```cypher
MATCH (rc:RecipeCategory)<-[:BELONGS_TO]-(r:Recipe)-[:FOR]->(review:Review)
RETURN rc.name AS Category, COUNT(review) AS ReviewCount
ORDER BY ReviewCount DESC
LIMIT 10
```
## Correlation Between Ingredients and Ratings
```cypher
MATCH (i:Ingredient)<-[:CONTAINS]-(r:Recipe)<-[:FOR]-(review:Review)
RETURN i.name AS Ingredient, AVG(review.rating) AS AvgRating, COUNT(r) AS RecipeCount
ORDER BY AvgRating DESC
LIMIT 10
```
## Analyze whether specific ingredients are associated with more positive or negative reviews.
<!-- better in elasticsearch -->
```cypher
MATCH (i:Ingredient)<-[:CONTAINS]-(r:Recipe)<-[:FOR]-(review:Review)
WITH i.name AS Ingredient, review.rating AS Rating, review
RETURN Ingredient, AVG(Rating) AS AvgRating, COUNT(review) AS ReviewCount
ORDER BY AvgRating DESC, ReviewCount DESC
LIMIT 10
```