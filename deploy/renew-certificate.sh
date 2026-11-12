#!/bin/sh
# Продление сертификата на VPS. Порт 80 в это время остаётся открытым:
# Let's Encrypt снова забирает файл из каталога webroot.

set -eu
cd "$(dirname "$0")/.."

docker compose --profile certificates run --rm certbot renew
docker compose exec nginx nginx -s reload
