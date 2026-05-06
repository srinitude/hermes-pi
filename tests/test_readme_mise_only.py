"""M02 — README and contributor docs use the mise-only workflow exclusively.

User-facing contract: a new contributor reading README.md (and CONTRIBUTING.md)
must be able to clone, install tools, set up dependencies, link the in-Hermes
skill path, verify sync, run lint/test, and invoke local CI without ever seeing
or running ``make``. The README task table must enumerate the mise tasks; the
sync model must reference ``mise run sync`` and ``mise run verify-sync``; and
the document must explicitly note that Make is intentionally unsupported.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"

# Recognise `make <known target>` and `make -<flag>` while ignoring prose like
# "make sure" or "make sense". Not preceded by a word/path character so backtick
# usage `` `make sync` `` and shell-block lines `make link` are still caught.
_MAKE_TARGET_NAMES = (
    "install",
    "link",
    "unlink",
    "sync",
    "verify-sync",
    "test",
    "lint",
    "ci",
    "setup",
    "help",
)
_MAKE_CMD_PATTERN = re.compile(
    r"(?<![\w./-])make[ \t]+"
    r"(?:" + "|".join(re.escape(t) for t in _MAKE_TARGET_NAMES) + r"|-[A-Za-z])"
)

REQUIRED_QUICKSTART_FRAGMENTS = (
    "mise install",
    "mise run setup",
    "mise run ci",
    "mise run verify-sync",
)

REQUIRED_TASK_TABLE_TASKS = (
    "setup",
    "install",
    "link",
    "unlink",
    "sync",
    "verify-sync",
    "lint",
    "test",
    "ci",
)


def _readme_text() -> str:
    return README.read_text(encoding="utf-8")


def _contributing_text() -> str:
    return CONTRIBUTING.read_text(encoding="utf-8")


def test_readme_quickstart_includes_mise_only_commands() -> None:
    text = _readme_text()
    for fragment in REQUIRED_QUICKSTART_FRAGMENTS:
        assert fragment in text, (
            f"README quickstart must include `{fragment}`"
        )
    assert "mise run link" in text or "mise run install" in text, (
        "README quickstart must include `mise run link` or `mise run install`"
    )


def test_readme_contains_no_make_command_examples() -> None:
    text = _readme_text()
    matches = _MAKE_CMD_PATTERN.findall(text)
    assert not matches, (
        "README must not contain user-facing `make <target>` commands; "
        f"matches={matches!r}"
    )


def test_readme_drops_make_targets_section_for_mise_tasks_section() -> None:
    text = _readme_text()
    assert not re.search(r"^##\s*Make targets\b", text, re.MULTILINE), (
        "README must not have a `## Make targets` section heading"
    )
    assert re.search(r"^##\s*[Mm]ise\s+tasks\b", text, re.MULTILINE), (
        "README must have a `## mise tasks` (or `## Mise tasks`) section"
    )


@pytest.mark.parametrize("task", REQUIRED_TASK_TABLE_TASKS)
def test_readme_task_table_lists_each_required_mise_task(task: str) -> None:
    text = _readme_text()
    pattern = re.compile(rf"`mise\s+run\s+{re.escape(task)}`")
    assert pattern.search(text), (
        f"README task table must list `mise run {task}`"
    )


def test_readme_states_make_is_intentionally_unsupported() -> None:
    lower = _readme_text().lower()
    needles = (
        "make is not supported",
        "make is intentionally unsupported",
        "no makefile",
        "without make",
        "make is unsupported",
    )
    assert any(n in lower for n in needles), (
        "README must explicitly state Make is intentionally unsupported"
    )


def test_readme_sync_model_uses_mise_only() -> None:
    text = _readme_text()
    assert "mise run sync" in text, (
        "README sync model must reference `mise run sync`"
    )
    assert "mise run verify-sync" in text, (
        "README sync model must reference `mise run verify-sync`"
    )
    assert "mise run link" in text or "mise run install" in text, (
        "README sync model must reference `mise run link` or `mise run install`"
    )


def test_contributing_md_uses_mise_only_commands() -> None:
    text = _contributing_text()
    matches = _MAKE_CMD_PATTERN.findall(text)
    assert not matches, (
        "CONTRIBUTING.md must not include user-facing `make <target>` commands; "
        f"matches={matches!r}"
    )
    assert "mise run ci" in text, "CONTRIBUTING.md must reference `mise run ci`"
