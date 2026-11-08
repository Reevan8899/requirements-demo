"""Сверяет определения SRS, историю Git, тесты pytest и статусы RTM."""

import argparse
import ast
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQ_ID = r"(?:BR|UR|FR|NFR)-[0-9]{3}"
DEFINITION = re.compile(rf"^## ({REQ_ID}):\s+\S", re.MULTILINE)
RTM_ROW = re.compile(rf"^\|\s*\[?({REQ_ID})(?=\]|\s|\|)")


def collect_test_links() -> dict[str, set[str]]:
    links = defaultdict(set)
    for path in sorted((ROOT / "tests").rglob("test_*.py")):
        syntax = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for test in syntax.body:
            if not isinstance(test, ast.FunctionDef) or not test.name.startswith("test_"):
                continue
            for marker in test.decorator_list:
                if not isinstance(marker, ast.Call) or ast.unparse(marker.func) != "pytest.mark.req":
                    continue
                for arg in marker.args:
                    if not isinstance(arg, ast.Constant) or not isinstance(arg.value, str):
                        raise ValueError(f"{path.name}::{test.name}: ID в метке req должен быть строкой")
                    links[arg.value].add(f"{path.name}::{test.name}")
    return links


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="путь для сохранения Markdown-отчёта")
    args = parser.parse_args()

    definitions = Counter(
        req for path in (ROOT / "docs" / "requirements").glob("*.md")
        for req in DEFINITION.findall(path.read_text(encoding="utf-8"))
    )
    requirements = set(definitions)
    if not requirements:
        print("Не найдено ни одного определения требования в SRS.")
        return 1

    history = subprocess.check_output(["git", "log", "--format=%B"], cwd=ROOT, encoding="utf-8")
    commits = set(re.findall(rf"\b{REQ_ID}\b", history))
    tests = collect_test_links()
    statuses = {}
    rtm = ROOT / "docs" / "traceability.md"
    for line in rtm.read_text(encoding="utf-8").splitlines():
        if match := RTM_ROW.match(line):
            statuses[match[1]] = line.rstrip("|").rsplit("|", 1)[-1].strip()

    problems = []
    for req, count in sorted(definitions.items()):
        if count > 1:
            problems.append(f"{req}: повторное определение в SRS")
        if req not in statuses:
            problems.append(f"{req}: отсутствует строка RTM")
        if req not in commits:
            detail = "в RTM реализовано, но нет коммита" if statuses.get(req, "").startswith("Реализовано") else "нет коммита"
            problems.append(f"{req}: {detail}")
        if req.startswith(("FR-", "UR-")) and req not in tests and statuses.get(req) != "Архивировано":
            problems.append(f"{req}: нет теста с меткой pytest.mark.req")
    for req in sorted(tests.keys() - requirements):
        locations = ", ".join(sorted(tests[req]))
        problems.append(f"{req}: тест ссылается на неизвестное требование ({locations})")
    for req in sorted(statuses.keys() - requirements):
        problems.append(f"{req}: строка RTM ссылается на неизвестное требование")

    summary = [
        f"Всего требований: {len(requirements)}",
        f"Упомянуто в коммитах: {len(requirements & commits)}/{len(requirements)}",
        f"Связано с тестами: {len(requirements & tests.keys())}/{len(requirements)}",
        "Проверка пройдена." if not problems else f"Найдено проблем: {len(problems)}",
    ]
    print("\n".join(summary + [f"- {problem}" for problem in problems]))
    if args.report:
        report = ["# Проверка трассируемости", "", *(f"- {line}" for line in summary), "",
                  "| Требование | В истории Git | Тесты pytest | Статус RTM |",
                  "|---|---|---|---|"]
        for req in sorted(requirements):
            names = ", ".join(f"`{name}`" for name in sorted(tests.get(req, ()))) or "—"
            found = "Да" if req in commits else "Нет"
            report.append(f"| {req} | {found} | {names} | {statuses.get(req, '—')} |")
        if problems:
            report.extend(["", "## Проблемы", "", *(f"- {problem}" for problem in problems)])
        args.report.write_text("\n".join(report) + "\n", encoding="utf-8")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
