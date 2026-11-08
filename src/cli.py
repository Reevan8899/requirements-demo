"""Командный интерфейс менеджера заметок (FR-001 — FR-005)."""

import argparse
import os
import sys
from pathlib import Path

from filelock import Timeout

from .messages import message
from .note_manager import NoteManager
from .storage import InvalidStorageError, Note


class NoteParser(argparse.ArgumentParser):
    def error(self, detail: str) -> None:
        raise ValueError(message("syntax"))


def _parser() -> NoteParser:
    parser = NoteParser(prog="note", add_help=False)
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", add_help=False)
    add.add_argument("--title", required=True)
    add.add_argument("--body", required=True)
    commands.add_parser("list", add_help=False)
    search = commands.add_parser("search", add_help=False)
    search.add_argument("--query", required=True)
    edit = commands.add_parser("edit", add_help=False)
    edit.add_argument("id")
    edit.add_argument("--title")
    edit.add_argument("--body")
    commands.add_parser("delete", add_help=False).add_argument("id")
    return parser


def _print_notes(notes: list[Note], empty_message: str) -> None:
    if not notes:
        print(message(empty_message))
        return
    print(message("columns"))
    print("\n".join(f"{note.id} | {note.title} | {note.created_at}" for note in notes))


def _confirm_delete(note_id: str) -> bool:
    try:
        return input(message("confirm_delete", id=note_id)).strip().casefold() == "да"
    except (EOFError, KeyboardInterrupt):
        return False


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv in (["--help"], ["-h"]) or (len(argv) == 2 and argv[1] in ("--help", "-h")):
        print(message("help"))
        return 0

    try:
        args = _parser().parse_args(argv)
        path = Path(os.environ.get("NOTE_STORAGE", "~/.notes.json")).expanduser()
        manager = NoteManager(path)
        match args.command:
            case "add":
                print(message("created", id=manager.add_note(args.title, args.body).id))
            case "list":
                _print_notes(manager.list_notes(), "empty")
            case "search":
                _print_notes(manager.search_notes(args.query), "no_results")
            case "edit":
                updated = manager.edit_note(args.id, title=args.title, body=args.body)
                print(message("edited", id=updated.id))
            case "delete":
                if _confirm_delete(args.id):
                    manager.delete_note(args.id)
                    print(message("deleted", id=args.id))
                else:
                    print(message("cancelled"))
        return 0
    except Timeout:
        detail = message("locked")
    except (OSError, InvalidStorageError):
        detail = message("storage")
    except ValueError as exc:
        detail = str(exc)
    print(message("error", detail=detail), file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
