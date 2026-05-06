"""R17 — worktree isolation required for mutating Pi recipes."""
from __future__ import annotations

import pathlib

REQUIRED_TOKENS = [
    "## Worktree Isolation (Mandatory)",
    "git worktree add",
    "workdir=",
    "no native --worktree",
    "packages/coding-agent/src/cli/args.ts:70-189",
    "packages/coding-agent/src/core/footer-data-provider.ts:12-15",
]


def test_skill_md_has_mandatory_worktree_heading(skill_md: str) -> None:
    assert "## Worktree Isolation (Mandatory)" in skill_md, \
        "SKILL.md must include ## Worktree Isolation (Mandatory)"


def test_required_tokens_present_across_md(all_md_text: str) -> None:
    missing = [t for t in REQUIRED_TOKENS if t not in all_md_text]
    assert not missing, f"missing worktree tokens: {missing}"


def test_reference_file_present(skill_root: pathlib.Path) -> None:
    f = skill_root / "references/pi-worktree-isolation.md"
    assert f.exists() and f.read_text(), "references/pi-worktree-isolation.md missing or empty"


def test_worktree_terminal_recipe_has_workdir(skill_root: pathlib.Path) -> None:
    text = (skill_root / "references/pi-worktree-isolation.md").read_text()
    assert "terminal(" in text and "workdir=" in text, \
        "worktree reference must show terminal(..., workdir=<worktree>) example"
    assert "git worktree add" in text and "git worktree remove" in text, \
        "worktree reference must include both add and remove cleanup"
