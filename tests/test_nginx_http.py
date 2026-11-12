"""Порт 80 отдаёт /health, а не редирект. Это договорённость runbook."""

from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1] / "nginx" / "default.conf.template"


def test_port_80_proxies_health_before_redirect() -> None:
    text = TEMPLATE.read_text(encoding="utf-8")
    health = text.find("location = /health")
    redirect = text.find("return 301")

    assert health != -1
    assert redirect != -1
    assert health < redirect
