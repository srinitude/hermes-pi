"""R06 — assert the first commit is published to srinitude/hermes-pi:main.

Network test: parses `gh api repos/srinitude/hermes-pi/branches/main` and
compares against `git rev-parse HEAD`. Skipped when `gh` is unavailable or
unauthenticated, since this contract can only be verified against the live
remote.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
REMOTE = "srinitude/hermes-pi"


def _gh_available() -> bool:
    if shutil.which("gh") is None:
        return False
    auth = subprocess.run(
        ["gh", "auth", "status"], capture_output=True, text=True, timeout=10
    )
    return auth.returncode == 0


pytestmark = pytest.mark.skipif(
    not _gh_available(),
    reason="gh CLI not available or not authenticated",
)


def _gh_branch_main_sha() -> str:
    result = subprocess.run(
        ["gh", "api", f"repos/{REMOTE}/branches/main"],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        pytest.fail(
            f"gh api repos/{REMOTE}/branches/main failed "
            f"(exit {result.returncode}):\n{result.stderr}"
        )
    payload = json.loads(result.stdout)
    return payload["commit"]["sha"]


def _local_head_sha() -> str:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
        capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 0, f"git rev-parse failed: {result.stderr}"
    return result.stdout.strip()


def test_remote_main_branch_exists() -> None:
    sha = _gh_branch_main_sha()
    assert len(sha) == 40, f"expected 40-char SHA, got {sha!r}"


def test_remote_main_matches_local_head() -> None:
    remote = _gh_branch_main_sha()
    local = _local_head_sha()
    assert remote == local, (
        f"origin/main is at {remote}, local HEAD is at {local}; "
        f"first push has not landed yet"
    )
