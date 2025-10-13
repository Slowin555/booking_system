# Booking System

A modern booking system built with Next.js, FastAPI, PostgreSQL, and Docker.

## Architecture

- **Frontend**: Next.js 14 with App Router, TypeScript, Tailwind CSS
- **Backend**: FastAPI with SQLAlchemy and Alembic migrations
- **Database**: PostgreSQL 15
- **Shared**: Zod schemas for type-safe API contracts
- **Infrastructure**: Docker Compose for development

## Project Structure

```
/
├── contracts/          # Shared Zod schemas
├── web/               # Next.js frontend
├── api/               # FastAPI backend
├── migrations/         # Database migrations
├── docker-compose.yml  # Development environment
├── Makefile           # Development commands
└── .github/           # CI/CD workflows
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Make (optional, for convenience commands)

### Development

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd booking
   cp .env.example .env
   ```

2. **Start development environment**:
   ```bash
   make dev
   # or
   docker-compose up --build
   ```

3. **Access the applications**:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Available Commands

```bash
make dev          # Start development environment
make build        # Build all containers
make up           # Start all services
make down         # Stop all services
make clean        # Clean up containers and volumes
make logs         # Show logs for all services
make db/migrate    # Run database migrations
make db/seed       # Seed initial data
make test          # Run tests
make lint          # Run linting
make typecheck     # Run type checking
```

## Health Checks

Both services include health check endpoints:

- **API Health**: `GET /health` - Returns `{"status": "ok", "service": "api"}`
- **Web Health**: `GET /api/health` - Returns `{"status": "ok", "service": "web"}`

## Development Workflow

1. **Database Migrations**: Use Alembic for database schema changes
2. **API Development**: FastAPI with automatic OpenAPI documentation
3. **Frontend Development**: Next.js with hot reloading
4. **Type Safety**: Shared Zod schemas between frontend and backend
5. **Testing**: Automated CI with linting, type checking, and tests

## Environment Variables

Copy `.env.example` to `.env` and configure:

- `DATABASE_URL`: PostgreSQL connection string
- `API_URL`: Backend API URL
- `NEXT_PUBLIC_API_URL`: Frontend API URL
- `JWT_SECRET`: JWT signing secret

## Contributing

1. Create a feature branch
2. Make your changes
3. Run `make lint` and `make typecheck`
4. Submit a pull request

The CI pipeline will automatically run linting, type checking, and tests.
