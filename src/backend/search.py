import faiss
import numpy as np
import pickle

# Load the FAISS index
index = faiss.read_index("faiss_content_index.idx")

# Load the metadata
with open("metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

# Define a function to search the index
def search(query_embedding, top_k=5):
    # Query FAISS index for similar embeddings
    distances, indices = index.search(np.array([query_embedding]), top_k)
    
    # Retrieve corresponding metadata
    results = []
    for idx in indices[0]:
        results.append(metadata[idx])
    return results

# Example usage: Assuming we have a query_embedding from the same model
# query_embedding = model.encode("Sample query text").tolist()
# results = search(query_embedding)
# print(results)
