"""R02 — assert SKILL.md/references/tests/assets bytes match the BOOTSTRAP baseline."""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
BASELINE_MANIFEST = REPO_ROOT / "analysis/baseline-manifest.sha256"
IN_HERMES_PREFIX = "/.hermes/skills/autonomous-ai-agents/pi/"


def _parse_manifest() -> list[tuple[str, str]]:
    """Return (sha256, repo-relative path) for every line in the baseline manifest."""
    if not BASELINE_MANIFEST.is_file():
        return []
    rows: list[tuple[str, str]] = []
    for line in BASELINE_MANIFEST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        sha, _, path = line.partition("  ")
        idx = path.find(IN_HERMES_PREFIX)
        assert idx != -1, f"unexpected path in manifest: {path}"
        rel = path[idx + len(IN_HERMES_PREFIX):]
        rows.append((sha, rel))
    return rows


MANIFEST_ROWS = _parse_manifest()


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def test_baseline_manifest_present() -> None:
    assert BASELINE_MANIFEST.is_file(), "analysis/baseline-manifest.sha256 missing"
    assert MANIFEST_ROWS, "baseline manifest produced no entries"


@pytest.mark.parametrize(
    "expected_sha,relpath",
    MANIFEST_ROWS or [("0" * 64, "SKILL.md")],
    ids=lambda v: v[1] if isinstance(v, tuple) else str(v),
)
def test_skill_file_matches_baseline(expected_sha: str, relpath: str) -> None:
    repo_path = REPO_ROOT / relpath
    assert repo_path.is_file(), f"{relpath} missing in repo (expected from baseline)"
    actual = _hash_file(repo_path)
    assert actual == expected_sha, (
        f"{relpath} hash drifted: expected {expected_sha}, got {actual}"
    )
