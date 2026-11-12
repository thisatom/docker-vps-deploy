from app.counter import record_visit
from app.main import DatabaseUnavailable, app, visit_count
from fastapi.testclient import TestClient


class FakeCursor:
    def __init__(self, total: int) -> None:
        self.total = total
        self.statements: list[str] = []

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def execute(self, query: str) -> None:
        self.statements.append(query)

    def fetchone(self) -> tuple[int]:
        return (self.total,)


class FakeConnection:
    def __init__(self, total: int) -> None:
        self.cursor_obj = FakeCursor(total)

    def cursor(self) -> FakeCursor:
        return self.cursor_obj


def test_record_visit_returns_number_from_database() -> None:
    connection = FakeConnection(total=3)

    assert record_visit(connection) == 3
    assert len(connection.cursor_obj.statements) == 2


def test_page_shows_injected_count() -> None:
    app.dependency_overrides[visit_count] = lambda: 4
    try:
        response = TestClient(app).get("/")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert "Эта страница открыта 4 раз." in response.text


def test_page_reports_database_failure() -> None:
    def broken() -> int:
        raise DatabaseUnavailable("База данных недоступна")

    app.dependency_overrides[visit_count] = broken
    try:
        response = TestClient(app).get("/")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json()["status"] == "unavailable"
