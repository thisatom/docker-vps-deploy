"""HTTP-слой: /health не трогает базу, страница / увеличивает счётчик."""

import os

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.counter import record_visit

app = FastAPI(title="docker-vps-deploy")


class DatabaseUnavailable(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


@app.exception_handler(DatabaseUnavailable)
def database_unavailable(_request: Request, exc: DatabaseUnavailable) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"status": "unavailable", "detail": exc.detail},
    )


def visit_count() -> int:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise DatabaseUnavailable("Не задана переменная DATABASE_URL")
    try:
        import psycopg
    except ImportError as exc:
        raise DatabaseUnavailable("Драйвер PostgreSQL не установлен") from exc
    try:
        with psycopg.connect(database_url) as connection:
            return record_visit(connection)
    except psycopg.Error:
        raise DatabaseUnavailable("База данных недоступна") from None


def render_page(count: int) -> str:
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>Счётчик визитов</title>
</head>
<body>
  <h1>Счётчик визитов</h1>
  <p>Эта страница открыта {count} раз.</p>
</body>
</html>
"""


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(count: int = Depends(visit_count)) -> str:
    return render_page(count)
