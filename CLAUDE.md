# Инструкции для Claude Code

Подробная версия: [AGENTS.md](AGENTS.md). Краткий дубль лежит в [.claude/CLAUDE.md](.claude/CLAUDE.md).

## Ограничения

- Учебный проект: FastAPI, PostgreSQL, Nginx, Certbot, Docker Compose, GitHub Actions, VPS Debian 12.
- Объясняй каждый шаг простыми словами по-русски: что сделано, зачем, как сказать на собеседовании.
- Docker на компьютере разработчика недоступен. Проверка — GitHub Actions и VPS.
- Секреты только в `.env` на сервере и в GitHub Secrets. В git допускается `.env.example`.
- Не записывай пароли, приватные ключи и живые сертификаты.
- Не делай force push без прямой просьбы пользователя.
- Не помечай этап готовым, если файлов этого этапа ещё нет. Карта: `docs/layout.md`.
- Документы без эмодзи.

## Куда смотреть

- Архитектура: `docs/architecture.md`
- Почему выбран такой стек: `docs/decisions/`
- Текст для собеседования: `docs/interview.md`
- Проверка на сервере: `docs/runbook.md`
