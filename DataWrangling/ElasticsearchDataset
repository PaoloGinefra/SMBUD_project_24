import pandas as pd
import re
import json
import math

# Funzione per convertire il tempo in minuti
def convert_duration_to_minutes(duration):
    if isinstance(duration, str):
        match = re.match(r"PT(\d+)H(\d+)M", duration)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            return hours * 60 + minutes
        elif "H" in duration:
            hours = int(duration[2:-1])
            return hours * 60
        elif "M" in duration:
            minutes = int(duration[2:-1])
            return minutes
    return 0

# Funzione per gestire i NaN e convertirli in None (null in JSON)
def handle_nan(value):
    """
    Converte NaN e altri valori speciali in None per JSON (diventa null).
    """
    if isinstance(value, float) and math.isnan(value):
        return None
    return value

# Carica i dataset con gestione delle rappresentazioni di valori mancanti
recipes_df = pd.read_csv("./Dataset/recipes(10000).csv", na_values=["", "NULL", "N/A"])
reviews_df = pd.read_csv("./Dataset/reviews(10000).csv", na_values=["", "NULL", "N/A"])

# Uniforma i tipi di dati
recipes_df = recipes_df.convert_dtypes()
reviews_df = reviews_df.convert_dtypes()

# Converte i tempi in minuti
recipes_df['CookTime'] = recipes_df['CookTime'].apply(convert_duration_to_minutes)
recipes_df['PrepTime'] = recipes_df['PrepTime'].apply(convert_duration_to_minutes)
recipes_df['TotalTime'] = recipes_df['TotalTime'].apply(convert_duration_to_minutes)

# Raggruppa le recensioni per RecipeId
reviews_grouped = reviews_df.groupby("RecipeId").apply(
    lambda x: x.to_dict(orient='records')
).to_dict()

# Trasforma il DataFrame delle ricette in una lista di dizionari
recipes_with_reviews = recipes_df.to_dict(orient='records')

# Aggiungi le recensioni a ciascuna ricetta
for recipe in recipes_with_reviews:
    recipe_id = recipe["RecipeId"]
    reviews = reviews_grouped.get(recipe_id, [])
    if reviews:  # Aggiungi solo se la lista di recensioni non è vuota
        recipe["Reviews"] = reviews

# Gestisci NaN (None) prima della scrittura nel JSON
recipes_with_reviews = [handle_nan(recipe) for recipe in recipes_with_reviews]

# Scrittura del JSON con gestione di NaN
output_file = "./Dataset/recipes_with_reviews.ndjson"
with open(output_file, "w", encoding="utf-8") as ndjson_file:
    for recipe in recipes_with_reviews:
        json_line = json.dumps(recipe, ensure_ascii=False, default=handle_nan)
        ndjson_file.write(json_line + "\n")


print("CSV data successfully processed and saved as JSON!")
