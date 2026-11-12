#!/bin/sh
# Обновление стека на VPS. Сначала файлы репозитория с origin/main,
# затем образ из GHCR. Сервер образ не собирает.
# Volume базы и сертификата эта команда не удаляет. .env pull не трогает.

set -eu
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo "Рядом с docker-compose.yml нет файла .env." >&2
  exit 1
fi

if ! git -c safe.directory="$(pwd)" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Каталог не является git-клоном. Файлы Compose и Nginx сами не обновятся." >&2
  exit 1
fi

echo "Подтягиваю файлы origin/main. Образ берётся из APP_IMAGE в .env."
git -c safe.directory="$(pwd)" pull --ff-only origin main

docker compose pull
docker compose up -d
