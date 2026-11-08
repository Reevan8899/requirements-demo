import pytest

from src.cli import main


@pytest.mark.req("FR-001", "UR-001")
def test_fr001_add_persists_note(manager, capsys):
    assert main(["add", "--title", "Заголовок", "--body", "Текст"]) == 0
    note, = manager.list_notes()
    assert (note.title, note.body) == ("Заголовок", "Текст")
    assert capsys.readouterr().out.strip() == f"Заметка создана. ID: {note.id}"


@pytest.mark.req("FR-001", "NFR-004")
@pytest.mark.parametrize(("title", "body", "error"), [
    (" ", "Текст", "Заголовок обязателен"),
    ("я" * 101, "Текст", "Заголовок слишком длинный"),
    ("Заголовок", "", "Тело заметки обязательно"),
    ("Заголовок", "я" * 10_001, "Тело заметки слишком длинное"),
])
def test_fr001_rejects_invalid_fields(manager, capsys, title, body, error):
    assert main(["add", "--title", title, "--body", body]) == 2
    assert capsys.readouterr().err.startswith(f"Ошибка: {error}.")
    assert manager.list_notes() == []


@pytest.mark.req("FR-001")
def test_fr001_accepts_inclusive_limits(manager):
    assert main(["add", "--title", "а" * 100, "--body", "я" * 10_000]) == 0
    note, = manager.list_notes()
    assert (len(note.title), len(note.body)) == (100, 10_000)


@pytest.mark.req("FR-002", "UR-002")
def test_fr002_empty(manager, capsys):
    assert main(["list"]) == 0
    assert capsys.readouterr().out.strip() == "Заметок пока нет."


@pytest.mark.req("FR-002", "UR-002")
def test_fr002_list_shows_id_title_date(manager, capsys):
    notes = [manager.add_note("Первая", "A"), manager.add_note("Вторая", "Б")]
    assert main(["list"]) == 0
    assert capsys.readouterr().out.splitlines() == [
        "ID | Заголовок | Дата создания",
        *(f"{note.id} | {note.title} | {note.created_at}" for note in notes),
    ]


@pytest.mark.req("FR-003", "UR-003")
@pytest.mark.parametrize("query", ["ВСТРЕЧ", "пятНИЦ"])
def test_fr003_matches_title_or_body_case_insensitively(manager, capsys, query):
    matched = manager.add_note("Встреча", "В пятницу")
    other = manager.add_note("Покупки", "Хлеб")
    assert main(["search", "--query", query]) == 0
    output = capsys.readouterr().out
    assert matched.id in output and other.id not in output


@pytest.mark.req("FR-003")
def test_fr003_handles_missing_matches_and_empty_query(manager, capsys):
    assert main(["search", "--query", "задача"]) == 0
    assert "Совпадений нет" in capsys.readouterr().out
    assert main(["search", "--query", " "]) == 2
    assert "Укажите непустое значение --query" in capsys.readouterr().err


@pytest.mark.req("FR-004", "UR-004")
@pytest.mark.parametrize("changes", [{"title": "Новый"}, {"body": "Новый текст"}, {"title": "Новый", "body": "Новый текст"}])
def test_fr004_updates_requested_fields(manager, capsys, changes):
    original = manager.add_note("Старый", "Старый текст")
    flags = [value for name, field in changes.items() for value in (f"--{name}", field)]
    assert main(["edit", original.id, *flags]) == 0
    updated, = manager.list_notes()
    assert (updated.id, updated.created_at) == (original.id, original.created_at)
    assert updated.updated_at >= original.updated_at
    assert updated.title == changes.get("title", original.title)
    assert updated.body == changes.get("body", original.body)
    assert "Заметка обновлена" in capsys.readouterr().out


@pytest.mark.req("FR-004", "NFR-004")
def test_fr004_keeps_original_after_invalid_edit(manager, capsys):
    original = manager.add_note("Старый", "Текст")
    assert main(["edit", original.id]) == 2
    assert "Передайте --title" in capsys.readouterr().err
    assert main(["edit", original.id, "--title", "а" * 101]) == 2
    assert "Сократите" in capsys.readouterr().err
    assert main(["edit", "unknown", "--body", "Текст"]) == 2
    assert "Проверьте ID командой note list" in capsys.readouterr().err
    assert manager.list_notes() == [original]


@pytest.mark.req("FR-005", "UR-005")
def test_fr005_requires_confirmation(manager, capsys, monkeypatch):
    note = manager.add_note("Лишнее", "Текст")
    monkeypatch.setattr("builtins.input", lambda prompt: "нет")
    assert main(["delete", note.id]) == 0
    assert "Удаление отменено" in capsys.readouterr().out
    assert manager.list_notes() == [note]
    monkeypatch.setattr("builtins.input", lambda prompt: " ДА ")
    assert main(["delete", note.id]) == 0
    assert "Заметка удалена" in capsys.readouterr().out
    assert manager.list_notes() == []
    assert main(["delete", note.id]) == 2
    assert "не найдена" in capsys.readouterr().err


@pytest.mark.req("FR-005")
def test_fr005_eof_cancels_delete(manager, monkeypatch):
    def end_of_input(prompt):
        raise EOFError

    note = manager.add_note("Лишнее", "Текст")
    monkeypatch.setattr("builtins.input", end_of_input)
    assert main(["delete", note.id]) == 0
    assert manager.list_notes() == [note]


@pytest.mark.req("NFR-004", "NFR-006")
def test_nfr004_help_and_syntax_errors_use_localized_messages(manager, capsys):
    assert main(["--help"]) == 0
    assert "Менеджер заметок" in capsys.readouterr().out
    assert main(["unknown"]) == 2
    assert "Выполните note --help" in capsys.readouterr().err


@pytest.mark.req("NFR-004")
@pytest.mark.parametrize("contents", ["[broken", "{}", "[0]", "[{}]"])
def test_nfr004_invalid_storage_is_preserved(manager, capsys, contents):
    manager.path.write_text(contents, encoding="utf-8")
    assert main(["add", "--title", "Новое", "--body", "Текст"]) == 2
    assert "Проверьте права доступа" in capsys.readouterr().err
    assert manager.path.read_text(encoding="utf-8") == contents
