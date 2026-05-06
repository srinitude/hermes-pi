"""R15 — MCP framed as opt-in / anti-pattern by default."""
from __future__ import annotations


def _section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start == -1:
        return ""
    nxt = text.find("\n## ", start + len(heading))
    return text[start:nxt] if nxt != -1 else text[start:]


def test_mcp_section_phrases(skill_md: str) -> None:
    section = _section(skill_md, "## MCP Bridging")
    assert section, "## MCP Bridging section missing"
    assert "opt-in" in section, "MCP Bridging must contain literal 'opt-in'"
    assert "anti-pattern by default" in section, \
        "MCP Bridging must contain literal 'anti-pattern by default'"


def test_mcp_section_cites_no_mcp(skill_md: str) -> None:
    section = _section(skill_md, "## MCP Bridging")
    assert "No MCP" in section or "no MCP" in section.lower(), \
        "MCP Bridging must cite the README's 'No MCP' philosophy line"
