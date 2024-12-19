Add:
Complesse
Check bonsai mapping


## Mapping recipes and reviews

> We defined the mapping for our index statically, avoiding the use of dynamic mapping to prevent potential issues. This mapping explicitly covers every attribute in our dataset and guarantees a well-defined structure for the documents stored in the index.
Fields such as RecipeId, AuthorId, and ReviewId were set as type keyword, as they contain structured, consistent content that does not require analysis or tokenization for search purposes. For fields containing textual content, such as names, instructions, and reviews, we used the text field type and applied the standard analyzer. This allows Elasticsearch to perform full-text searches and relevance-based querying.
Numerical fields, like the ones for quantities and times, were mapped as either float or integer, depending on the specific requirements of the data. Dates in the dataset were defined as date fields with the "strict_date_time" format, that matches the dataset’s date representation. The strict_date_time format follows the pattern yyyy-MM-dd'T'HH:mm:ss.SSSZ, for example, 2023-12-17T15:30:00.000Z.
In our mapping, certain fields are configured with "index": false. This setting ensures that these fields are not searchable or usable in filtering operations.

```json
PUT /recipesandreviews
{
  "mappings": {
    "properties": {
      "RecipeId": {
        "type": "keyword"
      },
      "Name": {
        "type": "text",
        "analyzer": "standard"
      },
      "AuthorId": {
        "type": "keyword"
      },
      "AuthorName": {
        "type": "text",
        "analyzer": "standard"
      },
      "CookTime": {
        "type": "integer"
      },
      "PrepTime": {
        "type": "integer"
      },
      "TotalTime": {
        "type": "integer"
      },
      "DatePublished": {
        "type": "date",
        "format": "strict_date_time"
      },
      "Description": {
        "type": "text",
        "analyzer": "standard"
      },
      "Images": {
        "type": "text",
        "index": false
      },
      "RecipeCategory": {
        "type": "text",
        "analyzer": "standard"
      },
      "Keywords": {
        "type": "text",
        "analyzer": "standard"
      },
      "RecipeIngredientQuantities": {
        "type": "text",
        "analyzer": "standard"
      },
      "RecipeIngredientParts": {
        "type": "text",
        "analyzer": "standard"
      },
      "AggregatedRating": {
        "type": "float"
      },
      "ReviewCount": {
        "type": "integer"
      },
      "Calories": {
        "type": "float"
      },
      "FatContent": {
        "type": "float"
      },
      "SaturatedFatContent": {
        "type": "float"
      },
      "CholesterolContent": {
        "type": "float"
      },
      "SodiumContent": {
        "type": "float"
      },
      "CarbohydrateContent": {
        "type": "float"
      },
      "FiberContent": {
        "type": "float"
      },
      "SugarContent": {
        "type": "float"
      },
      "ProteinContent": {
        "type": "float"
      },
      "RecipeServings": {
        "type": "float"
      },
      "RecipeYield": {
        "type": "text",
        "index": false
      },
      "RecipeInstructions": {
        "type": "text",
        "analyzer": "standard"
      },
      "Reviews": {
        "type": "nested", 
        "properties": {
          "ReviewId": {
            "type": "keyword"
          },
          "RecipeId": {
            "type": "keyword"
          },
          "AuthorId": {
            "type": "keyword"
          },
          "AuthorName": {
            "type": "text",
            "analyzer": "standard"
          },
          "Rating": {
            "type": "float"
          },
          "Review": {
            "type": "text",
            "analyzer": "standard"
          },
          "DateSubmitted": {
            "type": "date",
            "format": "strict_date_time"
          },
          "DateModified": {
            "type": "date",
            "format": "strict_date_time"
          }
        }
      }
    }
  }
}

```

- Find the recipes fit for meal prep 🔍
## 1. Romantic dinner recipes 🔍

> To identify recipes suitable for a romantic dinner, we designed a search query that targets recipes with a specific number of servings and prioritizes those explicitly associated with romance. This approach ensures that the results are both practical and relevant for a special evening.

>The query is structured as a compund query, since we wanted to combine different factors to have a better fitting output.

>Firstly, we used a must query, which enforces that the RecipeServings field has a value between 2 and 3. This range corresponds to a meal for two people, accommodating varying portion sizes depending on individual appetites.

>In addition to this, we added a should clause to boost the relevance of recipes that are specifically associated with romantic themes. The boosting mechanism ensures that recipes explicitly labeled or described as romantic are ranked higher in the search results. The should clause includes the following conditions:

>Reviews: Recipes receive a boost if the word "romantic" appears in any of their reviews. To achieve this, we use a nested query that navigates into the Reviews object and matches the Review field for the term "romantic." This captures user feedback or sentiments indicating that the recipe has been perceived as good for romantic occasions.

>Keywords: Recipes are boosted if the Keywords field contains the term "romantic." This field often contains tags or descriptive phrases added by the recipe creator, providing a direct indication of the recipe's intended use or audience.

>Description: Recipes with the term "romantic" in the Description field are also given a higher ranking. This ensures that recipes designed for romantic occasions, as described by the author, are prioritized in the results.

>Aggregated Rating: To ensure quality, recipes with an AggregatedRating of 3.5 or higher receive additional weighting. This ensures that highly rated recipes, which are more likely to provide a positive experience, are given preference in the results. 
We chose to not give a boost to this last query since it's not as important as the others for the purpose of this search.

>This query strategically boosts the recipes that are thematically aligned with romantic occasions, as indicated by user reviews, keywords, or descriptions. The inclusion of a rating filter further enhances the quality of the results, ensuring that users receive both relevant and well-regarded recipes.

```json

GET /recipeswithreviewsfinal/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "RecipeServings": {
              "gte": 2,
              "lte": 3
            }
          }
        }
      ],
      "should": [
        {
          "nested": {
            "path": "Reviews",
            "query": {
              "match": {
                "Reviews.Review": {
                  "query": "romantic",
                  "boost": 2
                }
              }
            }
          }
        },
        {
          "match": {
            "Keywords": {
              "query": "romantic",
              "boost": 2
            }
          }
        },
        {
          "match": {
            "Description": {
              "query": "romantic",
              "boost": 2
            }
          }
        },
        {
          "range": {
            "AggregatedRating": {
              "gte": 3.5
            }
          }
        }
      ]
    }
  }
}

```

## 2. Recipes for a party with a lot of servings🔍📊

>To find recipes suitable for hosting a party, we focused on identifying those that serve a larger number of people. In the must clause, we specified that the recipes should have a RecipeServings greater than or equal to 10, ensuring that they are fit for a gathering. Additionally, we applied a should clause to give extra weight to recipes that explicitly reference terms associated with parties and large events, such as "party," "large groups," "gathering," "celebration," "buffet," and similar phrases.

>The should clause includes several fields where these keywords might appear, enhancing the relevance of the search results. For example, the Keywords field is searched for terms like "party" and "celebration," with a boost of 2, emphasizing recipes designed with these themes in mind. The RecipeCategory field is also considered, with a boost of 1.5 for categories such as "Party," "Buffet," and "Appetizer," since these are often associated with party-friendly meals. Similarly, the Description field is searched for party-related terms with a boost of 1.5 to highlight recipes that mention large gatherings or events.

>Lastly, we included the Reviews field, specifically searching within the nested Reviews.Review subfield for mentions of party-related terms. These reviews are boosted with a higher weight (boost of 3) to prioritize recipes that have been greatly appreciated for parties since we thought that in this context the reviews are the most important parameter to account for.

>By using this approach, we can ensure that recipes most relevant for parties are given a higher score in the search results, while also only getting those that are designed to serve a larger number of people. The minimum_should_match parameter is set to 1, ensuring that at least one of the should conditions is be satisfied for a recipe to be returned in the results.

```json
GET /recipeswithreviews/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "RecipeServings": {
              "gte": 10
            }
          }
        }
      ],
      "should": [
        {
          "match": {
            "Keywords": {
              "query": "party, large groups, gathering, celebration, event, buffet",
              "operator": "or",
              "boost": 2
            }
          }
        },
        {
          "match": {
            "RecipeCategory": {
              "query": "Dessert, Appetizer, Main, Party, Buffet",
              "operator": "or",
              "boost": 1.5
            }
          }
        },
        {
          "match": {
            "Description": {
              "query": "party, large groups, gathering, celebration, event",
              "operator": "or",
              "boost": 1.5
            }
          }
        },
        {
          "nested": {
            "path": "Reviews",
            "query": {
              "match": {
                "Reviews.Review": {
                  "query": "party, celebration, gathering, event, buffet",
                  "operator": "or",
                  "boost": 3
                }
              }
            }
          }
        }
      ],
      "minimum_should_match": 1
    }
  }
}

```

## 3. Recipes without an oven with microwave🔍📊

> This query is designed to help a student who only has a microwave and no other appliances find recipes that can be made exclusively with a microwave.

>In the must clause, we ensure that the RecipeInstructions field contains the word "microwave", confirming that the recipe involves using the microwave for cooking. To further refine the search, we added a must_not clause to exclude any recipes that mention the use of other appliances, such as an oven, pan, pot, or fryer, in the Keywords or RecipeInstructions fields. This ensures that only recipes that rely solely on the microwave are included in the results.

>Additionally, the should clause is used to give a higher score to recipes that highlight the microwave as a key element. We search for the term "microwave" in the Keywords and in the Reviews.Review field, as they indicate that the microwave is an important part of the recipe according to either the recipe creator or reviewers.

>This approach ensures that the student will find recipes that are specifically designed for a microwave, without needing any additional cooking appliances, and gives extra weight to those that emphasize the microwave's role in the cooking process. We chose to not put a minimum should match since here the only foundamental parameters are those in the must and must not clause.

```json
GET /recipeswithreviews/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "RecipeInstructions": "microwave"
          }
        }
      ],
      "must_not": [
        {
          "match": {
            "Keywords": {
              "query": "oven pan pot fryer",
              "operator": "or"
            }
          }
        },
        {
          "match": {
            "RecipeInstructions": {
              "query": "oven pan pot fryer",
              "operator": "or"
            }
          }
        }
      ],
      "should": [
        {
          "match": {
            "Keywords": "microwave"
          }
        },
        {
          "nested": {
            "path": "Reviews",
            "query": {
              "match": {
                "Reviews.Review": "microwave"
              }
            }
          }
        }
      ]
    }
  }
}

```

- Recipes inspired by pop culture (movies, books, TV shows). 

## 4. Recipes with whatever I have in my fridge 🔍 add script to count
>This query is designed for a student who has chicken, onion, and cheese in their fridge and wants to find quick recipes that can be prepared in 30 minutes or less. The must clause specifies that the recipes should contain all three ingredients (chicken, onion, and cheese) using an "and" operator to ensure that all the specified ingredients are included in the recipe.

>To make sure the recipes are quick, the query also includes a range filter on the PrepTime field, restricting the results to recipes where the PrepTime is 30 minutes or less. This ensures that only quick meals are returned in the search results.
```json
GET /recipeswithreviewsfinal/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "RecipeIngredientParts": {
              "query": "chicken onion cheese",
              "operator": "and"
            }
          }
        },
        {
          "range": {
            "TotalTime": {
              "lte": 30
            }
          }
        }
      ]
    }
  }
}
```
## 5. Recipes with the Best Protein-Calorie Intake

>This query identifies recipes that have a high protein-to-calorie ratio while aligning with health-conscious and fitness-focused preferences. The main criteria is specified in the must clause, where the query filters for recipes with a protein-to-calorie ratio (pcratio) of at least 0.2, ensuring the selected recipes provide a significant amount of protein relative to their calorie content.

To enhance the ranking of recipes that resonate with fitness and health goals, the query includes should clauses that boost relevance based on the presence of specific keywords. These keywords, such as "healthy," "gym," "protein," "fit," "strong," "weight," and "nutritious," are searched within the Description, Keywords, and RecipeCategory fields. Matches in these fields increase the recipe's score, with additional emphasis placed on matches in the Keywords field through a boost factor. The query also examines the Reviews field, looking for mentions of the same health-oriented terms within user reviews, further contributing to a recipe's relevance score.

By combining the strict nutritional filter with keyword-based scoring, the query prioritizes recipes that meet the protein-to-calorie ratio threshold and are described or reviewed in a way that appeals to health-conscious or fitness-oriented users. Recipes with more keyword matches or relevant reviews are ranked higher, ensuring that the most nutritious and health-aligned options appear prominently in the results.
```json
GET /recipeswithreviewsfinal/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "script": {
            "script": {
              "source": """
                if (doc['Calories'].size() > 0 && doc['Calories'].value != 0) {
                  return doc['ProteinContent'].value / doc['Calories'].value >= 0.2;
                } else {
                  return false;
                }
              """
            }
          }
        }
      ],
      "should": [
        {
          "match": {
            "Description": {
              "query": "healthy gym protein fit strong weight nutritious",
              "operator": "or"
              }
            }
          },
        {
          "match": {
            "Keywords": {
              "query": "healthy gym protein fit strong weight nutritious",
              "operator": "or",
              "boost": 3
              }
            }
          },
        {
          "match": {
            "RecipeCategory": {
              "query": "healthy gym protein fit strong weight nutritious",
              "operator": "or"
              }
            }
          },
        {
          "nested": {
            "path": "Reviews",
              "query": {
                "match": {
                  "Reviews.Review": {
                    "query": "healthy gym protein fit strong weight nutritious",
                    "operator": "or"
                    }
                  }
                }
              }
            }
      ]
    }
  }
}


```

# 6. Recipes for Specific Dietary Restrictions 🔍
>This query is designed to find recipes suitable for individuals with lactose intolerance or those following a lactose-free diet. The search first excludes any recipes containing common sources of lactose, such as milk, cheese, lactose, and yogurt, using the must_not clause. This ensures that recipes with these ingredients are filtered out, as they are not appropriate for people who need to avoid lactose.

>In addition to filtering out lactose-containing ingredients, the query uses a should clause to boost the relevance of recipes that explicitly mention being lactose-free or suitable for those with lactose intolerance. It looks for these terms in the Keywords, Description, and RecipeCategory fields, as well as in Reviews. The query searches for terms like "lactose free" and "lactose intolerant" across these fields to give higher scores to recipes that are clearly labeled as suitable for those with lactose restrictions. This helps prioritize lactose-free recipes, making it easier for users to find meals that meet their dietary needs.
```json
GET /recipeswithreviewsfinal/_search
{
  "query": {
    "bool": {
      "must_not": [
        {
          "match": {
            "RecipeIngredientParts": {
              "query": "milk cheese lactose yogurt",
              "operator": "or"
            }
          }
        }
      ],
      "should": [
        {
          "match": {
            "Keywords": "lactose free"
          }
        },
        {
          "match": {
            "Description": "lactose free intolerant"
          }
        },
        {
          "match": {
            "RecipeCategory": "lactose free"
          }
        },
        {
          "nested": {
            "path": "Reviews",
            "query": {
              "match": {
                "Reviews.Review": "lactose free intolerant"
              }
            }
          }
        }
      ]
    }
  }
}
```
## ?. How the popularity an ingredient changed in years
```json
GET /recipeswithreviewsfinal/_search
{
  "size": 1,
  "query":{
    "match": {
      "RecipeIngredientParts": "corn"
      }
    },
  "aggs": {
    "by_review_year": {
      "date_histogram": {
        "field": "DatePublished",
        "calendar_interval": "year",
        "format": "yyyy"
      }
    }
  }
}
```


## ?. Seasonal Recipes (Based on Ingredients or Holidays) 🔍
>This query is structured using a bool query with a should clause to enhance the relevance of recipes related to specific seasonal occasions, particularly focusing on Christmas and winter holidays. The should clause means that at least one of the conditions inside it must be met for a recipe to be included in the results, but the more conditions it matches, the higher the score and priority of the recipe.

>Within the should clause, the query searches across four fields: Reviews, Description, Keywords, and RecipeCategory. These fields are examined for terms related to the holiday season, such as "christmas," "festivities," "winter," "cozy," and "holidays."
>For each of these fields, the query uses a match query with an operator set to "or". This allows the query to find any of these holiday-related terms individually within the field. For example, if a recipe description contains the word "cozy" or "christmas," it will still be included in the results. The "or" operator increases the flexibility of the query, allowing it to match any one of the given words in the field.
>Additionally, the query checks Reviews using a nested query. Since reviews are stored as a nested object, the query specifically searches the Reviews.Review field for holiday-related terms. This ensures that recipes with relevant seasonal mentions in reviews (like user comments on winter or holiday-themed dishes) are also prioritized.
```json
GET /recipeswithreviewsfinal/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "nested": {
            "path": "Reviews",
            "query": {
              "match": {
                "Reviews.Review": {
                  "query": "christmas festivities winter cozy holidays",
                  "operator": "or"
                }
              }
            }
          }
        },
        {
          "match": {
            "Description": {
              "query": "christmas festivities winter cozy holidays",
              "operator": "or"
            }
          }
        },
        {
          "match": {
            "Keywords": {
              "query": "christmas festivities winter cozy holidays",
              "operator": "or"
            }
          }
        },
        {
          "match": {
            "RecipeCategory": {
              "query": "christmas festivities winter cozy holidays",
              "operator": "or"
            }
          }
        }
      ]
    }
  }
}

```

## 7.Recipes grouped by calorie ranges and for each calorie range we see the protein sugar fat fiber ranges inside
```json
GET /recipeswithreviewsfinal/_search
{
  "size": 0,
  "aggs": {
    "calorie_ranges": {
      "range": {
        "field": "Calories",
        "ranges": [
          { "to": 1400, "key": "Low calorie" },
          { "from": 1400, "to": 2000, "key": "Medium calorie" },
          { "from": 2000, "key": "High calorie" }
        ]
      },
      "aggs": {
        "protein_ranges": {
          "range": {
            "field": "ProteinContent",
            "ranges": [
              { "to": 5, "key": "Low protein" },
              { "from": 5, "to": 15, "key": "Medium protein" },
              { "from": 15, "key": "High protein" }
            ]
          }
        },
        "fat_ranges": {
          "range": {
            "field": "FatContent",
            "ranges": [
              { "to": 5, "key": "Low fat" },
              { "from": 5, "to": 15, "key": "Medium fat" },
              { "from": 15, "key": "High fat" }
            ]
          }
        },
        "fiber_ranges": {
          "range": {
            "field": "FiberContent",
            "ranges": [
              { "to": 1, "key": "Low fiber" },
              { "from": 1, "to": 5, "key": "Medium fiber" },
              { "from": 5, "key": "High fiber" }
            ]
          }
        },
        "sugar_ranges": {
          "range": {
            "field": "SugarContent",
            "ranges": [
              { "to": 5, "key": "Low sugar" },
              { "from": 5, "to": 15, "key": "Medium sugar" },
              { "from": 15, "key": "High sugar" }
            ]
          }
        }
      }
    }
  }
}
```


## 8. Recipes that contain "healthy snacks" or are high-protein but exclude "dessert."

>This query is designed to find snack recipes that are specifically healthy and high in protein, while excluding any recipes that fall under the dessert category. It starts by using the must clause to filter recipes that fall into the "Snacks" category and contain at least 20 grams of protein. These two conditions ensure that the results are relevant to the searcher's criteria for protein-packed snacks.

>In addition to these foundational requirements, the query includes a should clause to boost recipes that explicitly reference "healthy snack" in the description, reviews, or keywords. The use of the operator: "and" within the match queries means that the terms "healthy" and "snack" must both be present in these fields, increasing the likelihood of finding recipes that are truly aligned with the searcher's goal of a healthy, protein-rich snack.

>Furthermore, the query includes a must_not clause to explicitly exclude recipes that are categorized as "dessert" or contain the term "dessert" in their keywords. This is important because the user wants to avoid any recipes that may be high in sugar or calories, which are often found in dessert items.
```json
GET /recipeswithreviewsfinal/_search
{
  "query": {
    "bool": {
      "must":[
        {"match": {"RecipeCategory": "Snacks"}},
        {"range": { "ProteinContent": { "gte": 20 } } }
      ],
      "should": [
        { "match": { 
            "Description": {
              "query": "healthy snack",
              "operator": "and"
            } } },
        {
          "nested": {
            "path": "Reviews",
            "query": {
              "match": {
                "Reviews.Review": {
                  "query": "healthy snack",
                  "operator": "and"
                }
              }
            }
          }
        },
        {
          "match": {
            "Keywords": {
              "query": "healthy snack"
            }
          }
        }
      ],
      "must_not": [
        { "match":{"RecipeCategory": "dessert"} },
        { "match":{"Keywords": "dessert"} }
      ]
    }
  }
}

```

## 9.Aggregation by author name of the authors with the best reviews

>This query is designed for users who are looking to find accredited recipe authors to be inspired by, based on the quality of their recipes and the positive feedback they receive. By identifying authors with the best-reviewed recipes, this query helps users discover trustworthy sources for highly-rated dishes.

>The search starts with a must clause to ensure that only recipes with an AggregatedRating of 4 or higher are included, meaning the recipes are highly rated. Additionally, it filters out recipes with fewer than 10 reviews using a range query within the must clause on the ReviewCount field. This ensures that the results represent recipes that are well-reviewed by a significant number of people, giving a more reliable picture of the author's reputation.

>To further refine the results, the query includes a nested query within the Reviews field, looking for specific positive terms such as "great," "excellent," "good," "amazing," and "awesome." This helps identify recipes that have reviews with a positive sentiment. The operator: "or" in the query ensures that any of these positive words will contribute to the match, making it easier to capture a variety of positive sentiments across different reviews.

>The aggregation part of the query then groups the results by AuthorId using a terms aggregation, which enables the query to list authors who have the best reviews. Within each author group, the average_rating aggregation computes the average AggregatedRating for their recipes. This provides a way to rank authors based on the quality of their work, specifically those who consistently receive high ratings.

```json
GET /recipeswithreviewsfinal/_search
{
  "size": 2,
  "query": {
    "bool": {
      "must": [
        {"range": { "AggregatedRating": { "gte": 4} } },
        {"range": { "ReviewCount": { "gte": 10 } } },
        {"nested":{
          "path": "Reviews",
          "query": {
            "match": {
              "Reviews.Review": {
                "query": "great excellent good amazing awesome",
                "operator": "or"
            }
          }
        }}}
      ]
    }
  },
  "aggs": {
    "positive_sentiment_per_author": {
      "terms": {
        "field": "AuthorId"
      },
      "aggs": {
        "average_rating": {
          "avg": {
            "field": "AggregatedRating"
          }
        }
      }
    }
  }
}

```
## 10. Meals for students
This query is designed to find recipes that are ideal for college students looking for affordable and easy meal options. The query searches for recipes that are tagged with keywords or descriptions related to "college student," "cheap," and "easy." These terms are used in various fields such as the Description, Keywords, and RecipeCategory to ensure that the results are tailored to the needs of students who are on a budget and looking for simple meal ideas. Additionally, the query looks within Reviews to capture any references to these themes, which helps in identifying recipes that other students have positively reviewed for being cost-effective and easy to prepare.

To ensure the recipes are practical for busy students, the query includes a must_not clause that filters out recipes requiring more than 60 minutes of preparation time. This ensures that only quick and efficient recipes are returned, as students often don’t have the luxury of long cooking times. The use of the minimum_should_match parameter ensures that the query returns recipes that meet at least one of the keyword or descriptive criteria, providing a diverse set of relevant results.

In summary, this query helps college students find recipes that are inexpensive, easy to make, and ideal for individuals with limited time and resources.
```json
GET /recipeswithreviewsfinal/_search
{
  "query": {
    "bool": {
      "should": [
          {"match":
            {
              "Description": {
                "query": "college student cheap easy",
                "operator": "or"
              }
            }
          },
          {"match":
            {
              "Keywords": {
                "query": " college student cheap easy",
                "operator": "or"
              }
            }
          },
          {"match":
            {
              "RecipeCategory": {
                "query": "college student cheap easy",
                "operator": "or"
              }
            }
          },
          {"nested":{
          "path": "Reviews",
          "query": {
            "match": {
              "Reviews.Review": {
                "query": "college student cheap easy",
                "operator": "or"
            }
          }
        }}}
      ],
      "must_not": [
        {
          "range": {
            "TotalTime": {
              "gte": 60
            }
          }
        }
      ],
      "minimum_should_match": 1
    }
  }
}
```









## Look for recipes that are easy and have a high rating

```json
GET /reviews/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "Rating": {
              "gte": 4
            }
          }
        },
        {
          "match": {
            "Review": {
              "query": "easy quick fast simple cheap",
              "operator": "or"
            }
          }
        }
      ]
    }
  }
}
```

## Finds contraddicting reviews with respects to the rating, either good reviews with a low rating or bad reviews with a high rating (nb: non va bene perche non trova cose che sono davvero contraddizioni)

```json
GET /reviews/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "bool": {
            "must": [
              {"range": {"Rating": {"gte": 4}}},
              {"match": {
                "Review": {
                  "query": "bad hideous disgusting awful terrible horrible",
                  "operator": "or"
                }
              }}
            ],
            "must_not": [
              {
                "match": {
                  "Review": {
                    "query": "not quite good amazing",
                    "operator": "or"
                  }
                }
              }
            ]
          }
        },
        {
          "bool": {
            "must": [
              {"range": {"Rating": {"lte": 1}}},
              {"match": {
                "Review": {
                  "query": "good amazing spectacular perfect super -bad",
                  "operator": "or"
                }
              }}
            ],
            "must_not": [
              {
                "match": {
                  "Review": {
                    "query": "bad awful not",
                    "operator": "or"
                  }
                }
              }
            ]
          }
        }
      ]
    }
  }
}

```

## are vegan recipes considered good?

```json
GET /reviews/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "match": {
            "Review": "Vegan"
          }
        }
      ],
      "should": [
        {
          "range": {
            "Rating": {
              "gte": 4
            }
          }
        },
        {
          "match": {
            "Review": {
              "query": "good amazing spectacular perfect super",
              "operator": "or"
            }
          }
        }
      ],
      "minimum_should_match": 1
    }
  }
}
```

## Recipes with certain ingredients and appliances

```json
GET /recipes/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "RecipeIngredientParts": "chicken"
          }
        },
        {
          "match": {
            "RecipeIngredientParts": "tomato"
          }
        },
        {
          "match": {
            "RecipeIngredientParts": "onion"
          }
        },
        {
          "match": {
            "RecipeIngredientParts": "salt"
          }
        }
      ],
      "should": [
        {
          "match": {
            "RecipeInstructions": "oven"
          }
        },
        {
          "match": {
            "RecipeInstructions": "pan"
          }
        }
      ],
      "filter": [
        {
          "range": {
            "AggregatedRating": {
              "gte": 4.5
            }
          }
        }
      ]
    }
  }
}
```

## Analyze the average rating of recipes by cuisine or difficulty

## Detect Trends

Keyword Trends Over Time: Find how often "vegan" recipes are being reviewed each year.
GET /recipes_in/\_search
{
"query": {
"term": {
"Keywords.keyword": "vegan"
}
},
"aggs": {
"vegan_reviews_over_time": {
"date_histogram": {
"field": "DatePublished",
"calendar_interval": "year"
}
}
}
}

## Count the frequency of positive or negative sentiment keywords in a document to derive sentiment.

{
"aggs": {
"positive_words": {
"terms": { "field": "review_text", "include": ["great", "awesome", "happy"] }
},
"negative_words": {
"terms": { "field": "review_text", "include": ["bad", "terrible", "horrible"] }
}
}
}

## "More Like This" Queries

{
"query": {
"more_like_this": {
"fields": ["description", "ingredients"],
"like": "A delicious and moist chocolate cake",
"min_term_freq": 1,
"max_query_terms": 12
}
}
}

## Personalized Search

Use Case: Recommend recipes based on a user’s preferences (e.g., high protein and low carb).
{
"query": {
"bool": {
"must": [
{ "range": { "protein": { "gte": 20 } } },
{ "range": { "carbs": { "lte": 10 } } }
],
"should": [
{ "match": { "cuisine": "Mediterranean" } },
{ "match": { "difficulty": "easy" } }
]
}
}
}

## Analyze the average rating of recipes by cuisine and difficulty

{
"aggs": {
"by_cuisine": {
"terms": { "field": "cuisine.keyword" },
"aggs": {
"by_difficulty": {
"terms": { "field": "difficulty.keyword" },
"aggs": {
"average_rating": {
"avg": { "field": "average_rating" }
}
}
}
}
}
}
}

## Find recipes with similar steps / number of steps

## Given in input some ingredients that the user has at home, search for the recipes with those ingredients and the highest rating.

## Look for the users that made the worst reviews (both based on rating and on words used)

## Identify Sentiment Patterns in Reviews

{
"query": {
"bool": {
"must": [
{ "match": { "review_text": "delicious amazing" } },
{ "match": { "review_text": "awful terrible" } }
],
"boost": 2,
"should": [
{ "match_phrase": { "review_text": "not good" } },
{ "match_phrase": { "review_text": "never again" } }
],
"minimum_should_match": 1
}
}
}
