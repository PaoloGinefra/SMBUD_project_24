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
- Romantic dinner recipes 🔍
- Recipes for a party with a lot of servings🔍📊
- Recipes without an oven with air fryer🔍📊
- Recipes inspired by pop culture (movies, books, TV shows). 
- Recipes with whatever I have in my fridge 🔍
- Find the recipes with the best protein/calory ratio 🔍
- Recipes for Specific Dietary Restrictions 🔍
- Seasonal Recipes (Based on Ingredients or Holidays) 🔍
- Best Meal Plan for Nutritional Balance and Minimum Overlap 📊


## 1. Recipes that contain "healthy snacks" or are high-protein but exclude "dessert."

```json
GET /recipes_in/_search
{
  "query": {
    "bool": {
      "should": [
        { "match": { "Description": "healthy snacks" } },
        { "range": { "ProteinContent": { "gte": 20 } } }
      ],
      "must_not": [
        { "match":{"RecipeCategory": "dessert"} }
      ]
    }
  }
}
```

## 2.Aggregation by author name of the authors with the best reviews

```json
GET /reviews/_search
{
  "size": 0,
  "query": {
    "bool": {
      "should": [
        { "match": { "Review": "great" } },
        { "match": { "Review": "excellent" } },
        { "match": { "Review": "good" } },
        { "match": { "Review": "amazing" } },
        { "match": { "Review": "awesome" } }
      ]
    }
  },
  "aggs": {
    "positive_sentiment_per_author": {
      "terms": {
        "field": "AuthorId",
        "order": { "_count": "desc" }
      },
      "aggs": {
        "projected_name": {
          "top_hits": {
            "_source": {
              "includes": ["AuthorName"]
            },
            "size": 1
          }
        }
      }
    }
  }
}
```

## 3.Look for recipes that are easy and have a high rating

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

## 4.Finds contraddicting reviews with respects to the rating, either good reviews with a low rating or bad reviews with a high rating (nb: non va bene perche non trova cose che sono davvero contraddizioni)

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

## 5. are vegan recipes considered good?

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

## 6. Recipes with certain ingredients and appliances

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

## 2. Detect Trends

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

## 1. Count the frequency of positive or negative sentiment keywords in a document to derive sentiment.

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

## 3. "More Like This" Queries

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

## 4. Personalized Search

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

## 5. Analyze the average rating of recipes by cuisine and difficulty

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

## 7. Find recipes with similar steps / number of steps

## 8. Given in input some ingredients that the user has at home, search for the recipes with those ingredients and the highest rating.

## 9. Look for the users that made the worst reviews (both based on rating and on words used)

## 10. Identify Sentiment Patterns in Reviews

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
