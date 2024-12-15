from elasticsearch import Elasticsearch
import random

# Connect to Bonsai Elasticsearch (replace with your Bonsai credentials)
bonsai_url = ""
es = Elasticsearch(bonsai_url)

# Define the index name
index_name = "recipeswithreviews"  # Name of your index

# Random query examples
queries = [
    {
        "query": {
            "match": {
                "RecipeCategory": "Dessert"
            }
        }
    }
]

# Select a random query from the list
random_query = random.choice(queries)

# Perform the search query
response = es.search(index=index_name, body=random_query)

# Print the response from Elasticsearch
print("Query Result:")
print(response)
