"""R06 — every cited source path resolves under opensrc cache."""
from __future__ import annotations

import pathlib
import re

CITATION = re.compile(r"packages/coding-agent/[\w./-]+(?::(\d+)(?:-(\d+))?)?")


def test_all_citations_resolve(skill_root: pathlib.Path, opensrc_root: pathlib.Path) -> None:
    bad = []
    for f in skill_root.rglob("*.md"):
        text = f.read_text(encoding="utf-8")
        for match in CITATION.finditer(text):
            full = match.group(0).split(":")[0]
            target = opensrc_root / full
            if not target.exists():
                bad.append((f.relative_to(skill_root).as_posix(), match.group(0)))
    assert not bad, f"unresolved opensrc citations: {bad}"


def test_cited_line_ranges_within_file(skill_root: pathlib.Path, opensrc_root: pathlib.Path) -> None:
    bad = []
    for f in skill_root.rglob("*.md"):
        text = f.read_text(encoding="utf-8")
        for match in CITATION.finditer(text):
            full, start, end = match.group(0).split(":")[0], match.group(1), match.group(2)
            target = opensrc_root / full
            if not target.exists() or not start:
                continue
            n_lines = len(target.read_text(encoding="utf-8").splitlines())
            hi = int(end) if end else int(start)
            if int(start) < 1 or hi > n_lines:
                bad.append((f.name, match.group(0), n_lines))
    assert not bad, f"out-of-range citations: {bad}"
