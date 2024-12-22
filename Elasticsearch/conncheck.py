import json
from elasticsearch import Elasticsearch
import random
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to Bonsai Elasticsearch (replace with your Bonsai credentials)
bonsai_url = os.getenv(
    "BONSAI_URL"
)
print("Bonsai URL:", bonsai_url)
es = Elasticsearch(bonsai_url,
                   verify_certs=True)

print("Connected to Bonsai Elasticsearch:", es.info())

# Define the index name
index_name = "recipeswithreviews"  # Name of your index

# Random query examples
# queries = [
#     {
#         "query": {
#             "bool": {
#                 "should": [
#                     {
#                         "match": {
#                             "RecipeIngredientParts": {
#                                 "query": "apple, salt",
#                                 "operator": "or"
#                             }
#                         }
#                     }
#                 ]
#             }
#         },
#         "fields": ["Name"]
#     }
# ]

# # Select a random query from the list
# random_query = random.choice(queries)

# # Perform the search query
# response = es.search(index=index_name, body=random_query)

# # Print the response from Elasticsearch
# print("Query Result:")
# print(response)
# print([a["fields"] for a in response["hits"]["hits"]])

ingredients = ["apples"]
limit = 1
body = {
    "size": 0,
    "aggs": {
        "calorie_ranges": {
            "range": {
                "field": "Calories",
                "ranges": [
                    {"to": 1400, "key": "Low calorie"},
                    {"from": 1400, "to": 2000, "key": "Medium calorie"},
                    {"from": 2000, "key": "High calorie"}
                ]
            },
            "aggs": {
                "protein_ranges": {
                    "range": {
                        "field": "ProteinContent",
                        "ranges": [
                            {"to": 5, "key": "Low protein"},
                            {"from": 5, "to": 15, "key": "Medium protein"},
                            {"from": 15, "key": "High protein"}
                        ]
                    }
                },
                "fat_ranges": {
                    "range": {
                        "field": "FatContent",
                        "ranges": [
                            {"to": 5, "key": "Low fat"},
                            {"from": 5, "to": 15, "key": "Medium fat"},
                            {"from": 15, "key": "High fat"}
                        ]
                    }
                },
                "fiber_ranges": {
                    "range": {
                        "field": "FiberContent",
                        "ranges": [
                            {"to": 1, "key": "Low fiber"},
                            {"from": 1, "to": 5, "key": "Medium fiber"},
                            {"from": 5, "key": "High fiber"}
                        ]
                    }
                },
                "sugar_ranges": {
                    "range": {
                        "field": "SugarContent",
                        "ranges": [
                            {"to": 5, "key": "Low sugar"},
                            {"from": 5, "to": 15, "key": "Medium sugar"},
                            {"from": 15, "key": "High sugar"}
                        ]
                    }
                }
            }
        }
    }
}

result = es.search(index=index_name, body=body, size=limit)
print(json.dumps(result['aggregations'], indent=2))
data = [{"matchingScore": record['_score']}
        for record in result['hits']['hits']]

print(data)
