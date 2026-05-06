"""R11 — AgentSessionEvent / AgentEvent unions match docs/json.md."""
from __future__ import annotations

import pathlib
import re


def _ts_block_after(text: str, marker: str) -> str:
    pos = text.find(marker)
    if pos == -1:
        return ""
    code_open = text.find("```typescript", pos)
    if code_open == -1:
        return ""
    code_end = text.find("```", code_open + 13)
    return text[code_open + len("```typescript"):code_end].strip() if code_end != -1 else ""


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def test_agent_session_event_union_matches(opensrc_root: pathlib.Path, all_md_text: str) -> None:
    json_md = (opensrc_root / "packages/coding-agent/docs/json.md").read_text()
    upstream = _ts_block_after(json_md, "AgentSessionEvent`]")
    assert upstream, "could not extract AgentSessionEvent block from docs/json.md"
    assert _norm(upstream) in _norm(all_md_text), \
        "AgentSessionEvent union (docs/json.md) must appear verbatim in skill"


def test_agent_event_union_matches(opensrc_root: pathlib.Path, all_md_text: str) -> None:
    json_md = (opensrc_root / "packages/coding-agent/docs/json.md").read_text()
    upstream = _ts_block_after(json_md, "AgentEvent`]")
    assert upstream, "could not extract AgentEvent block from docs/json.md"
    assert _norm(upstream) in _norm(all_md_text), \
        "AgentEvent union (docs/json.md) must appear verbatim in skill"
