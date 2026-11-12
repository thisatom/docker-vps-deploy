#!/bin/sh
# Выбирает каталог сертификата и только потом запускает обычный вход Nginx.
# Пока Let's Encrypt ещё не выпускал сертификат, Nginx получает временный
# самоподписанный файл и может слушать 443.

set -eu

if [ -z "${DOMAIN:-}" ]; then
  echo "Переменная DOMAIN пуста. Задайте её в .env на сервере." >&2
  exit 1
fi

live="/etc/letsencrypt/live/${DOMAIN}"
dummy="/etc/nginx/dummy"

if [ -s "${live}/fullchain.pem" ] && [ -s "${live}/privkey.pem" ]; then
  export CERT_DIR="${live}"
else
  if ! command -v openssl >/dev/null 2>&1; then
    if ! command -v apk >/dev/null 2>&1; then
      echo "Нет команды openssl и нет apk. Временный сертификат создать нельзя." >&2
      exit 1
    fi
    echo "В образе нет openssl. Ставлю пакет: он нужен только для временного сертификата."
    apk add --no-cache openssl
  fi
  mkdir -p "${dummy}"
  if [ ! -s "${dummy}/fullchain.pem" ] || [ ! -s "${dummy}/privkey.pem" ]; then
    openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
      -keyout "${dummy}/privkey.pem" \
      -out "${dummy}/fullchain.pem" \
      -subj "/CN=${DOMAIN}"
  fi
  export CERT_DIR="${dummy}"
fi

exec /docker-entrypoint.sh nginx -g "daemon off;"
