#!/bin/sh
# Обновление стека на VPS. Сервер не собирает образ: он скачивает тег из GHCR.
# Volume базы и сертификата эта команда не удаляет.

set -eu
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo "Рядом с docker-compose.yml нет файла .env." >&2
  exit 1
fi

docker compose pull
docker compose up -d
