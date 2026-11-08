"""Публичный API для операций с заметками и адаптеров экспорта (BR-003)."""

from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from filelock import FileLock

from .messages import message
from .storage import Note, load_notes, save_notes


def _validate(title: str | None, body: str | None) -> None:
    for name, value, limit in (("title", title, 100), ("body", body, 10_000)):
        if value is None:
            continue
        if not value.strip():
            raise ValueError(message(f"{name}_required"))
        if len(value) > limit:
            raise ValueError(message(f"{name}_limit"))


class NoteManager:
    def __init__(self, path: Path):
        self.path = path.resolve()
        self.lock = FileLock(self.path.with_name(f"{self.path.name}.lock"), timeout=2, mode=0o600)

    def add_note(self, title: str, body: str) -> Note:
        """Создаёт заметку и возвращает присвоенный ID (FR-001)."""
        _validate(title, body)
        with self.lock:
            notes = self.list_notes()
            now = datetime.now(timezone.utc).isoformat()
            note = Note(uuid4().hex, title.strip(), body.strip(), now, now)
            notes.append(note)
            save_notes(self.path, notes)
        return note

    def list_notes(self) -> list[Note]:
        """Возвращает снимок хранилища (FR-002)."""
        return load_notes(self.path)

    def search_notes(self, query: str) -> list[Note]:
        """Ищет подстроку в заголовке и тексте без учёта регистра (FR-003)."""
        query = query.strip().casefold()
        if not query:
            raise ValueError(message("query_required"))
        return [note for note in self.list_notes() if query in note.title.casefold() or query in note.body.casefold()]

    def edit_note(self, note_id: str, *, title: str | None = None, body: str | None = None) -> Note:
        """Обновляет указанные поля существующей заметки (FR-004)."""
        if title is None and body is None:
            raise ValueError(message("edit_required"))
        _validate(title, body)
        with self.lock:
            notes = self.list_notes()
            index = self._index(notes, note_id)
            original = notes[index]
            updated = replace(
                original,
                title=original.title if title is None else title.strip(),
                body=original.body if body is None else body.strip(),
                updated_at=datetime.now(timezone.utc).isoformat(),
            )
            notes[index] = updated
            save_notes(self.path, notes)
        return updated

    def delete_note(self, note_id: str) -> None:
        """Удаляет заметку после подтверждения на уровне CLI (FR-005)."""
        with self.lock:
            notes = self.list_notes()
            del notes[self._index(notes, note_id)]
            save_notes(self.path, notes)

    @staticmethod
    def _index(notes: list[Note], note_id: str) -> int:
        for index, note in enumerate(notes):
            if note.id == note_id:
                return index
        raise ValueError(message("missing", id=note_id))
