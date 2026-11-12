"""Счётчик в живом PostgreSQL. Без DATABASE_URL тест пропускается."""

import os

import pytest
from app.main import visit_count

pytestmark = pytest.mark.skipif(
    not os.environ.get("DATABASE_URL"),
    reason="DATABASE_URL не задан: живой PostgreSQL проверяет job в GitHub Actions",
)


def test_visit_count_grows_in_postgres() -> None:
    first = visit_count()
    second = visit_count()

    assert second == first + 1
