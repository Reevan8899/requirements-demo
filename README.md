# Requirements Demo

[![Traceability Check](https://github.com/Reevan8899/requirements-demo/actions/workflows/traceability.yml/badge.svg?branch=main&event=push)](https://github.com/Reevan8899/requirements-demo/actions/workflows/traceability.yml)

Учебный консольный менеджер заметок. Приложение создаёт, показывает, ищет, изменяет и удаляет записи в локальном JSON-файле.

## Быстрый старт

Нужен Python 3.10 или новее. Создайте и активируйте виртуальное окружение, затем выполните команды из корня репозитория.

```sh
python -m pip install -r requirements.txt
note --help
note add --title "Покупки" --body "Хлеб и молоко"
note list
note search --query "ХЛЕБ"
```

Для редактирования и удаления скопируйте ID из списка. Команда `note delete ID` запросит подтверждение. Хранилище по умолчанию — `~/.notes.json`. Переменная `NOTE_STORAGE` задаёт путь к другому файлу.

## Документация и проверки

- [Спецификация требований](docs/srs.md)
- [Матрица трассируемости](docs/traceability.md)
- [Глоссарий](docs/glossary.md)
- [Задачи по требованиям](https://github.com/Reevan8899/requirements-demo/issues?q=label%3Arequirement)

```sh
python -m pytest -v --cov=src --cov-report=term-missing --cov-fail-under=80
python scripts/check_traceability.py --report docs/traceability-report.md
```

`src/` содержит приложение, `tests/` — тесты, `docs/` — документацию, `scripts/` — проверку трассируемости. CI публикует Markdown-отчёт как артефакт `traceability-report`. В ручном запуске workflow параметр `simulate_low_coverage` включает демонстрацию отказа при недостаточном покрытии.

## Сообщения коммитов

Установите Node.js 24 и pnpm, затем выполните `pnpm install --frozen-lockfile`. Husky установит хук `commit-msg`. Для `feat`, `fix` и `test` в конце темы обязательна ссылка на требование, например `feat(notes): support searching by title (FR-003)`.
