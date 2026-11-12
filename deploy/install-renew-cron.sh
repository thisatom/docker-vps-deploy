#!/bin/sh
# Ставит продление сертификата в crontab текущего пользователя.
# Два раза в сутки: certbot сам выходит, если срок ещё не близкий.
# Let's Encrypt выдаёт сертификат примерно на 90 дней.

set -eu
cd "$(dirname "$0")/.."
root=$(pwd)

if ! command -v crontab >/dev/null 2>&1; then
  echo "Нет команды crontab. На Debian: apt-get install -y cron && systemctl enable --now cron" >&2
  exit 1
fi

marker="deploy/renew-certificate.sh"
# У cron короткий PATH. Без него docker часто не находится, и продление молча не идёт.
line="15 3,15 * * * PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin cd ${root} && sh deploy/renew-certificate.sh >> ${root}/renew.log 2>&1"
existing=$(crontab -l 2>/dev/null || true)

if printf '%s\n' "$existing" | grep -F "$marker" >/dev/null 2>&1; then
  echo "Продление уже записано в crontab."
  exit 0
fi

{
  printf '%s\n' "$existing"
  printf '%s\n' "$line"
} | sed '/^$/d' | crontab -

echo "Продление записано в crontab: 03:15 и 15:15. Лог: ${root}/renew.log"
if ! pgrep -x cron >/dev/null 2>&1 && ! pgrep -x crond >/dev/null 2>&1; then
  echo "Служба cron не запущена. На Debian: systemctl enable --now cron" >&2
  exit 1
fi
