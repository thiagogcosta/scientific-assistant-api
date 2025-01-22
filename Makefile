.PHONY : local-start, build, start, end, clear, clear_all, lock, quality, tests

local-start:
	@python3 -m pip install -q poetry==1.8.3
	@poetry install --only main
	@python3 -m poetry run src/main.py

# Target to build the Docker image
build:
	@echo "Starting the build of the RAG API..."
	@docker build --progress=plain -t scientific_assistant_api .

# Target to start the Docker service - success
start:
	@echo "Starting RAG API..."
	@docker run --network host --name api scientific_assistant_api

# Target to stop Docker service
end:
	@echo "Stopping RAG API..."
	@docker kill api

# Target to remove all Docker containers
clear:
	@echo "Removing Docker container..."
	@docker rm api

# Target to remove all Docker containers
clear_all:
	@echo "Removing all Docker containers..."
	@docker rm -f $$(docker ps -a -q) || true

# Target to invoke the poetry lock process
lock:
	@echo "Starting the lock process..."
	@python3 -m pip install -q poetry==1.8.3
	@poetry lock

# Target to invoke the quality process
quality:
	@echo "Starting the quality process..."
	@python3 -m pip install pre-commit==3.8.0
	@pre-commit install
	@pre-commit run --all-files

# Target to invoke the testing process
tests:
	@echo "Starting the tests process..."
	@poetry install --with dev
	@poetry run pytest --cov=tests --cov-fail-under=70
