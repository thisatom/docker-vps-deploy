#!/usr/bin/env python3
"""Блокирует локальный Docker, обращение к секретному .env и force push.

Событие: beforeShellExecution. На stdin — JSON, на stdout — JSON с permission.
Ошибка разбора заканчивается allow, чтобы сломанный хук не останавливал агента.
"""

from __future__ import annotations

import json
import re
import sys

DOCKER = re.compile(
    r"(?:^|[;&|`]\s*)(?:sudo\s+)?(?:docker(?:-compose)?|podman|nerdctl)(?=$|[\s])",
    re.IGNORECASE | re.MULTILINE,
)
FORCE_PUSH = re.compile(r"(?:^|\s)(?:-f|--force(?:-with-lease)?)(?=\s|$)", re.IGNORECASE)
GIT_PUSH = re.compile(r"(?:^|[;&|`]\s*)git\s+push\b", re.IGNORECASE)


def emit(payload: dict) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    json.dump(payload, sys.stdout, ensure_ascii=False)
    return 0


def allow() -> int:
    return emit({"permission": "allow"})


def deny(user_message: str, agent_message: str) -> int:
    return emit(
        {
            "permission": "deny",
            "user_message": user_message,
            "agent_message": agent_message,
        }
    )


def as_text(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(as_text(item) for item in value)
    return ""


def strip_quotes(command: str) -> str:
    without_double = re.sub(r'"(?:\\.|[^"])*"', " ", command)
    return re.sub(r"'(?:\\.|[^'])*'", " ", without_double)


def mentions_secret_env(command: str) -> bool:
    scrubbed = re.sub(r"\.env\.example\b", "", command, flags=re.IGNORECASE)
    return re.search(r"(?:^|[\s/\\'\"`=])\.env\b", scrubbed, flags=re.IGNORECASE) is not None


def main() -> int:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return allow()
    if not isinstance(data, dict):
        return allow()

    command = as_text(data.get("command"))
    if not command.strip():
        return allow()

    bare = strip_quotes(command)

    if DOCKER.search(bare):
        return deny(
            "Локальный Docker в этом проекте запрещён: на рабочей станции нет виртуализации.",
            "Останови команду Docker. Проверка выполняется на VPS и в GitHub Actions.",
        )

    if mentions_secret_env(command):
        return deny(
            "Команда обращается к секретному .env. В репозитории допустим только .env.example.",
            "Не читай и не записывай .env. Используй .env.example и GitHub Secrets.",
        )

    if GIT_PUSH.search(bare) and FORCE_PUSH.search(bare):
        return deny(
            "Force push заблокирован хуком. Нужна явная просьба пользователя и отдельное подтверждение.",
            "Не выполняй git push --force. История на main переписывается только по прямой просьбе.",
        )

    return allow()


if __name__ == "__main__":
    raise SystemExit(main())
