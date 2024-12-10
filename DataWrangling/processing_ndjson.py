import json

# Function to convert "c(...)" formatted strings into an array of text
def convert_to_array(c_string):
    if isinstance(c_string, str):
        # Remove 'c(' at the start and ')' at the end
        if c_string.startswith('c("') and c_string.endswith('")'):
            c_string = c_string[2:-2]  # Remove the 'c("...")' part
            # Split by '", "' and strip quotes from each item
            return [item.strip().strip('"') for item in c_string.split('", "')]
    return []  # Return an empty list if the format is invalid

# Function to process and convert the necessary fields in each recipe
def process_recipe(recipe):
    fields_to_convert = ['RecipeInstructions', 'RecipeIngredientParts', 'RecipeIngredientQuantities', 'Keywords']
    for field in fields_to_convert:
        if field in recipe and recipe[field]:
            recipe[field] = convert_to_array(recipe[field])
    return recipe

# Path to the input ndjson file
input_file = "./Dataset/recipes_with_reviews.ndjson"
output_file = "./Dataset/processed_recipes_with_reviews.ndjson"

# Open input file and output file
with open(input_file, "r", encoding="utf-8") as in_file, open(output_file, "w", encoding="utf-8") as out_file:
    for line in in_file:
        recipe = json.loads(line)
        processed_recipe = process_recipe(recipe)
        # Write the processed recipe to the output file
        json.dump(processed_recipe, out_file, ensure_ascii=False)
        out_file.write("\n")

print(f"Data processed and saved as {output_file}")
