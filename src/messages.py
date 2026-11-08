"""Русскоязычные строки интерфейса (NFR-006)."""

import json
from importlib.resources import files

MESSAGES = json.loads(files("src").joinpath("messages_ru.json").read_text(encoding="utf-8"))


def message(key: str, **values: str) -> str:
    return MESSAGES[key].format(**values)
