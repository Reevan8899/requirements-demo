# Матрица трассируемости (RTM)

- **Проект** — Менеджер заметок
- **Версия** — 1.0
- **Дата** — 8 ноября 2026 г.

Коммит в строке указывает на изменение, которое реализует или проверяет требование. Для пользовательских требований используется Issue соответствующей функции. Для NFR-005 критерий проверяется порогом покрытия в CI. Статусы требований ведутся в этой таблице.

| REQ | Тип | Приоритет | Issue | Коммит | Код или проверка | Тесты | Статус |
|---|---|---|---|---|---|---|---|
| [BR-001](requirements/business.md#br-001-автономность-пользователя) | BR | Must have | [#7](https://github.com/Reevan8899/requirements-demo/issues/7) | [`7b20917`](https://github.com/Reevan8899/requirements-demo/commit/7b20917a896367a9e7df84e9e128ef8f74490cbb) | [`storage.py`](../src/storage.py) | [`test_br001_works_without_network`](../tests/test_quality.py) | Реализовано |
| [BR-002](requirements/business.md#br-002-простота-использования) | BR | Must have | [#12](https://github.com/Reevan8899/requirements-demo/issues/12) | [`62ec85e`](https://github.com/Reevan8899/requirements-demo/commit/62ec85e8ea3595c8af04a4eff68b87429d319366) | Сценарий пользовательской приёмки | Ручной замер по Issue #12 | Требует приёмки |
| [BR-003](requirements/business.md#br-003-расширяемость) | BR | Should have | [#9](https://github.com/Reevan8899/requirements-demo/issues/9) | [`5d49602`](https://github.com/Reevan8899/requirements-demo/commit/5d49602d011f344e95af9da3a15eed27499de4b2) | [`note_manager.py`](../src/note_manager.py) | [`test_br003_external_adapter_reads_public_api`](../tests/test_quality.py) | Реализовано |
| [UR-001](requirements/user.md#ur-001-создание-заметки) | UR | Must have | [#1](https://github.com/Reevan8899/requirements-demo/issues/1) | [`6a23073`](https://github.com/Reevan8899/requirements-demo/commit/6a230736497eb2cb5da9e9120a66b1c6f4167abc) | [`cli.py`](../src/cli.py) | [`test_fr001_add_persists_note`](../tests/test_cli.py) | Реализовано |
| [UR-002](requirements/user.md#ur-002-просмотр-списка-заметок) | UR | Must have | [#2](https://github.com/Reevan8899/requirements-demo/issues/2) | [`6a23073`](https://github.com/Reevan8899/requirements-demo/commit/6a230736497eb2cb5da9e9120a66b1c6f4167abc) | [`cli.py`](../src/cli.py) | [`test_fr002_list_shows_id_title_date`](../tests/test_cli.py) | Реализовано |
| [UR-003](requirements/user.md#ur-003-поиск-по-заметкам) | UR | Should have | [#3](https://github.com/Reevan8899/requirements-demo/issues/3) | [`6a23073`](https://github.com/Reevan8899/requirements-demo/commit/6a230736497eb2cb5da9e9120a66b1c6f4167abc) | [`cli.py`](../src/cli.py) | [`test_fr003_matches_title_or_body_case_insensitively`](../tests/test_cli.py) | Реализовано |
| [UR-004](requirements/user.md#ur-004-редактирование-заметки) | UR | Should have | [#4](https://github.com/Reevan8899/requirements-demo/issues/4) | [`6a23073`](https://github.com/Reevan8899/requirements-demo/commit/6a230736497eb2cb5da9e9120a66b1c6f4167abc) | [`cli.py`](../src/cli.py) | [`test_fr004_updates_requested_fields`](../tests/test_cli.py) | Реализовано |
| [UR-005](requirements/user.md#ur-005-удаление-заметки) | UR | Could have | [#5](https://github.com/Reevan8899/requirements-demo/issues/5) | [`6a23073`](https://github.com/Reevan8899/requirements-demo/commit/6a230736497eb2cb5da9e9120a66b1c6f4167abc) | [`cli.py`](../src/cli.py) | [`test_fr005_requires_confirmation`](../tests/test_cli.py) | Реализовано |
| [FR-001](requirements/functional.md#fr-001-создание-заметки) | FR | Must have | [#1](https://github.com/Reevan8899/requirements-demo/issues/1) | [`5d49602`](https://github.com/Reevan8899/requirements-demo/commit/5d49602d011f344e95af9da3a15eed27499de4b2) | [`note_manager.py`](../src/note_manager.py) | [`test_fr001_*`](../tests/test_cli.py) | Реализовано |
| [FR-002](requirements/functional.md#fr-002-список-заметок) | FR | Must have | [#2](https://github.com/Reevan8899/requirements-demo/issues/2) | [`5d49602`](https://github.com/Reevan8899/requirements-demo/commit/5d49602d011f344e95af9da3a15eed27499de4b2) | [`note_manager.py`](../src/note_manager.py) | [`test_fr002_*`](../tests/test_cli.py) | Реализовано |
| [FR-003](requirements/functional.md#fr-003-поиск-заметок) | FR | Should have | [#3](https://github.com/Reevan8899/requirements-demo/issues/3) | [`5d49602`](https://github.com/Reevan8899/requirements-demo/commit/5d49602d011f344e95af9da3a15eed27499de4b2) | [`note_manager.py`](../src/note_manager.py) | [`test_fr003_*`](../tests/test_cli.py) | Реализовано |
| [FR-004](requirements/functional.md#fr-004-редактирование-заметки) | FR | Should have | [#4](https://github.com/Reevan8899/requirements-demo/issues/4) | [`5d49602`](https://github.com/Reevan8899/requirements-demo/commit/5d49602d011f344e95af9da3a15eed27499de4b2) | [`note_manager.py`](../src/note_manager.py) | [`test_fr004_*`](../tests/test_cli.py) | Реализовано |
| [FR-005](requirements/functional.md#fr-005-удаление-заметки) | FR | Could have | [#5](https://github.com/Reevan8899/requirements-demo/issues/5) | [`e42f158`](https://github.com/Reevan8899/requirements-demo/commit/e42f158ed357c9a3ef562102b8c9e1b1953d59b1) | [`cli.py`](../src/cli.py) | [`test_fr005_*`](../tests/test_cli.py) | Реализовано |
| [NFR-001](requirements/non-functional.md#nfr-001-производительность-списка) | NFR | Must have | [#6](https://github.com/Reevan8899/requirements-demo/issues/6) | [`55407a9`](https://github.com/Reevan8899/requirements-demo/commit/55407a972231ade824e0bb658dd8721532c0a47f) | [`cli.py`](../src/cli.py) | [`test_nfr001_list_10000_notes_under_500_ms`](../tests/test_quality.py) | Реализовано |
| [NFR-002](requirements/non-functional.md#nfr-002-атомарность-хранения) | NFR | Must have | [#7](https://github.com/Reevan8899/requirements-demo/issues/7) | [`7b20917`](https://github.com/Reevan8899/requirements-demo/commit/7b20917a896367a9e7df84e9e128ef8f74490cbb) | [`storage.py`](../src/storage.py) | [`test_nfr002_*`](../tests/test_quality.py) | Реализовано |
| [NFR-003](requirements/non-functional.md#nfr-003-права-доступа-к-хранилищу) | NFR | Should have | [#10](https://github.com/Reevan8899/requirements-demo/issues/10) | [`7b20917`](https://github.com/Reevan8899/requirements-demo/commit/7b20917a896367a9e7df84e9e128ef8f74490cbb) | [`storage.py`](../src/storage.py) | [`test_nfr003_storage_has_owner_only_permissions`](../tests/test_quality.py) | Реализовано (POSIX) |
| [NFR-004](requirements/non-functional.md#nfr-004-русскоязычные-ошибки) | NFR | Must have | [#8](https://github.com/Reevan8899/requirements-demo/issues/8) | [`e42f158`](https://github.com/Reevan8899/requirements-demo/commit/e42f158ed357c9a3ef562102b8c9e1b1953d59b1) | [`cli.py`](../src/cli.py) | [`test_nfr004_*`](../tests/test_cli.py) | Реализовано |
| [NFR-005](requirements/non-functional.md#nfr-005-покрытие-тестами-80) | NFR | Should have | [#9](https://github.com/Reevan8899/requirements-demo/issues/9) | [`c713787`](https://github.com/Reevan8899/requirements-demo/commit/c713787144a90079ecc6717d34519e7478e770ad) | [`traceability.yml`](../.github/workflows/traceability.yml) | Порог pytest-cov в CI | Реализовано |
| [NFR-006](requirements/non-functional.md#nfr-006-внешний-файл-локализации) | NFR | Could have | [#11](https://github.com/Reevan8899/requirements-demo/issues/11) | [`5d49602`](https://github.com/Reevan8899/requirements-demo/commit/5d49602d011f344e95af9da3a15eed27499de4b2) | [`messages_ru.json`](../src/messages_ru.json) | [`test_nfr004_help_and_syntax_errors_use_localized_messages`](../tests/test_cli.py) | Реализовано |

## Метрики

- В SRS 19 требований. Все 19 связаны с историей Git.
- Все 5 FR и 5 UR имеют тесты с явными метками `pytest.mark.req`.
- Реализовано 18 требований, включая режим `0600` на POSIX. BR-002 ожидает пользовательской приёмки.

| Тип | Всего | Реализовано | Требует приёмки |
|---|---:|---:|---:|
| BR | 3 | 2 | 1 |
| UR | 5 | 5 | 0 |
| FR | 5 | 5 | 0 |
| NFR | 6 | 6 | 0 |

## История изменений

| Дата | Изменение | Автор |
|---|---|---|
| 08.11.2026 | Добавлены связи с задачами, коммитами, кодом и тестами. | Reevan8899 |
