"""Один ряд в PostgreSQL хранит число открытий главной страницы."""

from typing import Any

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    total BIGINT NOT NULL
)
"""

INCREMENT = """
INSERT INTO visits (id, total)
VALUES (1, 1)
ON CONFLICT (id) DO UPDATE
SET total = visits.total + 1
RETURNING total
"""


def record_visit(conn: Any) -> int:
    """Создаёт таблицу при первом визите и возвращает новое значение счётчика.

    conn — соединение psycopg или подмена в тесте. У объекта должен быть cursor().
    """
    with conn.cursor() as cursor:
        cursor.execute(CREATE_TABLE)
        cursor.execute(INCREMENT)
        row = cursor.fetchone()
    if row is None:
        raise RuntimeError("База не вернула значение счётчика")
    return int(row[0])
