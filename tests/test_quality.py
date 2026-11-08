import io
import json
import os
import socket
import stat
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
from dataclasses import asdict
from time import perf_counter

import pytest

from src import storage
from src.cli import main
from src.note_manager import NoteManager


@pytest.mark.req("BR-001")
def test_br001_works_without_network(manager, monkeypatch, capsys):
    def no_network(*args, **kwargs):
        pytest.fail("Офлайн-сценарий попытался открыть сокет")

    monkeypatch.setattr(socket, "socket", no_network)
    assert main(["add", "--title", "Офлайн", "--body", "Текст"]) == 0
    note, = manager.list_notes()
    assert main(["edit", note.id, "--body", "Изменённый текст"]) == 0
    assert main(["search", "--query", "изменённый"]) == 0
    assert note.id in capsys.readouterr().out


@pytest.mark.req("BR-003")
def test_br003_external_adapter_reads_public_api(manager):
    def export_lines(source):
        return [f"{note.title}: {note.body}" for note in source.list_notes()]

    manager.add_note("Тема", "Текст")
    assert export_lines(manager) == ["Тема: Текст"]


@pytest.mark.req("NFR-001")
def test_nfr001_list_10000_notes_under_500_ms(manager):
    note = asdict(manager.add_note("Короткий заголовок", "Короткий текст"))
    records = [dict(note, id=str(index)) for index in range(10_000)]
    manager.path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    output = io.StringIO()
    with redirect_stdout(output):
        start = perf_counter()
        result = main(["list"])
        elapsed = perf_counter() - start
    assert result == 0
    assert len(output.getvalue().splitlines()) == 10_001
    assert elapsed <= 0.500, f"Формирование списка заняло {elapsed * 1000:.1f} мс"


@pytest.mark.req("NFR-002")
def test_nfr002_failed_replace_leaves_previous_file(manager, monkeypatch):
    original = manager.add_note("Исходная", "Текст")

    def fail_replace(source, destination):
        raise OSError("Имитация сбоя до атомарной замены")

    monkeypatch.setattr(storage.os, "replace", fail_replace)
    with pytest.raises(OSError, match="Имитация сбоя"):
        manager.add_note("Новая", "Текст")
    assert manager.list_notes() == [original]
    assert list(manager.path.parent.glob("*.tmp")) == []


@pytest.mark.req("NFR-002")
def test_nfr002_parallel_additions_preserve_all_notes(manager):
    def add(index):
        return NoteManager(manager.path).add_note(str(index), "Текст").id

    with ThreadPoolExecutor(max_workers=4) as pool:
        ids = set(pool.map(add, range(12)))
    assert len(ids) == 12
    assert {note.id for note in manager.list_notes()} == ids


@pytest.mark.req("NFR-003")
@pytest.mark.skipif(os.name != "posix", reason="Режим 0600 проверяется на POSIX")
def test_nfr003_storage_has_owner_only_permissions(manager):
    manager.add_note("Тема", "Текст")
    assert stat.S_IMODE(manager.path.stat().st_mode) == 0o600
    manager.path.chmod(0o644)
    manager.add_note("Тема 2", "Текст")
    assert stat.S_IMODE(manager.path.stat().st_mode) == 0o600
