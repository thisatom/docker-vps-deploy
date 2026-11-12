import os

from app.main import app
from fastapi.testclient import TestClient


def test_health_does_not_need_database(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert "DATABASE_URL" not in os.environ

    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
