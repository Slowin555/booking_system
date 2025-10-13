# Booking Project Makefile

.PHONY: help dev build up down clean logs db/migrate db/seed test lint typecheck

# Default target
help:
	@echo "Available commands:"
	@echo "  dev          - Start development environment"
	@echo "  build        - Build all containers"
	@echo "  up           - Start all services"
	@echo "  down         - Stop all services"
	@echo "  clean        - Clean up containers and volumes"
	@echo "  logs         - Show logs for all services"
	@echo "  db/migrate    - Run database migrations"
	@echo "  db/seed       - Seed initial data"
	@echo "  test          - Run tests"
	@echo "  lint          - Run linting"
	@echo "  typecheck     - Run type checking"

# Development environment
dev:
	@echo "Starting development environment..."
	docker-compose up --build

# Build all containers
build:
	@echo "Building all containers..."
	docker-compose build

# Start all services
up:
	@echo "Starting all services..."
	docker-compose up -d

# Stop all services
down:
	@echo "Stopping all services..."
	docker-compose down

# Clean up containers and volumes
clean:
	@echo "Cleaning up containers and volumes..."
	docker-compose down -v --remove-orphans
	docker system prune -f

# Show logs
logs:
	@echo "Showing logs for all services..."
	docker-compose logs -f

# Database migrations
db/migrate:
	@echo "Running database migrations..."
	docker-compose run --rm migrations

# Seed initial data
db/seed:
	@echo "Seeding initial data..."
	docker-compose run --rm api python scripts/seed.py

# Run tests
test:
	@echo "Running tests..."
	docker-compose run --rm api python -m pytest
	docker-compose run --rm web npm test

# Linting
lint:
	@echo "Running linting..."
	docker-compose run --rm api python -m flake8 .
	docker-compose run --rm web npm run lint

# Type checking
typecheck:
	@echo "Running type checking..."
	docker-compose run --rm api python -m mypy .
	docker-compose run --rm web npm run typecheck
