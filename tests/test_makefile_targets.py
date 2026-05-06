"""R03 — assert every required Makefile target dry-runs cleanly."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_TARGETS = (
    "install",
    "link",
    "unlink",
    "sync",
    "verify-sync",
    "test",
    "lint",
    "ci",
)


@pytest.mark.parametrize("target", REQUIRED_TARGETS)
def test_make_target_dry_runs(target: str) -> None:
    cmd = ["make", "-n", "-C", str(REPO_ROOT), target]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, (
        f"make -n {target} failed with exit {result.returncode}\n"
        f"stdout=\n{result.stdout}\nstderr=\n{result.stderr}"
    )


def test_makefile_uses_ff_only_for_sync() -> None:
    text = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    assert "--ff-only" in text, "Makefile sync target must use --ff-only merge"
    assert "rebase" not in text.lower(), (
        "Makefile must not use rebase semantics for sync"
    )


def test_makefile_link_target_invokes_install_sh() -> None:
    text = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    assert "install.sh" in text, "Makefile must delegate link to install.sh"
