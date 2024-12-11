Mistakes:
ID's should be keywords, not integers (slides)
## Mapping recipes and reviews
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
        "fields": {
          "raw": {
            "type": "keyword"
          }
        }
      },
      "RecipeIngredientQuantities": {
        "type": "text",
        "fields": {
          "raw": {
            "type": "keyword"
          }
        }
      },
      "RecipeIngredientParts": {
        "type": "text",
        "fields": {
          "raw": {
            "type": "keyword"
          }
        }
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
        "type": "float" //TODO: check if integer is better
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

## Mapping recipes

> TODO: Check date formatting

```json
PUT /recipes
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
        "type": "keyword"
      },
      "Keywords": {
        "type": "text",
        "fields": {
          "raw": {
            "type": "keyword"
          }
        }
      },
      "RecipeIngredientQuantities": {
        "type": "text",
        "fields": {
          "raw": {
            "type": "keyword"
          }
        }
      },
      "RecipeIngredientParts": {
        "type": "text",
        "fields": {
          "raw": {
            "type": "keyword"
          }
        }
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
        "type": "float" //TODO: check if integer is better
      },
      "RecipeYield": {
        "type": "text",
        "index": false
      },
      "RecipeInstructions": {
        "type": "text",
        "analyzer": "standard"
      }
    }
  }
}
```

# Reviews index

```json
PUT /reviews
{
  "mappings": {
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
```

- Find the recipes fit for meal prep 🔍
## 1. Romantic dinner recipes 🔍

> In order to find recipes for a romantic dinner we searched for those with a number of servings between 2 and 3 (fir for a dinner for 2 people depending on how much they eat) and we added a should clause to boost the ones that contain the word romantic either in the review, keyword or description, signaling that they were specificallt thought for that kind of event.

```json

GET /recipeswithreviews/_search
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

>In order to find recipes fit to host a party we looked for those that had a number of servings greater then 10 in a must clause. We also added a should clause to boost the recipes specifically designed for parties (since they mention words related to it either in the keywords, category, description or review)

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

> In order to find recipes that are made soley with a microwave we chose to use a must clause to find those recipes that ise a microwave in their instructions and a must not to filter out those who use any other appliance. Furthermore, we added a should clause to boost the recipes that also mention microwave in their keywords or reviews since this means that the microwave is considered an important step for them.

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
              "query": "oven pan pot air fryer",
              "operator": "or"
            }
          }
        },
        {
          "match": {
            "RecipeInstructions": {
              "query": "oven pan pot air fryer",
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

## 4. Recipes with whatever I have in my fridge 🔍
```json
GET /processed/_search
{
  "query": {
    "match": {
      "RecipeIngredientParts": {
        "query": "chicken onion cheese",
        "operator": "and"
      }
    }
  }
}
```
## 5. Find the recipes with the best protein/calory ratio 
```json
GET /processed/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "Calories": {
              "gte": 400,
              "lte": 600
            }
          }
        },
        {
          "range": {
            "ProteinContent": {
              "gte": 30,
              "lte": 30.7
            }
          }
        }
      ],
      "should": [
        {
          "match": {
            "Description": {
              "query": "healthy gym protein fit strong weight nutritious",
              "operator": "or",
              "boost": 1
            }
          }
        },
        {
          "match": {
            "Keywords": {
              "query": "healthy gym protein fit strong weight nutritious",
              "operator": "or",
              "boost": 2
            }
          }
        },
        {
          "match": {
            "RecipeCategory": {
              "query": "healthy gym protein fit strong weight nutritious",
              "operator": "or",
              "boost": 2
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
                  "operator": "or",
                  "boost": 1
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
```json
GET /processed/_search
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

## 7. Seasonal Recipes (Based on Ingredients or Holidays) 🔍
```json
GET /processed/_search
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

- Best Meal Plan for Nutritional Balance and Minimum Overlap 📊
- fuzzyness per typos


## 8. Recipes that contain "healthy snacks" or are high-protein but exclude "dessert."

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

```json
GET /recipesandreviews/_search
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

## 10. Popular recipes in a certain time interval
```json
GET /recipesandreviews/_search
{
  "query": {
    "nested": {
      "path": "Reviews",
      "query": {
        "range": {
          "Reviews.DateSubmitted": {
            "gte": "2010-01-01T00:00:00Z",
            "lt": "2011-01-01T00:00:00Z",
            "format": "strict_date_time"
          }
        }
      }
    }
  },
  "sort": [
    {
      "ReviewCount": {
        "order": "desc"
      }
    }
  ]
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
