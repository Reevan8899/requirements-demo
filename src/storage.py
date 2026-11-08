"""Локальное атомарное хранилище JSON (NFR-002, NFR-003)."""

import json
import os
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Note:
    id: str
    title: str
    body: str
    created_at: str
    updated_at: str


class InvalidStorageError(Exception):
    """Содержимое файла не соответствует формату хранилища."""


def load_notes(path: Path) -> list[Note]:
    try:
        with path.open(encoding="utf-8") as stream:
            records = json.load(stream)
    except FileNotFoundError:
        return []
    except (ValueError, UnicodeError) as exc:
        raise InvalidStorageError from exc

    if not isinstance(records, list):
        raise InvalidStorageError

    notes = []
    for record in records:
        if not isinstance(record, dict) or not all(isinstance(value, str) for value in record.values()):
            raise InvalidStorageError
        try:
            notes.append(Note(**record))
        except TypeError as exc:
            raise InvalidStorageError from exc
    return notes


def save_notes(path: Path, notes: list[Note]) -> None:
    # mkstemp creates a file accessible only to the owner on POSIX.
    descriptor, filename = tempfile.mkstemp(dir=path.parent, prefix=".notes-", suffix=".tmp")
    temporary = Path(filename)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump([asdict(note) for note in notes], stream, ensure_ascii=False)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
