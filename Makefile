# Makefile for the semantic-search-ekg project

# Docker commands
build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

# Run individual data processing steps locally (optional)
create-dataset:
	python src/data_import/create_dataset.py

generate-embeddings:
	python src/data_import/generate_embeddings.py

store-faiss-index:
	python src/data_import/store_embeddings_faiss.py

# Open the frontend in a web browser
open-browser:
	@echo "Opening the frontend in your default browser..."
ifeq ($(shell uname), Darwin)  # macOS
	open http://localhost:8001
else ifeq ($(shell uname), Linux)  # Linux
	xdg-open http://localhost:8001
else  # Windows
	start http://localhost:8001
endif

# Clean up generated files
clean:
	rm -rf data/processed/*.csv data/processed/*.idx data/processed/*.pkl

# Test commands
test:
	python -m unittest discover -s tests


# Documentation
docs:
	@echo "Documentation is available in the README.md file."
