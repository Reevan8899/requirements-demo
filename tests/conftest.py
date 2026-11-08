import pytest

from src.note_manager import NoteManager


@pytest.fixture
def manager(tmp_path, monkeypatch):
    path = tmp_path / "notes.json"
    monkeypatch.setenv("NOTE_STORAGE", str(path))
    return NoteManager(path)
