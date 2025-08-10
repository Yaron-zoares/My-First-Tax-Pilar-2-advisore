# Pilar2 Makefile - Easy project management

.PHONY: help install install-dev install-minimal clean test lint format run-backend run-frontend run-all

# Default target
help:
	@echo "Pilar2 Project Management"
	@echo "========================"
	@echo ""
	@echo "Available commands:"
	@echo "  install         - Install production dependencies"
	@echo "  install-dev     - Install development dependencies"
	@echo "  install-minimal - Install minimal dependencies only"
	@echo "  clean           - Clean Python cache and build files"
	@echo "  test            - Run tests"
	@echo "  lint            - Run linting and code quality checks"
	@echo "  format          - Format code with black and isort"
	@echo "  run-backend     - Start the backend server"
	@echo "  run-frontend    - Start the frontend"
	@echo "  run-all         - Start both backend and frontend"
	@echo "  update-deps     - Update dependencies to latest versions"
	@echo "  check-security  - Check for security vulnerabilities"
	@echo "  docs            - Build documentation"
	@echo "  docker-build    - Build Docker image"
	@echo "  docker-run      - Run Docker container"

# Installation targets
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

install-minimal:
	pip install -r requirements-minimal.txt

# Development targets
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".black_cache" -exec rm -rf {} +
	rm -rf build/ dist/ *.egg-info/

test:
	pytest tests/ -v --cov=backend --cov=config --cov=models --cov=agents

lint:
	flake8 backend/ config/ models/ agents/ --max-line-length=88 --extend-ignore=E203,W503
	mypy backend/ config/ models/ agents/
	bandit -r backend/ config/ models/ agents/ -f json -o bandit-report.json
	safety check

format:
	black backend/ config/ models/ agents/ --line-length=88
	isort backend/ config/ models/ agents/ --profile=black

# Run targets
run-backend:
	@echo "Starting Pilar2 Backend Server..."
	python run_backend.py

run-frontend:
	@echo "Starting Pilar2 Frontend..."
	python run_frontend.py

run-all:
	@echo "Starting Pilar2 Backend and Frontend..."
	@echo "Backend will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:8501"
	@echo "Press Ctrl+C to stop both servers"
	@echo ""
	@echo "Starting Backend..."
	@python run_backend.py & \
	@echo "Starting Frontend..." && \
	@python run_frontend.py & \
	@wait

# Maintenance targets
update-deps:
	@echo "Updating dependencies to latest versions..."
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt
	pip install --upgrade -r requirements-dev.txt

check-security:
	@echo "Checking for security vulnerabilities..."
	safety check
	bandit -r backend/ config/ models/ agents/ -f json -o security-report.json
	@echo "Security reports saved to security-report.json"

docs:
	@echo "Building documentation..."
	cd docs && make html
	@echo "Documentation built in docs/_build/html/"

# Docker targets
docker-build:
	@echo "Building Docker image..."
	docker build -t pilar2:latest .

docker-run:
	@echo "Running Docker container..."
	docker run -p 8000:8000 -p 8501:8501 pilar2:latest

# Quick development setup
setup-dev: clean install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make run-backend' to start the backend server"
	@echo "Run 'make run-frontend' to start the frontend"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make lint' to check code quality"

# Production setup
setup-prod: clean install
	@echo "Production environment setup complete!"
	@echo "Run 'make run-backend' to start the backend server"

# Health check
health-check:
	@echo "Checking system health..."
	@python -c "import sys; print(f'Python version: {sys.version}')"
	@python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"
	@python -c "import pandas; print(f'Pandas version: {pandas.__version__}')"
	@python -c "import pydantic; print(f'Pydantic version: {pydantic.__version__}')"
	@echo "Health check complete!"

# Backup and restore
backup:
	@echo "Creating backup of current state..."
	@tar -czf "pilar2-backup-$(shell date +%Y%m%d-%H%M%S).tar.gz" \
		--exclude='venv' \
		--exclude='__pycache__' \
		--exclude='*.pyc' \
		--exclude='.git' \
		--exclude='logs' \
		--exclude='data/uploads' \
		--exclude='data/processed' \
		--exclude='reports' \
		.

# Environment setup
setup-env:
	@echo "Setting up environment..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		cp config/secrets.env.example .env; \
		echo "Please edit .env file with your configuration"; \
	else \
		echo ".env file already exists"; \
	fi

# Database operations
db-migrate:
	@echo "Running database migrations..."
	@cd backend && alembic upgrade head

db-rollback:
	@echo "Rolling back last migration..."
	@cd backend && alembic downgrade -1

db-reset:
	@echo "Resetting database..."
	@cd backend && alembic downgrade base && alembic upgrade head
