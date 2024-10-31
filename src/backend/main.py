import faiss
import numpy as np
import pickle
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from typing import List

app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],  # Adjust based on your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load FAISS index and metadata
index = faiss.read_index("data/processed/faiss_content_index.idx")
with open("data/processed/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

# Load the sentence-transformer model for embedding
model = SentenceTransformer('all-MiniLM-L6-v2')  # Use the same model as for original embeddings

class QueryRequest(BaseModel):
    query: str

class SearchResult(BaseModel):
    title: str
    summary: str
    content: str
    url: str
    score: float

class QueryResponse(BaseModel):
    query: str
    results: List[SearchResult]

def search_similar_articles(query_embedding, top_k=5):
    """Search the FAISS index for the most similar articles to the query embedding."""
    distances, indices = index.search(np.array([query_embedding]).astype('float32'), top_k)
    
    # Retrieve the metadata for each of the top results
    results = []
    for i, idx in enumerate(indices[0]):
        article = metadata[idx]
        results.append({
            "title": article["title"],
            "summary": article["summary"],
            "content": article["content"],
            "url": article.get("url", ""),  # Assume URL is in metadata, or use empty string if not
            "score": float(distances[0][i])  # Convert distance to a float for JSON compatibility
        })
    
    return results

@app.get("/")
def read_root():
    return {"message": "Welcome to the semantic search API!"}

@app.post("/search", response_model=QueryResponse)
async def search(query_request: QueryRequest):
    # Convert the query into an embedding
    query_embedding = model.encode(query_request.query)
    
    # Perform search using FAISS and retrieve top results
    results = search_similar_articles(query_embedding, top_k=5)
    
    return QueryResponse(query=query_request.query, results=results)
