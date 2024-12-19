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

## 1. Romantic dinner recipes 🔍
```json

GET /recipesandreviews/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "RecipeServings": {
              "gte": 2,
              "lte": 3
            }}}],
      "should": [
        {
          "nested": {
            "path": "Reviews",
            "query": {
              "match": {
                "Reviews.Review": {
                  "query": "romantic",
                  "boost": 2
                }}}}},
        {
          "match": {
            "Keywords": {
              "query": "romantic",
              "boost": 2
            }}},
        {
          "match": {
            "Description": {
              "query": "romantic",
              "boost": 2
            }}},
        {
          "range": {
            "AggregatedRating": {
              "gte": 3.5
            }}}]}}}

```

## 2. Recipes without an oven with microwave🔍📊

```json
GET /recipesandreviews/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "RecipeInstructions": "microwave"
          }}],
      "must_not": [
        {
          "match": {
            "Keywords": {
              "query": "oven pan pot fryer",
              "operator": "or"
            }}},
        {
          "match": {
            "RecipeInstructions": {
              "query": "oven pan pot fryer",
              "operator": "or"
            }}}],
      "should": [
        {
          "match": {
            "Keywords": "microwave"
          }},
        {
          "nested": {
            "path": "Reviews",
            "query": {
              "match": {
                "Reviews.Review": "microwave"
              }}}}]}}}

```

## 3. Quick Recipes Using All Given Ingredients
```json
GET /recipesandreviews/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "RecipeIngredientParts": {
              "query": "chicken onion cheese",
              "operator": "and"
            }}},
        {
          "range": {
            "TotalTime": {
              "lte": 30
            }}}]}}}
```


## 4. Recipes for a party with a lot of servings

```json
GET /recipesandreviews/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "RecipeServings": {
              "gte": 10
            }}}],
      "should": [
        {
          "match": {
            "Keywords": {
              "query": "party, large groups, gathering, celebration, 
              event, buffet",
              "operator": "or",
              "boost": 2
            }}},
        {
          "match": {
            "RecipeCategory": {
              "query": "Dessert, Appetizer, Main, Party, Buffet",
              "operator": "or",
              "boost": 1.5
            }}},
        {
          "match": {
            "Description": {
              "query": "party, large groups, gathering, celebration, event",
              "operator": "or",
              "boost": 1.5
            }}},
        {
          "nested": {
            "path": "Reviews",
            "query": {
              "match": {
                "Reviews.Review": {
                  "query": "party, celebration, gathering, event, buffet",
                  "operator": "or",
                  "boost": 3
                }}}}}],
      "minimum_should_match": 1
    }}}

```

## 5. Recipes with the best protein/calorie ratio

```json
GET /recipesandreviews/_search
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
            }}}],
      "should": [
        {
          "match": {
            "Description": {
              "query": "healthy gym protein fit strong weight nutritious",
              "operator": "or"
              }}},
        {
          "match": {
            "Keywords": {
              "query": "healthy gym protein fit strong weight nutritious",
              "operator": "or",
              "boost": 3
              }}},
        {
          "match": {
            "RecipeCategory": {
              "query": "healthy gym protein fit strong weight nutritious",
              "operator": "or"
              }}},
        {
          "nested": {
            "path": "Reviews",
              "query": {
                "match": {
                  "Reviews.Review": {
                    "query": "healthy gym protein fit strong weight nutritious",
                    "operator": "or"
                    }}}}}]}}}


```

# 6. Recipes for specific dietary restrictions (lactose intolerance)

```json
GET /recipesandreviews/_search
{
  "query": {
    "bool": {
      "must_not": [
        {
          "match": {
            "RecipeIngredientParts": {
              "query": "milk cheese lactose yogurt",
              "operator": "or"
            }}}],
      "should": [
        {
          "match": {
            "Keywords": "lactose free"
          }},
        {
          "match": {
            "Description": "lactose free intolerant"
          }},
        {
          "match": {
            "RecipeCategory": "lactose free"
          }},
        {
          "nested": {
            "path": "Reviews",
            "query": {
              "match": {
                "Reviews.Review": "lactose free intolerant"
              }}}}]}}}
```

## 7.Query to analyze the correlation between macronutrient ranges and calorie content
```json
GET /recipesandreviews/_search
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
        ]},
      "aggs": {
        "protein_ranges": {
          "range": {
            "field": "ProteinContent",
            "ranges": [
              { "to": 5, "key": "Low protein" },
              { "from": 5, "to": 15, "key": "Medium protein" },
              { "from": 15, "key": "High protein" }
            ]}},
        "fat_ranges": {
          "range": {
            "field": "FatContent",
            "ranges": [
              { "to": 5, "key": "Low fat" },
              { "from": 5, "to": 15, "key": "Medium fat" },
              { "from": 15, "key": "High fat" }
            ]}},
        "fiber_ranges": {
          "range": {
            "field": "FiberContent",
            "ranges": [
              { "to": 1, "key": "Low fiber" },
              { "from": 1, "to": 5, "key": "Medium fiber" },
              { "from": 5, "key": "High fiber" }
            ]}},
        "sugar_ranges": {
          "range": {
            "field": "SugarContent",
            "ranges": [
              { "to": 5, "key": "Low sugar" },
              { "from": 5, "to": 15, "key": "Medium sugar" },
              { "from": 15, "key": "High sugar" }
            ]}}}}}}
```


## 8. Healthy, high-protein snacks that are not desserts

```json
GET /recipesandreviews/_search
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
                }}}}},
        {
          "match": {
            "Keywords": {
              "query": "healthy snack"
            }}}],
      "must_not": [
        { "match":{"RecipeCategory": "dessert"} },
        { "match":{"Keywords": "dessert"} }
      ]}}}

```

## 9.Aggregation by author name of the authors with the best reviews

```json
GET /recipesandreviews/_search
{
  "size": 1,
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
                "query": "great excellent good amazing awesome delicious yummy",
                "operator": "or"
            }}}}}]}},
  "aggs": {
    "positive_sentiment_per_author": {
      "terms": {
        "field": "AuthorId"
      },
      "aggs": {
        "average_rating": {
          "avg": {
            "field": "AggregatedRating"
          }}}}}}

```
## 10. Easy, budget-friendly recipes ideal for students

```json
GET /recipesandreviews/_search
{
  "query": {
    "bool": {
      "should": [
          {"match":
            {
              "Description": {
                "query": "college student cheap easy",
                "operator": "or"
              }}},
          {"match":
            {
              "Keywords": {
                "query": " college student cheap easy",
                "operator": "or"
              }}},
          {"match":
            {
              "RecipeCategory": {
                "query": "college student cheap easy",
                "operator": "or"
              }}},
          {"nested":{
          "path": "Reviews",
          "query": {
            "match": {
              "Reviews.Review": {
                "query": "college student cheap easy",
                "operator": "or"
            }}}}}],
      "must_not": [
        {
          "range": {
            "TotalTime": {
              "gte": 60
            }}}],
      "minimum_should_match": 1
    }}}
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
