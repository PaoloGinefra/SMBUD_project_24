from elasticsearch import Elasticsearch
import random
from dotenv import load_dotenv
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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

body ={
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

result = es.search(index=index_name, body=body, size=1)
# print(result)
data = [{"matchingScore": record['_score']}
        for record in result['hits']['hits']]

calorie_ranges = result['aggregations']['calorie_ranges']['buckets'] #prende i 3 bucket

# Inizializza matrici vuote
fatCorrelation = np.zeros((3, 3))
proteinCorrelation = np.zeros((3, 3))
fiberCorrelation = np.zeros((3, 3))
sugarCorrelation = np.zeros((3, 3))

# Header per colonne (categorie di calorie) e righe (sub-ranges)
column_headers = ["LowCalorie", "MediumCalorie", "HighCalorie"]
fat_row_headers = ["LowFat", "MediumFat", "HighFat"]
sugar_row_headers = ["LowSugar", "MediumSugar", "HighSugar"]
fiber_row_headers = ["LowFiber", "MediumFiber", "HighFiber"]
protein_row_headers = ["LowProtein", "MediumProtein", "HighProtein"]

# Riempimento delle matrici
i = 0
for calorie_range in calorie_ranges:
    # Riempimento Fat
    fat_ranges = calorie_range['fat_ranges']['buckets']
    for j, fat_range in enumerate(fat_ranges):
        fatCorrelation[j][i] = fat_range['doc_count']

    # Riempimento Sugar
    sugar_ranges = calorie_range['sugar_ranges']['buckets']
    for j, sugar_range in enumerate(sugar_ranges):
        sugarCorrelation[j][i] = sugar_range['doc_count']

    # Riempimento Fiber
    fiber_ranges = calorie_range['fiber_ranges']['buckets']
    for j, fiber_range in enumerate(fiber_ranges):
        fiberCorrelation[j][i] = fiber_range['doc_count']

    # Riempimento Protein
    protein_ranges = calorie_range['protein_ranges']['buckets']
    for j, protein_range in enumerate(protein_ranges):
        proteinCorrelation[j][i] = protein_range['doc_count']

    i += 1

# Creazione dei DataFrame fuori dal ciclo
dfFat = pd.DataFrame(fatCorrelation, columns=column_headers, index=fat_row_headers)
dfSugar = pd.DataFrame(sugarCorrelation, columns=column_headers, index=sugar_row_headers)
dfFiber = pd.DataFrame(fiberCorrelation, columns=column_headers, index=fiber_row_headers)
dfProtein = pd.DataFrame(proteinCorrelation, columns=column_headers, index=protein_row_headers)

# Stampa risultati
print("\nFat Correlation Matrix:")
print(dfFat)
print("\nFiber Correlation Matrix:")
print(dfFiber)
print("\nSugar Correlation Matrix:")
print(dfSugar)
print("\nProtein Correlation Matrix:")
print(dfProtein)

# Function to plot heatmap
def plot_heatmap(matrix, row_headers, column_headers, title, cmap="coolwarm"):
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        matrix,
        annot=True,  # Annotate cells with their values
        fmt=".1f",   # Format the annotations as floating-point numbers
        xticklabels=column_headers,
        yticklabels=row_headers,
        cmap=cmap,
        cbar=True
    )
    plt.title(title)
    plt.xlabel("Calorie Range")
    plt.ylabel("Subcategories")
    plt.show()

# Plot heatmaps for each matrix
'''
plot_heatmap(dfFat, fat_row_headers, column_headers, "Fat Heatmap")
plot_heatmap(dfFiber, fiber_row_headers, column_headers, "Fiber Heatmap")
plot_heatmap(dfSugar, sugar_row_headers, column_headers, "Sugar Heatmap")
plot_heatmap(dfProtein, protein_row_headers, column_headers, "Protein Heatmap")
'''

#Matrici normalizzate
for i in range(fatCorrelation.shape[1]):  # Itera sulle colonne
    total_documents = np.sum(fatCorrelation[:, i])  # Somma totale della colonna
    print(total_documents)
    if total_documents > 0:
        fatCorrelation[:, i] /= total_documents  # Normalizza (come percentuale)

dfFatNormalized = pd.DataFrame(fatCorrelation, columns=column_headers, index=protein_row_headers)
plot_heatmap(dfFatNormalized, fat_row_headers, column_headers, "Fat Normalized Heatmap")

for i in range(fiberCorrelation.shape[1]):  # Itera sulle colonne
    total_documents = np.sum(fiberCorrelation[:, i])  # Somma totale della colonna
    print(total_documents)
    if total_documents > 0:
        fiberCorrelation[:, i] /= total_documents  # Normalizza (come percentuale)

dfFiberNormalized = pd.DataFrame(fiberCorrelation, columns=column_headers, index=fiber_row_headers)
plot_heatmap(dfFiberNormalized, fiber_row_headers, column_headers, "Fiber Normalized Heatmap")

for i in range(sugarCorrelation.shape[1]):  # Itera sulle colonne
    total_documents = np.sum(sugarCorrelation[:, i])  # Somma totale della colonna
    print(total_documents)
    if total_documents > 0:
        sugarCorrelation[:, i] /= total_documents  # Normalizza (come percentuale)

dfSugarNormalized = pd.DataFrame(sugarCorrelation, columns=column_headers, index=sugar_row_headers)
plot_heatmap(dfSugarNormalized, sugar_row_headers, column_headers, "Sugar Normalized Heatmap")

for i in range(proteinCorrelation.shape[1]):  # Itera sulle colonne
    total_documents = np.sum(proteinCorrelation[:, i])  # Somma totale della colonna
    print(total_documents)
    if total_documents > 0:
        proteinCorrelation[:, i] /= total_documents  # Normalizza (come percentuale)

dfProteinNormalized = pd.DataFrame(proteinCorrelation, columns=column_headers, index=protein_row_headers)
plot_heatmap(dfProteinNormalized, protein_row_headers, column_headers, "Protein Heatmap")
