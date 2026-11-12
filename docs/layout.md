# Карта репозитория и этапы

«Готово» значит, что файл уже лежит в дереве. «Запланировано» значит, что рабочего файла ещё нет.

## Готово

| Путь | Роль |
| --- | --- |
| `README.md` | Вход в проект: что это, схема, как запускать и откатывать |
| `AGENTS.md` | Правила для агента Cursor |
| `CLAUDE.md`, `.claude/CLAUDE.md` | Те же ограничения для Claude Code |
| `.cursor/rules/` | Короткие правила по темам: проект, Python, контейнеры, CI, документы |
| `.cursor/hooks.json` | Когда запускать хуки |
| `.cursor/hooks/guard-shell.py` | Запрет локального Docker, чтения `.env` и force push |
| `.cursor/hooks/guard-writes.py` | Запрет записать секрет в git |
| `.cursor/skills/` | Как объяснять шаг и как проверять VPS |
| `.env.example` | Имена переменных без настоящих секретов |
| `.gitignore`, `.dockerignore` | Что не коммитить и что не класть в образ |
| `docs/` | Архитектура, решения, текст для собеседования, проверка сервера |
| `pyproject.toml`, `app/` | FastAPI: `/health` и страница счётчика |
| `tests/` | pytest: health без базы, счётчик с подменой доступа |

## Запланировано

| Порядок | Путь | Что появится |
| --- | --- | --- |
| 3 | `Dockerfile` | Multi-stage образ, пользователь без root |
| 4 | `docker-compose.yml` | `app`, `postgres` с volume и healthcheck, `nginx` |
| 5 | `nginx/` | Прокси и выдача файла проверки Let's Encrypt |
| 6 | `deploy/` | Команда обновления на VPS: pull и up |
| 7 | `.github/workflows/` | Ruff, pytest, сборка, GHCR, деплой по SSH |

Каталоги `nginx/`, `deploy/`, `.github/workflows/` пока пустые.
