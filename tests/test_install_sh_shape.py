"""R04 — assert install.sh implements the symlink + backup contract."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALL_SH = REPO_ROOT / "install.sh"


def _read() -> str:
    assert INSTALL_SH.is_file(), "install.sh missing"
    return INSTALL_SH.read_text(encoding="utf-8")


def test_install_sh_uses_ln_snf() -> None:
    text = _read()
    assert "ln -snf" in text, (
        "install.sh must end with an atomic `ln -snf` invocation; "
        "no cp/mv-based clobber is allowed."
    )


def test_install_sh_creates_timestamped_backup() -> None:
    text = _read()
    assert ".backup" in text, (
        "install.sh must back up under ~/.hermes/skills/autonomous-ai-agents/.backup/"
    )
    assert "pi-" in text, "install.sh backup target must include the pi- prefix"
    assert "%Y%m%dT%H%M%SZ" in text, (
        "install.sh must use an ISO8601-style UTC timestamp for the backup dir"
    )
    assert "mv " in text, "install.sh must move (not delete) the existing dir"


def test_install_sh_rejects_cp_r_installer() -> None:
    text = _read()
    forbidden = ("cp -r", "cp -R", "rsync ")
    for token in forbidden:
        assert token not in text, (
            f"install.sh must be a symlink installer, not a copy installer "
            f"(found `{token}`)"
        )


def test_install_sh_idempotent_when_already_linked() -> None:
    text = _read()
    assert "readlink" in text, (
        "install.sh must check the existing symlink target via readlink "
        "before replacing it"
    )


def test_install_sh_set_strict_bash() -> None:
    text = _read()
    assert text.startswith("#!/usr/bin/env bash"), "install.sh must be bash"
    assert "set -euo pipefail" in text, "install.sh must use set -euo pipefail"
