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

## 2. Detect Trends
Keyword Trends Over Time: Find how often "vegan" recipes are being reviewed each year.
{
  "aggs": {
    "vegan_reviews_over_time": {
      "date_histogram": {
        "field": "reviews.date",
        "calendar_interval": "year"
      },
      "filter": {
        "term": { "reviews.comment": "vegan" }
      }
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


## 6. Recipes that contain "healthy snacks" or are high-protein but exclude "dessert."
{
  "query": {
    "bool": {
      "should": [
        { "match_phrase": { "description": "healthy snacks" } },
        { "range": { "protein": { "gte": 20 } } }
      ],
      "must_not": [
        { "term": { "tags.keyword": "dessert" } }
      ]
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
