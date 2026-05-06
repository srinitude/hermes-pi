"""R08 — Hermes integration examples use terminal/process/mcp_skill_* exclusively."""
from __future__ import annotations

import re

ALLOWED_PREFIXES = ("terminal(", "process(", "mcp_skill_", "# Hermes:", "# hermes:")
FORBIDDEN_INLINE = ("subprocess.run", "os.system", "os.popen")


def _section(skill_md: str, heading: str) -> str:
    start = skill_md.find(heading)
    if start == -1:
        return ""
    next_h = skill_md.find("\n## ", start + len(heading))
    return skill_md[start:next_h] if next_h != -1 else skill_md[start:]


def _fenced(text: str) -> list[str]:
    return re.findall(r"```[a-zA-Z]*\n(.*?)```", text, re.S)


def test_hermes_section_blocks_are_terminal_or_process(skill_md: str) -> None:
    section = _section(skill_md, "## Hermes Integration Patterns")
    assert section, "## Hermes Integration Patterns missing"
    blocks = _fenced(section)
    assert blocks, "## Hermes Integration Patterns must contain code examples"
    for b in blocks:
        first = b.lstrip().splitlines()[0] if b.strip() else ""
        assert first.startswith(ALLOWED_PREFIXES), \
            f"code block must start with terminal/process/mcp_skill_/# Hermes: -- got: {first[:80]}"


def test_no_subprocess_in_hermes_section(skill_md: str) -> None:
    section = _section(skill_md, "## Hermes Integration Patterns")
    for tok in FORBIDDEN_INLINE:
        assert tok not in section, f"forbidden inline tool in Hermes section: {tok}"
