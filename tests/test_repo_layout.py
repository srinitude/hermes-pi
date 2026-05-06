"""R01 — assert the standalone repo carries every required file."""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = (
    "install.sh",
    "mise.toml",
    "pyproject.toml",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    ".gitignore",
    ".github/workflows/ci.yml",
    "scripts/verify-sync.sh",
    "SKILL.md",
)

REQUIRED_DIRS = (
    "references",
    "tests",
    "assets",
)


@pytest.mark.parametrize("relpath", REQUIRED_FILES)
def test_required_file_exists_and_non_empty(relpath: str) -> None:
    target = REPO_ROOT / relpath
    assert target.is_file(), f"{relpath} missing under {REPO_ROOT}"
    assert target.stat().st_size > 0, f"{relpath} is empty"


@pytest.mark.parametrize("relpath", REQUIRED_DIRS)
def test_required_dir_populated(relpath: str) -> None:
    target = REPO_ROOT / relpath
    assert target.is_dir(), f"{relpath}/ missing under {REPO_ROOT}"
    files = [p for p in target.rglob("*") if p.is_file()]
    assert files, f"{relpath}/ is empty"


def test_install_sh_executable() -> None:
    install_sh = REPO_ROOT / "install.sh"
    mode = install_sh.stat().st_mode
    assert mode & 0o111, "install.sh must be executable"


def test_verify_sync_executable() -> None:
    script = REPO_ROOT / "scripts/verify-sync.sh"
    mode = script.stat().st_mode
    assert mode & 0o111, "scripts/verify-sync.sh must be executable"
