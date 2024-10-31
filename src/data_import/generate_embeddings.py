import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np

# Load the dataset
file_path = "data/processed/articles_dataset.csv"
df = pd.read_csv(file_path)

# Initialize the sentence-transformers model
# You can replace 'all-MiniLM-L6-v2' with another model if needed
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define a function to create embeddings
def create_embedding(text):
    if pd.isnull(text):
        return np.nan  # Handle missing values if any
    return model.encode(text).tolist()  # Convert numpy array to list for easier storage

# Generate embeddings for each row and add them as new columns
df['title_embedding'] = df['title'].apply(create_embedding)
df['summary_embedding'] = df['summary'].apply(create_embedding)
df['content_embedding'] = df['content'].apply(create_embedding)

# Save the updated dataset to a new CSV file
output_file_path = "data/processed/aarticles_with_embeddings.csv"
df.to_csv(output_file_path, index=False)

print(f"Embeddings generated and saved to {output_file_path}")
