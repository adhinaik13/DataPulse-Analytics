# DataPulse Analytics

A portfolio-scale event analytics demo with a FastAPI backend, SQLAlchemy persistence, PostgreSQL via Docker Compose, and a React/TypeScript dashboard.

## Implemented API

- `GET /health` — simple service health response.
- `POST /events` — validates and persists an event record.
- `GET /analytics/metrics` — aggregates event, distinct-user, distinct-session, and event-value totals.
- `GET /analytics/top-events` — returns the ten most common event names.

Interactive API documentation is available at `/docs` when the backend is running.

## Stack

- Python, FastAPI, Pydantic, SQLAlchemy
- PostgreSQL (with psycopg)
- React, TypeScript, Vite, and Recharts
- Docker Compose for local services
- Pytest and GitHub Actions for the current backend test suite

Redis is included in the local Compose environment and configured through `REDIS_URL`, but the current API code does not yet use Redis for caching, queues, or analytics. Authentication, authorization, production migrations, and robust event-ingestion controls are also not implemented and should not be assumed.

## Run locally

Copy the environment template and start the stack:

```bash
cp .env.example .env
docker compose up --build
```

Open the dashboard at http://localhost:5173 and the API docs at http://localhost:8000/docs.

Generate sample records with:

```bash
docker compose exec api python -m app.seed
```

Run the backend tests:

```bash
pip install -r backend/requirements.txt
pytest backend/tests
```

## Configuration and safety

Review `.env.example` before deployment. The credentials in Compose defaults are for local development only; replace them for any shared or hosted environment and keep real secrets out of Git.

## Scope

This is a learning/demo project, not a production analytics service. The current tests cover basic backend health behavior; ingestion, aggregation, database failure modes, and frontend workflows need broader automated coverage before production use.
