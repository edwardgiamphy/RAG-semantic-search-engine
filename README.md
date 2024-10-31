# Semantic Search Project

This project is a semantic search application that allows users to query articles based on meaning rather than keyword matching. It combines data processing, FAISS for vector similarity search, and FastAPI for serving an API and frontend and build a retrieval system.

## `README.md` Overview

1. **Project Organization**: Brief description of the project and structure.
2. **Setup Instructions**: Commands to build, run, and test the application using `make`.
3. **Scripts Overview**: Explanation of each script’s purpose within the project.
4. **Usage Examples**: Steps to run the full application, example search queries, and troubleshooting tips.

This `Makefile` and `README.md` will streamline development and make the project more accessible for future collaborators or maintenance.

## Makefile Overview:

Docker Commands:

- 'build': Builds the Docker image using - docker-compose build.

- 'up': Starts the app with docker-compose up.

- 'down': Stops the app with docker-compose down.

Data Processing Commands:

- 'create-dataset': Runs the script to create a dataset from JSON files.
- 'generate-embeddings': Runs the script to generate embeddings.
- 'store-faiss-index': Stores the embeddings in FAISS for future search.

Cleanup:
- 'clean': Deletes any processed files in 'data/processed'.

Testing:
- 'test': Runs unit tests in the 'tests' folder.

Documentation:
- 'docs': Placeholder to reference 'README.md' for full project documentation.


 

## Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data_import           <- Scripts to download or generate data
    │   │  
    │   │
    │   ├── backend       <- Scripts to manage the user query and run the application
    │   │
    │   ├── frontend         <- Files to manage the frontend
    │   │                     predictions
    │
    └── tests            <- A few tests to check that some functionalities of the project workflow are healthy

## Setup Instructions
### 0. Project quick use (optional)
For quick use, you may want to run individual data processing steps locally into a conda environment. If so, run :
```
conda create -n "search" python=3.10.14
conda activate search
pip install -r requirements.txt
```
Then install run the data processing steps:
```
make create-data-folder
make fetch-data
make create-dataset
make generate-embeddings
make store-faiss-index
```

Then you may want to run the tests in the conda environment (look above for more details).

### 1. Install Dependencies

To set up the environment, ensure that you have Docker installed. Then, build and run the Docker containers.
```
make build
make up
```


The application will be available at:

Backend API: http://localhost:8000
Frontend: http://localhost:8001
### 2. Running Data Processing Scripts
To manually run data processing scripts without Docker (optional):
```
make create-dataset         # Create dataset from JSON 
make generate-embeddings    # Generate embeddings from the dataset
make store-faiss-index      # Store embeddings in FAISS index
```
### 3. Running Tests
To ensure everything is working as expected, you can run unit tests:

```make test```

If so, you may want to open an interactive terminal in the container. To do so, go the the Dockerfile and:
- uncomment the last line 
```# CMD ["bash"]``` 
- comment the above line 
```CMD ["bash", "-c", "uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 & cd src/frontend && python -m http.server 8001"]```


Then start the container with an interactive shell:
```
docker build -t semantic-search .
docker run -it --rm -p 8000:8000 -p 8001:8001 semantic-search
```

Once inside the container, you can manually start FastAPI and the HTTP server by running:
```
uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 &
cd src/frontend && python -m http.server 8001
```



### 4. Cleaning Up
To delete generated files (e.g., processed CSVs, FAISS index, metadata files):


```make clean```

## Scripts Overview

### Data Processing
- 'create_dataset.py': Reads raw JSON files in 'data/raw/' and creates a CSV dataset in 'data/processed/'.
- 'generate_embeddings.py': Generates embeddings for each article using sentence-transformers and saves them to 'data/processed/articles_with_embeddings.csv'.
- 'store_embeddings_faiss.py': Loads embeddings from 'articles_with_embeddings.csv', builds a FAISS index, and saves it to 'data/processed/'.

### Backend
'main.py': Initializes the FastAPI server, defines the '/search' endpoint for querying similar articles, and enables CORS for frontend requests.
'query_search.py': Contains the function to search for similar articles using the FAISS index.

### Frontend
'index.html': Simple frontend interface allowing users to enter search queries and view the top 5 most relevant articles.

## Usage

### Running the Application
To start the full application:

'make up'
Open the frontend at http://localhost:8001.
Enter a search query, and the frontend will display the top 5 most relevant articles based on semantic similarity.

### Example Search Query
To search for articles using the CLI (e.g., with curl):
```
curl -X POST "http://localhost:8000/search" -H "Content-Type: application/json" -d '{"query": "depardieu"}'
```
## Troubleshooting

Docker Build Errors: If you encounter build errors, ensure requirements.txt specifies compatible versions of all dependencies (e.g., numpy<2.0 for FAISS).
Errors in Data Processing: If there are issues in generating embeddings or storing the FAISS index, check that articles_with_embeddings.csv is correctly formatted.

## Additional Information

Refer to docs/ for additional project documentation and usage details.


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
