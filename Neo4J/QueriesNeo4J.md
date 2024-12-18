# QUERIES NEO4J TASTE TRIOS

##  1. Based on a list of ingredients that the user has, find the ingredients the most used with a set of those ingredients, the recipes matched with those ingredient, the average of the average rating of the recipes matched and the average number of ingredients that the user has, matched in the recipes of the ingredient found.

> INSERT INPUT

This query analyzes recipes based on a provided list of ingredients to identify additional ingredients that frequently appear in combination with those in the list. It evaluates these additional ingredients by calculating their compatibility with the provided ingredients and their relevance based on recipe popularity and quality.
This query is particularly useful for recommending new ingredients to include in a recipe, optimizing ingredient selection based on popularity and quality, or creating a data-driven approach to culinary exploration.

Key Steps and Functionality:

- Input Ingredients:
The query uses a parameter, $providedIngredients, which is a list of ingredients provided by the user.

- The query finds recipes (r) that contain at least one of the provided ingredients (i) and identifies other ingredients (i1) in those recipes that are not in the provided list.
It ensures that these ingredients are distinct and tracks the count of how many provided ingredients are present in each recipe as availableMatchedIngredients.
- Calculate Average Recipe Rating:
For each matched recipe, the query retrieves associated reviews (rev) and calculates the average rating (avgRating) of those recipes.
- Aggregate Statistics for Matched Ingredients:
It counts the number of unique recipes (recipeCount) that include the matched ingredient (i1) in combination with the provided ingredients.
It computes the average of the average ratings (avgOfAvgRatings) across all recipes containing the matched ingredient.
It calculates the average number of provided ingredients matched in the recipes that contain the additional ingredient (IngredientCompatibility).
- Order Results by Relevance:
The results are ordered based on a relevance score that considers both the compatibility of the matched ingredient (IngredientCompatibility) and the logarithm of the number of recipes (log10(recipeCount)) where it is found. This ensures a balance between ingredient synergy and recipe popularity.
     

     ```
                WITH 
                $providedIngredients AS ingredients
                MATCH 
                (i:Ingredient)<-[:CONTAINS]-(r:Recipe)-[:CONTAINS]->(i1:Ingredient)
                WHERE 
                i.name IN ingredients AND NOT i1.name IN ingredients
                WITH 
                DISTINCT r, 
                i1.name AS matchedIngredient,
                ingredients,
                COUNT(distinct i) as availableMatchedIngredients
                MATCH 
                (r)<-[:FOR]-(rev:Review)
                WITH 
                matchedIngredient, 
                r, 
                AVG(rev.rating) AS avgRating,
                ingredients,
                availableMatchedIngredients
                MATCH 
                (r)-[:CONTAINS]->(i:Ingredient)
                WHERE 
                i.name IN ingredients
                RETURN 
                matchedIngredient, 
                COUNT(DISTINCT r) AS recipeCount, 
                AVG(avgRating) AS avgOfAvgRatings, 
                AVG(availableMatchedIngredients) as IngredientCompatibility
                ORDER BY 
                IngredientCompatibility * log10(recipeCount) DESC;
     ```

## 2. Suggest recipes belonging to the same category of a given recipe within a calorie range similar and no shared ingredients.

> INSERT INPUT

This Cypher query suggests recipes that belong to the same category as a given recipe but have no shared ingredients, while maintaining a similar calorie count within a specified range.

Key Steps and Functionality:

- Find the Recipe Category:
The query starts by identifying the category (c) of a specified recipe (r1) using its name.
- Filter Recipes in the Same Category:
It retrieves other recipes (r2) that belong to the same category (c) but are not the same as the original recipe (r1).
- Calorie Range Matching:
Recipes are filtered to ensure their calorie count (r2.Calories) is within 100 calories of the specified recipe (r1.Calories).
The calorie values are handled using COALESCE to account for potential missing data.
- Exclude Shared Ingredients:
The query ensures no ingredients are shared between the original recipe (r1) and the suggested recipes (r2) by using a subquery that checks for the absence of overlapping Ingredient relationships.
- Sort by Calorie Difference:
Suggested recipes are ordered by the absolute difference in calories (CalorieDifference), ensuring the closest matches in terms of calorie content appear first.

This query is useful for recommending alternative recipes within the same category that align with dietary preferences or calorie requirements, while ensuring a diverse ingredient selection.


     ```cypher
     MATCH 
     (r1:Recipe {Name: "Caprese Salad Tomatoes (Italian Marinated Tomatoes)"})-[:BELONGS_TO]->(c:RecipeCategory)<-[:BELONGS_TO]-(r2:Recipe)
     WHERE 
     ABS(COALESCE(r1.Calories, 0) - COALESCE(r2.Calories, 0)) <= 100 
     AND r1 <> r2 
     AND NOT EXISTS {
     MATCH (r1)-[:CONTAINS]->(i:Ingredient)<-[:CONTAINS]-(r2)
     }
     RETURN 
     r2.Name AS SimilarRecipe,
     round(ABS(COALESCE(r1.Calories, 0) - COALESCE(r2.Calories, 0)), 1) AS CalorieDifference
     ORDER BY 
     CalorieDifference ASC;
     ```

## 3. Find recipes with the least number of ingredients required for X servings or large groups

This query identifies recipes that require the least number of ingredients to prepare for a given number of servings, emphasizing recipes designed for large groups or higher servings.

Key Steps and Functionality:
- Filter Recipes Based on Serving Size:

- Recipes are selected based on their serving size (r.RecipeServings) or their association with categories and keywords indicating they are suitable for large groups:
    - Recipes with servings greater than or equal to 10.
    - Recipes belonging to the category For Large Groups or having the keyword For Large Groups.
- Ingredient Collection: For each matching recipe, the query identifies all associated ingredients (i) and collects their names into a list (Ingredients). It counts the number of unique ingredients required for the recipe as RequiredIngredients.
- Sort by Ingredient Count:
Recipes are sorted in ascending order based on the number of ingredients required (RequiredIngredients), highlighting those that are simpler to prepare in terms of ingredient count.

This query is useful for users looking to prepare simple recipes with minimal ingredients, especially for large groups. It streamlines recipe selection by balancing simplicity and scalability.

     ```cypher
     MATCH 
     (c:RecipeCategory)<-[:BELONGS_TO]-(r:Recipe)-[:CONTAINS]->(i:Ingredient),
     (r)-[:DESCRIBED_BY]->(k:Keyword)
     WHERE 
     tointeger(r.RecipeServings) >= 10 
     OR c.name = 'For Large Groups' 
     OR k.name = 'For Large Groups'
     WITH 
     r,
     COLLECT(i.name) AS Ingredients,
     COUNT(i) AS RequiredIngredients
     RETURN 
     r.Name AS RecipeName,
     RequiredIngredients,
     Ingredients
     ORDER BY 
     RequiredIngredients ASC;
     ```

## 4. Match a user to recipes based on recipes the user reviewed with a high rating

> INSERT INPUT

This  query recommends recipes to a specific user based on the ingredients of recipes they have rated highly. It identifies recipes that share ingredients with these highly-rated recipes but that the user has not reviewed yet.

Key Steps and Functionality:

- Identify High-Rated Recipes:
The query starts by finding recipes (r) reviewed by the user (u) with a high rating (rating > 4).
It also identifies the ingredients (i) of these highly-rated recipes.
- Find Suggested Recipes:
It retrieves recipes (suggested) that contain one or more of the same ingredients as the user's high-rated recipes. It excludes recipes the user has already reviewed to ensure only new suggestions are presented.
- Ingredient Matching:
For each suggested recipe, the query counts the number of ingredients it shares with the user's high-rated recipes (matchingIngredients).
- Sort and Limit Results:
Suggested recipes are ordered in descending order based on the number of matching ingredients.
The query limits the output to the top 5 most relevant recipe suggestions.

This query is particularly useful for personalized recipe recommendations. It leverages the user's past preferences to suggest recipes with similar ingredient profiles, ensuring relevance and increasing the likelihood of user satisfaction.

     ```cypher
     MATCH 
     (u:User)-[:WROTE]->(review:Review)-[:FOR]->(r:Recipe)-[:CONTAINS]->(i:Ingredient)
     WHERE 
     review.rating > 4 AND u.name='Donna Tomko'
     MATCH 
     (suggested:Recipe)-[:CONTAINS]->(i)
     WHERE NOT
     (u)-[:WROTE]->()-[:FOR]->(suggested)
     WITH suggested, COUNT(DISTINCT i) AS matchingIngredients
     RETURN 
     suggested.Name AS recipeName,
     matchingIngredients
     ORDER BY 
     matchingIngredients DESC LIMIT 5;
     ```

## 5. Find the ingredients that appear in the highest number of categories (most diversified ingredients) and the average across all the categories of the average rating of the recipes containing that ingredient.
This query identifies the most diversified ingredients in a recipe database and calculates their average ratings across categories.
- Matching Ingredients and Categories:
The query starts by finding all Ingredient nodes (i) that are connected to Recipe nodes (r) via the CONTAINS relationship.
It further connects each Recipe to RecipeCategory nodes (c) through the BELONGS_TO relationship.
- Optional Matching Reviews:
For each recipe, the query optionally matches Review nodes (rev) via the FOR relationship. This step captures the ratings given to recipes.
- Calculating Metrics:
It calculates the average rating (AvgRatingPerCategory) for each category a recipe belongs to by averaging the ratings of its reviews.
- Aggregating Results:
For each ingredient (IngredientName), the query counts the number of distinct categories it appears in (NumOfCategories).
It also computes the average of AvgRatingPerCategory across all categories (AvgRatingAcrossCategories), ensuring a comprehensive rating measure.
- Returning the Output:
The query returns the ingredient name (IngredientName), the number of categories it appears in (NumOfCategories), and the rounded average rating across categories (AvgRatingAcrossCategories).
The results are sorted in descending order of NumOfCategories (most diversified ingredients first) and, within the same number of categories, by AvgRatingAcrossCategories (higher ratings first).

This query is particularly useful for identifying versatile ingredients that contribute to recipes across diverse categories while also considering their average quality or popularity as judged by user reviews.

     ```cypher
     MATCH 
     (i:Ingredient)<-[:CONTAINS]-(r:Recipe)-[:BELONGS_TO]->(c:RecipeCategory)
     OPTIONAL MATCH  
     (r)<-[:FOR]-(rev:Review)
     WITH 
     i.name AS IngredientName, 
     c.name AS CategoryName, 
     AVG(rev.rating) AS AvgRatingPerCategory
     WITH 
     IngredientName, 
     COUNT(DISTINCT CategoryName) AS NumOfCategories, 
     AVG(AvgRatingPerCategory) AS AvgRatingAcrossCategories
     RETURN 
     IngredientName, 
     NumOfCategories, 
     round(AvgRatingAcrossCategories, 2) AS AvgRatingAcrossCategories
     ORDER BY 
     NumOfCategories DESC, 
     AvgRatingAcrossCategories DESC;
     ```

## 6. Suggest recipes similar to a given one based on shared ingredients, shared keywords and return if the recipe found is in the same category as the inserted one 
> INSERT INPUT

This query suggests recipes similar to a given recipe based on shared ingredients and keywords. It compares the specified recipe (in this case, "Caprese Salad Tomatoes (Italian Marinated Tomatoes)") with other recipes in the database and ranks them based on how many ingredients and keywords they share. 
- Matching Ingredients and Recipes:
The query begins by matching the recipe named "Caprese Salad Tomatoes (Italian Marinated Tomatoes)" (r1) and finds the ingredients (i) that it contains using the CONTAINS relationship.
It then matches other recipes (r2) that contain the same ingredients (i) through the CONTAINS relationship.
- Matching Recipe Categories:
Both r1 and r2 are matched to their respective categories (c1 and c2) using the BELONGS_TO relationship. This step ensures that the query can later determine whether the recipes belong to the same category.
- Matching Keywords:
The query optionally matches keywords (k) associated with both recipes (r1 and r2) via the DESCRIBED_BY relationship. This helps capture any additional shared characteristics or themes in the recipes.
- Filtering Different Recipes:
The WHERE r1 <> r2 condition ensures that the query does not compare the recipe with itself.
- Aggregating Data:
The query aggregates the number of shared ingredients (SharedIngredients) and shared keywords (SharedKeywords) between r1 and r2. It also collects the names of the shared ingredients (SharedIngredientsList) and keywords (SharedKeywordsList).
- Checking for Same Category:
The CASE statement checks if the two recipes belong to the same category by comparing c1.name (category of r1) and c2.name (category of r2). It returns "Yes" if they belong to the same category, and "No" otherwise.
- Sorting Results:
The results are sorted by the number of shared ingredients (SharedIngredients) in descending order, followed by the number of shared keywords (SharedKeywords) in descending order.

This query is designed to suggest recipes that are similar to the given one, based on shared ingredients and keywords. The output helps identify recipes that use similar ingredients or cover similar topics, making it useful for users seeking recipes with similar flavor profiles or themes.

     ```cypher
     MATCH 
     (r1:Recipe {Name: "Caprese Salad Tomatoes (Italian Marinated Tomatoes)"})-[:CONTAINS]->(i:Ingredient)<-[:CONTAINS]-(r2:Recipe),
     (r1)-[:BELONGS_TO]->(c1:RecipeCategory),
     (r2)-[:BELONGS_TO]->(c2:RecipeCategory)
     OPTIONAL MATCH 
     (r1)-[:DESCRIBED_BY]->(k:Keyword)<-[:DESCRIBED_BY]-(r2)
     WHERE 
     r1 <> r2
     RETURN 
     r2.Name AS SimilarRecipe, 
     COUNT(DISTINCT i) AS SharedIngredients, 
     COUNT(DISTINCT k) AS SharedKeywords, 
     COLLECT(DISTINCT i.name) AS SharedIngredientsList, 
     COLLECT(DISTINCT k.name) AS SharedKeywordsList, 
     CASE WHEN c1.name = c2.name THEN "Yes" ELSE "No" END AS SameCategory
     ORDER BY 
     SharedIngredients DESC, 
     SharedKeywords DESC;
     ```


## 7. Find categories that require the minimum amount of time, displayng also the minimum and maximum totaltime per category and the average number of ingredients for recipes in that category

This Cypher query is designed to find recipe categories that require the minimum average amount of time, and display the following details for each category:

- Category Information:
The query starts by matching Recipe nodes that are related to RecipeCategory nodes through the BELONGS_TO relationship.
It filters out recipes where the TotalTime is null, ensuring only recipes with a specified total time are considered.
- Ingredient Count:
The query then matches the Ingredient nodes related to each recipe via the CONTAINS relationship. This allows it to count the number of unique ingredients per recipe.
- Aggregation:
The total time for each recipe is extracted in minutes (r.TotalTime.minutes AS totalTimeMinutes), and the number of ingredients in each recipe is counted.
The query then calculates the following aggregated values for each category:
- Average total time (avgTotalTimeMinutes): The average total time for all recipes in the category.
- Minimum total time (minTotalTimeMinutes): The minimum total time across all recipes in the category.
- Maximum total time (maxTotalTimeMinutes): The maximum total time across all recipes in the category.
- Average number of ingredients (avgIngredientsPerCategory): The average number of ingredients for recipes in the category.

The query returns the category name (category), the average total time in minutes (avgTotalTimeMinutes), the minimum and maximum total times (minTotalTimeMinutes and maxTotalTimeMinutes), and the average number of ingredients per recipe (avgIngredientsPerCategory).
The results are sorted by the average total time in ascending order, so categories with the least average total time appear first.
This query provides insights into recipe categories that require the least amount of preparation time, and includes the minimum and maximum preparation times and the average number of ingredients per recipe in each category. The results are ordered by the average total time, starting with categories that have the shortest average preparation time.

     ```cypher
     MATCH 
     (r:Recipe)-[:BELONGS_TO]->(c:RecipeCategory)
     WHERE 
     r.TotalTime IS NOT NULL
     MATCH 
     (r)-[:CONTAINS]->(i:Ingredient)
     WITH c, 
          r, 
          r.TotalTime.minutes AS totalTimeMinutes,
          COUNT(DISTINCT i) AS numIngredients
     WITH c, 
          AVG(totalTimeMinutes) AS avgTotalTimeMinutes,
          MIN(totalTimeMinutes) AS minTotalTimeMinutes,
          MAX(totalTimeMinutes) AS maxTotalTimeMinutes,
          AVG(numIngredients) AS avgIngredientsPerCategory
     RETURN 
     c.name AS category,
     tointeger(avgTotalTimeMinutes) AS avgTotalTimeMinutes,
     tointeger(minTotalTimeMinutes) AS minTotalTimeMinutes,
     tointeger(maxTotalTimeMinutes) AS maxTotalTimeMinutes,
     tointeger(avgIngredientsPerCategory) AS avgIngredientsPerCategory
     ORDER BY avgTotalTimeMinutes ASC;
     ```

## 8. Find the ingredients used in the recipes with highest ratings and return them ordered by avg rating weighted logarithmically on the number of reviews

This Cypher query identifies the ingredients used in the recipes with the highest ratings and orders them based on a weighted average rating. The weighting is logarithmically scaled by the number of reviews for each ingredient to balance the impact of popularity and rating quality.

- MATCH Clause:
Retrieves the relationship between ingredients (i), recipes (r), and reviews (review) by navigating through the graph structure.
The :CONTAINS relationship connects ingredients to recipes.
The :FOR relationship connects recipes to their reviews.
- WITH Clause:
Gathers the ingredient name (i.name) as Ingredient, the review rating (review.rating) as Rating, and the entire review node (review) for further computation.
- RETURN Clause:
Calculates the average rating for each ingredient (AvgRating) rounded to two decimal places.
Counts the total number of reviews for each ingredient (ReviewCount).
Orders the results by a calculated score: AvgRating * log10(ReviewCount). This formula weights the average rating by the logarithm of the number of reviews, emphasizing ingredients with higher reviews while mitigating the dominance of highly-rated but less-reviewed ingredients.
- ORDER BY Clause:
Sorts the results in descending order of the weighted score, prioritizing ingredients associated with highly rated and well-reviewed recipes.
- Output:
The result is a list of ingredients sorted by their significance in recipes with high ratings, where significance is determined by a combination of average rating and review volume. This is useful for identifying the most impactful ingredients in highly regarded recipes.

     ```cypher
     MATCH 
     (i:Ingredient)<-[:CONTAINS]-(r:Recipe)<-[:FOR]-(review:Review)
     WITH 
     i.name AS Ingredient,
     review.rating AS Rating,
     review
     RETURN 
     Ingredient,
     round(Avg(Rating), 2) AS AvgRating,
     COUNT(review) AS ReviewCount
     ORDER BY 
     AvgRating * log10(ReviewCount) DESC;
     ```

## 9. Given a set of ingredient that user don't like, find pairs of ingredients they like that are often in the same recipe, in order to suggest the user ingredients that match well together. The result is ordered by descending number of co.occurences
> INSERT INPUT

This query identifies pairs of ingredients the user likes that frequently appear together in recipes, excluding any ingredients the user dislikes. The aim is to suggest ingredient combinations that match well and might appeal to the user based on their preferences.

- WITH Clause:
Defines a list of ingredients the user dislikes (NotLikedIngredients) to filter them out from the query.
- MATCH Clause:
Finds pairs of ingredients (i1 and i2) contained in the same recipe (r) through the :CONTAINS relationship.
- WHERE Clause:
Ensures the query only considers pairs of ingredients where:
i1.name < i2.name: Prevents duplicate pairs (e.g., "A-B" and "B-A").
Neither ingredient is in the NotLikedIngredients list: Excludes undesired ingredients from the analysis.
- WITH Clause:
Groups data by ingredient pairs and the recipes in which they co-occur.
- RETURN Clause:
Returns the names of the paired ingredients (Ingredient1 and Ingredient2).
Calculates the number of distinct recipes where each pair appears together (CoOccurrenceCount).
- ORDER BY Clause:
Sorts the results by the number of co-occurrences in descending order, prioritizing the most frequent ingredient pairs.
- Output:
The query produces a ranked list of ingredient pairs that the user is likely to enjoy and that frequently appear together in recipes. This information can help generate suggestions for ingredient combinations that match well, potentially inspiring new recipes or meal ideas aligned with the user's preferences.

    ```cypher
     WITH 
     ['butter','cheese', 'pineapple'] AS NotLikedIngredients
     MATCH
     (i1:Ingredient)<-[:CONTAINS]-(r:Recipe)-[:CONTAINS]->(i2:Ingredient)
     WHERE
     i1.name < i2.name 
     AND NOT i1.name  IN NotLikedIngredients 
     AND NOT i2.name IN NotLikedIngredients
     WITH
     i1, i2, r
     RETURN
     i1.name AS Ingredient1,
     i2.name AS Ingredient2,
     COUNT(DISTINCT r) AS CoOccurrenceCount
     ORDER BY
     CoOccurrenceCount DESC
    ```

## 10. Diet recipe - given a set of ingredient that the recipe should contain, find the recipe under a certain treshold of calories with the best ratio for protein and lowest ratio for fat. Return in the result also the average rating of the recipe.

> INSERT INPUT

This query is designed to find diet-friendly recipes that meet the following criteria:

- Ingredient Inclusion: The recipe must contain specific ingredients, such as "chicken" and "spinach."

- Calorie Restriction: The recipe must have a total calorie count of 500 or less.

- High Protein and Low Fat:
The query calculates the protein ratio, carbohydrate ratio, and fat ratio for each recipe by dividing the respective macronutrient content by the total calories.
It then prioritizes recipes with the highest protein-to-fat efficiency, using the formula ProteinRatio * (1/FatRatio) for ranking.
- Positive Reviews: The recipe must have an average review rating of 4.0 or higher.

The query outputs the following details for each recipe that matches the criteria:

- RecipeName: The name of the recipe.
- AvgRating: The average review score for the recipe.
- ProteinRatio: The ratio of protein to total calories (rounded to two decimal places).
- CarboRatio: The ratio of carbohydrates to total calories (rounded to two decimal places).
- FatRatio: The ratio of fat to total calories (rounded to two decimal places).

Recipes are sorted by the highest protein-to-fat efficiency (ProteinRatio * (1/FatRatio)) in descending order, ensuring that recipes with the best protein-to-fat balance are prioritized.
This query is particularly useful for users seeking healthy recipes that:

- Contain specific ingredients.
- Stay within calorie limits.
- Maximize protein intake while minimizing fat content.
- Have been rated highly by other users.

    ```cypher
    MATCH 
    (recipe:Recipe)-[:CONTAINS]->(ingredient:Ingredient)
    MATCH 
    (recipe)<-[:FOR]-(review:Review)
    WHERE 
    ingredient.name IN ["chicken", "spinach"]  
    AND recipe.Calories <= 500
    WITH 
    recipe, 
    round(recipe.ProteinContent / recipe.Calories,2) AS protein_ratio,
    round(recipe.CarbohydrateContent / recipe.Calories,2) AS carbo_ratio,
    round(recipe.FatContent / recipe.Calories,2) AS fat_ratio,
    avg(review.rating) AS avg_review_rating
    WHERE 
    avg_review_rating >= 4
    RETURN 
    recipe.Name AS RecipeName, 
    avg_review_rating AS AvgRating, 
    protein_ratio AS ProteinRatio, 
    carbo_ratio AS CarboRatio, 
    fat_ratio AS FatRatio
    ORDER BY 
    ProteinRatio * (1/FatRatio) DESC;
    ```