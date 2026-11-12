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
| `tests/` | pytest: health без базы, счётчик с подменой; живой PostgreSQL только при `DATABASE_URL` |
| `Dockerfile` | Два этапа, пользователь `app`, Uvicorn на порту 8000 |
| `docker-compose.yml` | `app`, `postgres` с volume и healthcheck, `nginx` на портах 80 и 443 |
| `nginx/` | Порт 80: проверка Certbot и `/health`. Порт 443: сайт. Временный сертификат, затем Let's Encrypt |
| `docker-compose.ci.yml` | Только смоук в GitHub Actions: не скачивать локальный тег приложения из реестра |
| `deploy/issue-certificate.sh` | Первый выпуск сертификата на VPS и запись продления в crontab |
| `deploy/renew-certificate.sh` | Продление сертификата и перечитка конфига Nginx |
| `deploy/install-renew-cron.sh` | Crontab: два раза в сутки вызвать продление |
| `deploy/update.sh` | На VPS: `git pull --ff-only`, pull образа и up, без удаления volume |
| `.github/workflows/ci.yml` | Ruff, pytest, PostgreSQL, смоук Compose. Сборка, GHCR и SSH только из `main` |

## Запланировано

Рабочих файлов вне дерева нет. Сайт откроется после первого зелёного прогона workflow на `main`, когда на VPS лежат клон в `/opt/docker-vps-deploy`, файл `.env` и секреты `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`.
