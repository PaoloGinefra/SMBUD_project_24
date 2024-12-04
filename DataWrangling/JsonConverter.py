import csv
import json

# File paths
csv_file_path = "./Dataset/recipes(10000).csv"
json_file_path = "./Dataset/recipes(10000).json"

# Elasticsearch index name
index_name = "your-index-name"

try:
    # Open the CSV file
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Open the JSON file
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            for row in csv_reader:
                # Add the index action
                action = {"index": {"_index": index_name}}
                json_file.write(json.dumps(action) + '\n')

                # Add the row data
                json_file.write(json.dumps(row, ensure_ascii=False) + '\n')
except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print(f"Conversion complete. JSON file saved to {json_file_path}.")
