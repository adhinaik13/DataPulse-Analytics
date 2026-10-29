from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


def teardown_module():
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ingestion_and_analytics_endpoints():
    first = client.post(
        "/events",
        json={
            "event_name": "purchase",
            "user_id": "user-1",
            "session_id": "session-1",
            "value": 12.5,
        },
    )
    second = client.post(
        "/events",
        json={
            "event_name": "page_view",
            "user_id": "user-1",
            "session_id": "session-2",
        },
    )
    assert first.status_code == 201
    assert second.status_code == 201

    metrics = client.get("/analytics/metrics")
    assert metrics.status_code == 200
    assert metrics.json() == {
        "events": 2,
        "users": 1,
        "sessions": 2,
        "revenue": 12.5,
    }

    top = client.get("/analytics/top-events")
    assert top.status_code == 200
    assert top.json() == [
        {"event": "page_view", "count": 1},
        {"event": "purchase", "count": 1},
    ]


def test_rejects_invalid_event_values():
    response = client.post(
        "/events",
        json={
            "event_name": "purchase",
            "user_id": "user-1",
            "session_id": "session-1",
            "value": -1,
        },
    )
    assert response.status_code == 422

    for value in (float("inf"), float("-inf"), float("nan")):
        response = client.post(
            "/events",
            json={
                "event_name": "purchase",
                "user_id": "user-1",
                "session_id": "session-1",
                "value": value,
            },
        )
        assert response.status_code == 422


def test_rejects_blank_required_fields_and_unknown_fields():
    blank = client.post(
        "/events",
        json={"event_name": " ", "user_id": "user-1", "session_id": "session-1"},
    )
    unknown = client.post(
        "/events",
        json={
            "event_name": "purchase",
            "user_id": "user-1",
            "session_id": "session-1",
            "unexpected": "field",
        },
    )
    assert blank.status_code == 422
    assert unknown.status_code == 422


def test_cors_allows_local_dashboard_origin():
    response = client.options(
        "/analytics/metrics",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
