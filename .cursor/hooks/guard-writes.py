#!/usr/bin/env python3
"""Не даёт агенту записать секреты в дерево репозитория.

Событие: preToolUse. Срабатывает на запись и правку файлов.
Удаление .env разрешено. Чтение разрешено.
Ошибка разбора заканчивается allow.
"""

from __future__ import annotations

import json
import re
import sys

PRIVATE_KEY = re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")
MUTATION = ("write", "strreplace", "search_replace", "edit", "apply_patch")


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


def basename(path: str) -> str:
    return path.replace("\\", "/").rstrip("/").split("/")[-1]


def secret_path(path: str) -> bool:
    name = basename(path)
    if name == ".env.example":
        return False
    if name == ".env" or name.startswith(".env."):
        return True
    if name in {"id_rsa", "id_ed25519"}:
        return True
    if name.endswith((".pem", ".key")):
        return True
    return False


def collect_paths(tool_input: dict) -> list[str]:
    paths: list[str] = []
    for key in ("path", "file_path", "target_file", "target_notebook"):
        value = tool_input.get(key)
        if isinstance(value, str):
            paths.append(value)
    return paths


def collect_text(tool_input: dict) -> str:
    chunks: list[str] = []
    for key in ("contents", "content", "new_string", "streamContent", "patch"):
        value = tool_input.get(key)
        if isinstance(value, str):
            chunks.append(value)
    return "\n".join(chunks)


def is_mutation(tool_name: str) -> bool:
    folded = tool_name.lower()
    if "delete" in folded or "read" in folded:
        return False
    return any(token in folded for token in MUTATION)


def main() -> int:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return allow()
    if not isinstance(data, dict):
        return allow()

    tool_name = data.get("tool_name") or data.get("tool") or ""
    if not isinstance(tool_name, str) or not is_mutation(tool_name):
        return allow()

    tool_input = data.get("tool_input") or data.get("input") or {}
    if not isinstance(tool_input, dict):
        return allow()

    for path in collect_paths(tool_input):
        if secret_path(path):
            return deny(
                f"Запись в {basename(path)} заблокирована. Секреты не хранятся в репозитории.",
                "Разрешён только .env.example с плейсхолдерами change-me. Живой .env создаётся на VPS вручную.",
            )

    if PRIVATE_KEY.search(collect_text(tool_input)):
        return deny(
            "В содержимом файла обнаружен приватный ключ. Запись остановлена.",
            "Не сохраняй приватные ключи в репозиторий. Ключ деплоя кладётся в GitHub Secrets.",
        )

    return allow()


if __name__ == "__main__":
    raise SystemExit(main())