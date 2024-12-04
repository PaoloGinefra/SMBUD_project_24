import pandas as pd
import re
import json

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

df = pd.read_csv("./Dataset/recipes(10000).csv")

df['CookTime'] = df['CookTime'].apply(convert_duration_to_minutes)
df['PrepTime'] = df['PrepTime'].apply(convert_duration_to_minutes)
df['TotalTime'] = df['TotalTime'].apply(convert_duration_to_minutes)

json_data = df.to_json(orient='records', lines=True)

with open("./Dataset/recipes(10000WithTime).csv", "w") as json_file:
    json_file.write(json_data)

print("CSV data successfully processed and saved as JSON!")

