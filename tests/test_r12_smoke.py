"""R12 — pi smoke commands exit deterministically (no hang)."""
from __future__ import annotations

import os
import shutil
import subprocess


def test_pi_binary_present() -> None:
    assert shutil.which("pi"), "pi binary required on PATH"


def test_pi_version_exits_zero() -> None:
    r = subprocess.run(["pi", "--version"], capture_output=True, text=True, timeout=10)
    assert r.returncode == 0, f"pi --version failed: {r.stderr}"
    out = (r.stdout + r.stderr).strip()
    assert out, "pi --version must print a version string"


def test_pi_help_documents_mode_flag() -> None:
    r = subprocess.run(["pi", "--help"], capture_output=True, text=True, timeout=10)
    assert r.returncode == 0
    out = r.stdout + r.stderr
    assert "--mode <mode>" in out, "pi --help must document --mode <mode>"


def test_pi_print_mode_smoke_exits_within_30s() -> None:
    env = {**os.environ, "PI_OFFLINE": "1", "PI_SKIP_VERSION_CHECK": "1"}
    cmd = [
        "pi", "-p", "--offline", "--no-extensions", "--no-skills",
        "--no-context-files", "--no-prompt-templates", "--no-themes",
        "--no-tools", "ping",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=env)
    # Exit code 0 = succeeded, non-zero = deterministic auth-error. Either is acceptable.
    # The contract forbids hangs (TimeoutExpired raises before this assertion).
    assert isinstance(r.returncode, int), "pi -p must produce a deterministic exit code"
