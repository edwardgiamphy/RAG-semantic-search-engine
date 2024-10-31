import pandas as pd
import numpy as np
import faiss
import pickle

# Load the embeddings CSV file
df = pd.read_csv("data/processed/articles_with_embeddings.csv")

# Filter out rows with invalid content embeddings
def parse_embedding(embedding_str):
    try:
        embedding = np.array(eval(embedding_str))
        if embedding.dtype == 'float64':
            return embedding.astype('float32')  # Ensure correct type
        return embedding
    except (SyntaxError, ValueError, TypeError):
        return None  # Return None for invalid embeddings

# Apply the parsing function and filter out any invalid rows
df['parsed_embedding'] = df['content_embedding'].apply(parse_embedding)
df = df.dropna(subset=['parsed_embedding'])

# Stack embeddings into a single array
embeddings = np.vstack(df['parsed_embedding'].values)

# Initialize FAISS index
embedding_dim = embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dim)

# Add embeddings to the FAISS index
index.add(embeddings)

# Save the FAISS index and metadata
faiss.write_index(index, "data/processed/faiss_content_index.idx")

# Save metadata for retrieval
metadata = df[["title", "summary", "content"]].to_dict(orient="records")
with open("data/processed/metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("FAISS index and metadata saved successfully.")
