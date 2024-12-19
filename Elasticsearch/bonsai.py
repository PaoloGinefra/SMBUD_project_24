

from elasticsearch import Elasticsearch
import json

# Connessione a Elasticsearch
bonsai_url = ""
es = Elasticsearch(bonsai_url)

# Definire il nome dell'indice
index_name = "recipeswithreviews"

# Definire la configurazione del mapping per l'indice
index_body = {
    "mappings": {
        "properties": {
            "RecipeId": {"type": "keyword"},
            "Name": {"type": "text", "analyzer": "standard"},
            "AuthorId": {"type": "keyword"},
            "AuthorName": {"type": "text", "analyzer": "standard"},
            "CookTime": {"type": "integer"},
            "PrepTime": {"type": "integer"},
            "TotalTime": {"type": "integer"},
            "DatePublished": {"type": "date", "format": "strict_date_time"},
            "Description": {"type": "text", "analyzer": "standard"},
            "Images": {"type": "text", "index": False},
            "RecipeCategory": {"type": "text", "analyzer": "standard"},
            "Keywords": {"type": "text", "analyzer": "standard"},
            "RecipeIngredientQuantities": {"type": "text", "analyzer": "standard"},
            "RecipeIngredientParts": {"type": "text", "analyzer": "standard"},
            "AggregatedRating": {"type": "float"},
            "ReviewCount": {"type": "integer"},
            "Calories": {"type": "float"},
            "FatContent": {"type": "float"},
            "SaturatedFatContent": {"type": "float"},
            "CholesterolContent": {"type": "float"},
            "SodiumContent": {"type": "float"},
            "CarbohydrateContent": {"type": "float"},
            "FiberContent": {"type": "float"},
            "SugarContent": {"type": "float"},
            "ProteinContent": {"type": "float"},
            "RecipeServings": {"type": "float"},
            "RecipeYield": {"type": "text", "index": False},
            "RecipeInstructions": {"type": "text", "analyzer": "standard"},
            "Reviews": {
                "type": "nested", 
                "properties": {
                    "ReviewId": {"type": "keyword"},
                    "RecipeId": {"type": "keyword"},
                    "AuthorId": {"type": "keyword"},
                    "AuthorName": {"type": "text", "analyzer": "standard"},
                    "Rating": {"type": "float"},
                    "Review": {"type": "text", "analyzer": "standard"},
                    "DateSubmitted": {"type": "date", "format": "strict_date_time"},
                    "DateModified": {"type": "date", "format": "strict_date_time"}
                }
            }
        }
    }
}

# Verifica se l'indice esiste, altrimenti crealo
if not es.indices.exists(index=index_name):
    response = es.indices.create(index=index_name, body=index_body)
    print(f"Indice '{index_name}' creato con successo. Risposta:", response)
else:
    print(f"L'indice '{index_name}' esiste già.")
