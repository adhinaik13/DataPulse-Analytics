[![CI](https://github.com/vankudothuadhinaik/DataPulse-Analytics/actions/workflows/ci.yml/badge.svg)](https://github.com/vankudothuadhinaik/DataPulse-Analytics/actions/workflows/ci.yml)

# DataPulse Analytics

A portfolio-scale event analytics demo with a FastAPI backend, SQLAlchemy persistence, PostgreSQL via Docker Compose, and a React/TypeScript dashboard.

## Implemented API

- `GET /health` — lightweight liveness response.
- `GET /health/ready` — checks that the database can answer a query; returns HTTP 503 when the database is unavailable.
- `POST /events` — validates and persists an event record; rejects blank/oversized identifiers, unknown fields, negative values, and non-finite event values.
- `GET /analytics/metrics` — aggregates event, distinct-user, distinct-session, and event-value totals.
- `GET /analytics/top-events` — returns the ten most common event names with deterministic tie ordering.
- Configurable CORS for the local dashboard, controlled by `CORS_ALLOWED_ORIGINS`.

Interactive API documentation is available at `/docs` when the backend is running.

## Stack

- Python, FastAPI, Pydantic, SQLAlchemy
- PostgreSQL (with psycopg)
- React, TypeScript, Vite, and Recharts
- Docker Compose for local services
- Pytest and GitHub Actions for backend endpoint and validation tests

Redis is included in the local Compose environment and configured through `REDIS_URL`, but the current API code does not yet use Redis for caching, queues, or analytics. Authentication, authorization, production migrations, and robust event-ingestion controls are also not implemented and should not be assumed. The readiness endpoint is a dependency check, not an authentication or deployment-readiness guarantee.

## Run locally

Copy the environment template and start the stack:

```bash
cp .env.example .env
docker compose up --build
```

Open the dashboard at http://localhost:5173 and the API docs at http://localhost:8000/docs.

For a non-default API address in a Vite frontend build, set `VITE_API_BASE_URL` (for example, `https://api.example.com`). The local default is `http://localhost:8000`.

Generate sample records with:

```bash
docker compose exec api python -m app.seed
```

Run the backend tests:

```bash
pip install -r backend/requirements.txt
pytest backend/tests
```

The tests use an isolated in-memory SQLite database and cover health, event ingestion, metric aggregation, top-event ordering, payload validation, and local CORS preflight behavior.

## Configuration and safety

Review `.env.example` before deployment. The credentials in Compose defaults are for local development only; replace them for any shared or hosted environment and keep real secrets out of Git.

## Scope

This is a learning/demo project, not a production analytics service. Database migrations, authentication/authorization, ingestion rate limits, operational observability, and broader frontend workflows remain future work.
