[![CI](https://github.com/vankudothuadhinaik/DataPulse-Analytics/actions/workflows/ci.yml/badge.svg)](https://github.com/vankudothuadhinaik/DataPulse-Analytics/actions/workflows/ci.yml)

# DataPulse Analytics

A portfolio-scale event analytics demo with a FastAPI backend, SQLAlchemy persistence, PostgreSQL via Docker Compose, and a React/TypeScript dashboard.

## Implemented API

- `GET /health` — simple service health response.
- `POST /events` — validates and persists an event record; rejects blank/oversized identifiers, unknown fields, negative values, and non-finite event values. Database write failures are rolled back and returned as a safe `503` response.
- `GET /analytics/metrics` — aggregates event, distinct-user, distinct-session, and event-value totals.
- `GET /analytics/top-events` — returns the ten most common event names with deterministic tie ordering.
- Configurable CORS for the local dashboard, controlled by `CORS_ALLOWED_ORIGINS`.

Interactive API documentation is available at `/docs` when the backend is running.

## Stack

- Python, FastAPI, Pydantic, SQLAlchemy
- PostgreSQL (with psycopg)
- React, TypeScript, Vite, and Recharts
- Docker Compose for local services
- Pytest and GitHub Actions for backend endpoint, validation, and frontend build checks

Redis is included in the local Compose environment and configured through `REDIS_URL`, but the current API code does not yet use Redis for caching, queues, or analytics. Authentication, authorization, production migrations, and robust event-ingestion controls are also not implemented and should not be assumed.

## Run locally

Copy the environment template and start the stack:

```bash
cp .env.example .env
docker compose up --build
```

The local Compose API sets `DATAPULSE_AUTO_CREATE_TABLES=true` so tables are created for this demo. The application does not create tables merely because its Python module is imported. For hosted or production deployments, leave this setting disabled and manage schema changes with a migration system before deploying.

Open the dashboard at http://localhost:5173 and the API docs at http://localhost:8000/docs.

For a non-default API address in a Vite frontend build, set `VITE_API_BASE_URL` (for example, `https://api.example.com`). The local default is `http://localhost:8000`.

Generate sample records with:

```bash
docker compose exec api python -m app.seed
```

Run the backend tests:

```bash
python -m pip install -r backend/requirements.txt
PYTHONPATH=backend python -m pytest backend/tests
```

The tests use an isolated in-memory SQLite database and cover health, event ingestion, metric aggregation, top-event ordering, payload validation, local CORS preflight behavior, and rollback/safe responses for a simulated database write failure.

## Configuration and safety

Review `.env.example` before deployment. The credentials in Compose defaults are for local development only; replace them for any shared or hosted environment and keep real secrets out of Git. This API currently does not implement authentication; do not expose it to untrusted networks as though it were protected.

## Scope

This is a learning/demo project, not a production analytics service. Database migrations, authentication/authorization, ingestion rate limits, operational observability, and broader frontend workflows remain future work.
