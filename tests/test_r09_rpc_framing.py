"""R09 — RPC framing pitfall warns against Node readline."""
from __future__ import annotations


def _section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start == -1:
        return ""
    nxt = text.find("\n## ", start + len(heading))
    return text[start:nxt] if nxt != -1 else text[start:]


def test_warns_against_node_readline(skill_md: str, all_md_text: str) -> None:
    rpc = _section(skill_md, "## RPC Mode")
    assert rpc, "## RPC Mode section missing"
    assert "Node readline" in rpc or "node readline" in rpc.lower(), \
        "## RPC Mode must mention Node readline"
    assert "LF-only" in all_md_text or "LF only" in all_md_text, \
        "must reference LF-only framing"
    assert "src/modes/rpc/jsonl.ts:14-19" in all_md_text or \
           "modes/rpc/jsonl.ts:14-19" in all_md_text, \
        "must cite jsonl.ts:14-19 for the framing rationale"
