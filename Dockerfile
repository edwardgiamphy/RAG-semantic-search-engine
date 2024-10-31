# Use the official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .

# Run data processing scripts to set up FAISS index and embeddings
RUN python src/data_import/fetch_rss.py
RUN python src/data_import/create_dataset.py
RUN python src/data_import/generate_embeddings.py
RUN python src/data_import/store_embeddings_faiss.py

# Expose ports for FastAPI (8000) and the frontend (8001)
EXPOSE 8000
EXPOSE 8001

# Command to run both the backend and frontend
CMD ["bash", "-c", "uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 & cd src/frontend && python -m http.server 8001"]

# Start an interactive shell after the container setup is complete
# CMD ["bash"]