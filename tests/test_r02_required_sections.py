"""R02 — required ## sections present in order."""
from __future__ import annotations

REQUIRED_SECTIONS = [
    "## Prerequisites",
    "## Pi Philosophy",
    "## Pi Primitives",
    "## Pi Extension Events (Hooks)",
    "## Non-Interactive Mode (Mandatory)",
    "## Fast Streaming Recipes",
    "## Hermes Integration Patterns",
    "## Worktree Isolation (Mandatory)",
    "## CLI Reference",
    "## Settings & Configuration",
    "## Sessions",
    "## Skills, Prompt Templates, Themes, Pi Packages",
    "## Extensions Authoring (Headless-Friendly Patterns)",
    "## RPC Mode",
    "## SDK Mode",
    "## MCP Bridging (Opt-In, Anti-Pattern by Default)",
    "## Environment Variables",
    "## Cost & Performance Tips",
    "## Pitfalls & Gotchas",
    "## Rules for Hermes Agents",
    "## Pi vs Claude Code (Side-By-Side)",
]


def test_all_sections_in_order(skill_md: str) -> None:
    last_pos = -1
    for section in REQUIRED_SECTIONS:
        pos = skill_md.find(section)
        assert pos != -1, f"missing required section: {section}"
        assert pos > last_pos, f"section out of order: {section}"
        last_pos = pos
