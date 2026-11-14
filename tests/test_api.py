import sqlite3

from fastapi.testclient import TestClient

from app.main import app, initialize_database


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_visit_counter_increments_and_persists(tmp_path, monkeypatch):
    import app.main as api

    database = tmp_path / "test_visits.db"
    monkeypatch.setattr(api, "DATABASE_PATH", database)
    initialize_database()

    with TestClient(app) as client:
        first = client.post("/api/visits")
        second = client.post("/api/visits")
        current = client.get("/api/visits")

    assert first.status_code == 200
    assert first.json() == {"visits": 1}
    assert second.json() == {"visits": 2}
    assert current.json() == {"visits": 2}

    with sqlite3.connect(database) as connection:
        stored = connection.execute(
            "SELECT visits FROM visitor_counter WHERE id = 1"
        ).fetchone()[0]
    assert stored == 2