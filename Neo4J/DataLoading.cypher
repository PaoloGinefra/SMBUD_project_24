LOAD CSV
WITH HEADERS FROM "file:///recipes(10000).csv" AS row
WITH row
WHERE row.RecipeId IS NOT null
MERGE (r:Recipe { id: row.RecipeId })
ON CREATE SET r.Name = row.Name, r.Calories = tofloat(row.Calories), r.RecipeServings = tointeger(row.RecipeServings), r.CookTime = duration(row.CookTime), r.PrepTime = duration(row.PrepTime), r.TotalTime = duration(row.TotalTime), r.FatContent = tofloat(row.FatContent), r.CarbohydrateContent = tofloat(row.CarbohydrateContent), r.ProteinContent = tofloat(row.ProteinContent)

WITH r, row, trim(replace(row.Keywords, 'c(', '')) AS cleaned_keywords
WITH r, row, trim(replace(cleaned_keywords, ')', '')) AS final_keywords
WITH r, row, split(replace(final_keywords, '"', ''), ', ') AS keywords
UNWIND keywords AS keyword
MERGE (k:Keyword { name: keyword })
MERGE (r)-[: DESCRIBED_BY ]->(k)

WITH r, row, trim(replace(row.RecipeIngredientParts, 'c(', '')) AS cleaned_ingredients
WITH r, row, trim(replace(cleaned_ingredients, ')', '')) AS final_ingredients
WITH r, row, split(replace(final_ingredients, '"', ''), ', ') AS ingredients
UNWIND ingredients AS ingredient
WITH r, row, ingredient
WHERE ingredient <> 'character(0'
MERGE (i:Ingredient {name: ingredient})
MERGE (r)-[: CONTAINS ]->(i)

MERGE (rc:RecipeCategory { name: coalesce(row.RecipeCategory, 'Unknown') })
MERGE (r)-[: BELONGS_TO ]->(rc)

WITH r, row
MERGE (u:User { id: row.AuthorId })
  ON CREATE SET u.name = row.AuthorName // Ensure we only set the name on creation
MERGE (r)-[: CREATED_BY ]->(u)

LOAD CSV
WITH HEADERS FROM "file:///reviews(10000).csv" AS reviewRow
WITH reviewRow
WHERE reviewRow.RecipeId IS NOT null
MERGE (reviewer:User { id: reviewRow.AuthorId })
  ON CREATE SET reviewer.name = reviewRow.AuthorName // Ensure name is set only on creation

WITH reviewRow, reviewer
MERGE (review:Review { id:reviewRow.ReviewId, rating: tointeger(reviewRow.Rating), comment: coalesce(reviewRow.Review, 'No Comment') })

// Match the Recipe with the corresponding RecipeId from the reviews.csv
WITH reviewRow, reviewer, review
MATCH (recipe:Recipe { id: reviewRow.RecipeId })
WITH recipe, reviewRow, reviewer, review
MERGE (reviewer)-[:WROTE]->(review)
MERGE (review)-[:FOR]->(recipe)
