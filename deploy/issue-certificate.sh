#!/bin/sh
# Первый выпуск сертификата Let's Encrypt на VPS.
# Стек уже должен подниматься: образ приложения есть в реестре, DNS домена указывает на сервер.

set -eu
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo "Рядом с docker-compose.yml нет файла .env." >&2
  exit 1
fi

set -a
# shellcheck disable=SC1091
. ./.env
set +a

if [ -z "${DOMAIN:-}" ] || [ -z "${ACME_EMAIL:-}" ]; then
  echo "В .env нужны DOMAIN и ACME_EMAIL." >&2
  exit 1
fi

echo "Поднимаю postgres, app и nginx."
docker compose up -d postgres app nginx

echo "Запрашиваю сертификат для ${DOMAIN}."
docker compose --profile certificates run --rm certbot certonly \
  --webroot \
  -w /var/www/certbot \
  --email "${ACME_EMAIL}" \
  --agree-tos \
  --no-eff-email \
  --keep-until-expiring \
  -d "${DOMAIN}"

echo "Пересоздаю nginx, чтобы он прочитал сертификат из volume."
docker compose up -d --force-recreate --no-deps nginx

echo "Записываю продление сертификата в crontab."
sh deploy/install-renew-cron.sh
