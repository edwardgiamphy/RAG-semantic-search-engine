import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

# Load the FAISS index
index = faiss.read_index("data/processed/faiss_content_index.idx")

# Load the metadata associated with each embedding
with open("data/processed/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

# Initialize the sentence-transformers model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Replace with the model you used to create the embeddings

def query_to_embedding(query):
    """Convert a user query into an embedding."""
    return model.encode(query) # prevent the warning related to clean_up_tokenization_spaces

def search_similar_articles(query_embedding, top_k=5):
    """Search for articles similar to the given query embedding."""
    distances, indices = index.search(np.array([query_embedding]).astype('float32'), top_k)
    
    # Retrieve the metadata for the top matches
    results = []
    for idx in indices[0]:
        results.append(metadata[idx])
    
    return results

if __name__ == "__main__":
    # Get the user query
    query = input("Enter your search query: ")
    
    # Convert the query to an embedding
    query_embedding = query_to_embedding(query)
    
    # Search for similar articles
    results = search_similar_articles(query_embedding)
    
    # Display the results
    print("\nTop results for your query:\n")
    for i, result in enumerate(results, start=1):
        print(f"Result {i}")
        print("Title:", result["title"])
        print("Summary:", result["summary"])
        print("Content:", result["content"])
        print("\n" + "-"*40 + "\n")
