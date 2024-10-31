import pandas as pd
import json

# List of input JSON files
json_files = ["data/raw/articles.json", "data/raw/articles2.json"]

# List to store the data from each file
data = []

# Loop through each JSON file and load the data
for file in json_files:
    try:
        with open(file, "r", encoding="utf-8") as f:
            articles = json.load(f)  # Load list of articles from JSON
            # Add each article dictionary to data list
            for article in articles:
                data.append({
                    "title": article.get("title", ""),
                    "summary": article.get("summary", ""),
                    "content": article.get("content", "")
                })
    except FileNotFoundError:
        print(f"Warning: {file} not found. Skipping this file.")
    except json.JSONDecodeError:
        print(f"Error: Could not parse {file}. Skipping this file.")

# Convert the data to a DataFrame
df = pd.DataFrame(data, columns=["title", "summary", "content"])

# Save the DataFrame to a CSV file
df.to_csv("data/processed/articles_dataset.csv", index=False, encoding="utf-8")

print("Dataset created and saved as articles_dataset.csv")
