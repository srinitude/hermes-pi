"""R05 — assert symlink + clean tree + main-branch invariants."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LINK_PATH = Path.home() / ".hermes/skills/autonomous-ai-agents/pi"


def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), capture_output=True, text=True, cwd=cwd, timeout=30
    )


def test_in_hermes_path_is_symlink() -> None:
    assert LINK_PATH.is_symlink(), (
        f"{LINK_PATH} must be a symlink, not a regular directory"
    )


def test_symlink_resolves_to_repo_root() -> None:
    assert LINK_PATH.is_symlink(), f"{LINK_PATH} not a symlink"
    link_real = os.path.realpath(str(LINK_PATH))
    repo_real = os.path.realpath(str(REPO_ROOT))
    assert link_real == repo_real, (
        f"{LINK_PATH} resolves to {link_real}, expected {repo_real}"
    )


def test_repo_branch_is_main() -> None:
    result = _run("git", "rev-parse", "--abbrev-ref", "HEAD", cwd=REPO_ROOT)
    assert result.returncode == 0, f"git rev-parse failed: {result.stderr}"
    assert result.stdout.strip() == "main", (
        f"branch must be main, got {result.stdout.strip()}"
    )


def test_repo_working_tree_clean() -> None:
    result = _run("git", "status", "--porcelain", cwd=REPO_ROOT)
    assert result.returncode == 0, f"git status failed: {result.stderr}"
    assert result.stdout == "", (
        f"working tree must be clean; dirty entries:\n{result.stdout}"
    )
