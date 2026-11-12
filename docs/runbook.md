# Проверка

Команды Docker выполняются на VPS по SSH. На рабочей станции их нет.

Секреты из `.env` в чат и в логи не копировать.

## Сейчас

После push в любую ветку открой GitHub Actions, workflow `CI`. Job `Ruff and pytest` должен быть зелёным. Секреты для него не задаются.

Push в `main` после тестов запускает ещё два job: `Build and push image` и `Deploy to VPS`. Второй job зелёный только если заданы `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY` и на сервере есть каталог `/opt/docker-vps-deploy` с `.env`.

Перед первым деплоем на VPS:

1. Клон репозитория лежит в `/opt/docker-vps-deploy`.
2. Рядом есть `.env`. В `APP_IMAGE` владелец написан строчными буквами, тег — `latest`.
3. Пользователь из `VPS_USER` может запускать `docker`.
4. Если пакет GHCR закрытый, на сервере уже выполнен `docker login ghcr.io`. Токен в репозиторий не копировать.

Ручное обновление из этого каталога:

```bash
sh deploy/update.sh
```

В репозитории достаточно убедиться в следующем:

- файла `.env` в git нет;
- `.env.example` есть, внутри `change-me` и `example.com`;
- в `docs/layout.md` статус совпадает с деревом файлов.

## Сертификат

Эти команды выполняют на VPS, когда стек уже поднимается и A-запись домена указывает на этот сервер. На рабочей станции их нет.

```bash
sh deploy/issue-certificate.sh
curl -fsS "https://example.com/health"
```

Повторный запуск скрипта выпуска не заказывает новый сертификат, пока старый ещё действует: у Certbot стоит `--keep-until-expiring`.

Продление:

```bash
sh deploy/renew-certificate.sh
```

Файлы сертификата лежат в volume `letsencrypt`. В каталог проекта они не копируются.

## После деплоя приложения

Подставь свой домен вместо `example.com`. Каталог на сервере — тот, где лежат `docker-compose.yml` и `.env`.

1. Контейнеры запущены.

   ```bash
   docker compose ps
   ```

   Ожидание: `nginx`, `app`, `postgres` в состоянии running. У базы статус health — healthy.

2. Процесс приложения отвечает изнутри сервера.

   ```bash
   curl -fsS http://127.0.0.1/health
   ```

   Ожидание: JSON со статусом ok. Пока сертификата нет, проверка идёт на порт 80.

3. Счётчик растёт.

   ```bash
   curl -fsS http://127.0.0.1/
   curl -fsS http://127.0.0.1/
   ```

   Второе число больше первого.

4. Снаружи, после выпуска сертификата.

   ```bash
   curl -fsS https://example.com/health
   ```

5. База переживает пересоздание контейнера.

   ```bash
   docker compose restart postgres
   curl -fsS http://127.0.0.1/
   ```

   Число на месте. Так проверяется volume.

## Откат

1. В GHCR или в истории git взять SHA предыдущего успешного коммита.
2. На сервере в `.env` выставить `APP_IMAGE=ghcr.io/OWNER/docker-vps-deploy:<sha>`.
3. Выполнить:

   ```bash
   sh deploy/update.sh
   ```

   Чтобы следующий push в `main` снова выкладывал свежий образ, верни в `APP_IMAGE` тег `latest`. Пока там старый SHA, `update.sh` будет скачивать именно его.

4. Снова открыть `/health`.
5. Volume Postgres не удалять. Команда `docker compose down -v` стирает счётчик, для отката она не используется.

## Если сайт не открывается

Смотреть по порядку: `docker compose ps`, логи `nginx`, логи `app`, логи `postgres`. Типовые причины: в `.env` другой пароль, чем у уже созданного volume базы; DNS домена указывает не на этот VPS; контейнер `app` стартовал раньше готовой базы.
