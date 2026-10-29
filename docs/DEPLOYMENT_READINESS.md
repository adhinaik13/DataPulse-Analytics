# Deployment readiness checklist

DataPulse is a demo analytics service. The current application calls SQLAlchemy `Base.metadata.create_all` at startup; this is convenient for local development but is not a versioned schema migration strategy for production.

## Required before production deployment

- Replace startup schema creation with Alembic migrations and reviewable migration revisions.
- Run migrations as a controlled release step, not independently in every API worker.
- Add integration tests against the same database engine used in deployment; SQLite-only tests cannot establish PostgreSQL behavior for all constraints and transactions.
- Keep `/health` as a liveness check and `/health/ready` as a dependency-aware readiness check.
- Configure explicit CORS origins per environment; do not use wildcard origins with credentials.
- Add authentication and authorization before exposing ingestion or analytics endpoints to untrusted clients.
- Define retention, deletion, and access-control policies before storing real user/event data.
- Add request-size limits, rate limits, structured logs, and metrics for ingestion failures.
- Use secret-managed database credentials and verify backups/restore procedures.

## Release verification

1. Start with a clean database and apply migrations from zero.
2. Upgrade a database created by the previous release.
3. Run API integration tests for event ingestion, validation errors, analytics aggregations, and database outage.
4. Confirm readiness returns HTTP 503 when the database is unavailable.
5. Confirm the service does not silently create or mutate production schema on application startup.

Do not describe the current demo as production-ready until these gates are implemented and tested.
