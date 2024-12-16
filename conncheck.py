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
    "query": {
        "bool": {
            "should": [
                {
                    "match":
                        {
                            "RecipeIngredientParts":
                            {
                                "query": " ".join(ingredients),
                                "operator": "or"
                            }
                        }
                }
            ]
        }
    }
}
result = es.search(index=index_name, body=body, size=limit)
# print(result)
data = [{"matchingScore": record['_score']}
        for record in result['hits']['hits']]

print(data)
