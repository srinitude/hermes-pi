"""R16 — Pi-vs-Claude-Code parity table with >=12 cited rows."""
from __future__ import annotations

import pathlib
import re

REQUIRED_ROWS = [
    "non-interactive",
    "streaming",
    "extension",
    "MCP",
    "sub-agent",
    "plan mode",
    "permission",
    "session",
    "fast-startup",
    "RPC",
    "fallback",
    "structured",
]


def test_table_has_required_rows(skill_root: pathlib.Path) -> None:
    f = skill_root / "references/pi-vs-claude-code.md"
    assert f.exists(), "references/pi-vs-claude-code.md missing"
    text = f.read_text()
    rows = [line for line in text.splitlines() if line.startswith("| ") and "|" in line[2:]]
    assert len(rows) >= 14, f"need >=14 markdown table rows (incl. header+sep), got {len(rows)}"
    body = "\n".join(rows).lower()
    missing = [t for t in REQUIRED_ROWS if t.lower() not in body]
    assert not missing, f"missing required comparison rows: {missing}"


def test_each_data_row_has_pi_and_claude_code_citation(skill_root: pathlib.Path) -> None:
    text = (skill_root / "references/pi-vs-claude-code.md").read_text()
    pattern = re.compile(r"^\|[^|]+\|[^|]+\|[^|]+\|", re.M)
    rows = [m.group(0) for m in pattern.finditer(text)]
    data_rows = [r for r in rows if "---" not in r and not r.lower().startswith("| topic")
                 and not r.lower().startswith("| dimension") and not r.lower().startswith("| feature")]
    assert len(data_rows) >= 12, f"need >=12 data rows, got {len(data_rows)}"
    for r in data_rows:
        assert "packages/coding-agent" in r or "pi.dev" in r, f"row missing Pi citation: {r[:80]}"
