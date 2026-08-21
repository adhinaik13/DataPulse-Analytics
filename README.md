# DataPulse Analytics

Portfolio-ready full-stack web analytics platform using Python/FastAPI, PostgreSQL, React/TypeScript, Redis, and Docker.

## Features
- Event ingestion API
- Python ETL/demo-data pipeline
- PostgreSQL analytics queries and indexes
- Redis-ready architecture
- React + TypeScript dashboard
- Docker Compose
- Pytest and GitHub Actions CI

## Run
cp .env.example .env
docker compose up --build

Then open http://localhost:5173 and http://localhost:8000/docs.

Generate demo data:
docker compose exec api python -m app.seed

This is an original implementation inspired by common open-source full-stack analytics architectures; it does not copy source repository code.
