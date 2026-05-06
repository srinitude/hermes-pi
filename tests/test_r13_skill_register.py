"""R13 — skill registers (lives at expected category path)."""
from __future__ import annotations

import pathlib


def test_skill_directory_under_autonomous_ai_agents(skill_root: pathlib.Path) -> None:
    parts = skill_root.parts
    assert parts[-2:] == ("autonomous-ai-agents", "pi"), \
        f"skill must be at autonomous-ai-agents/pi, got: {skill_root}"


def test_skill_md_present(skill_root: pathlib.Path) -> None:
    assert (skill_root / "SKILL.md").exists(), "SKILL.md must exist for skill registration"


def test_skill_md_min_length(skill_md: str) -> None:
    assert len(skill_md) >= 8000, f"SKILL.md must be >= 8000 chars (got {len(skill_md)})"
    assert len(skill_md) <= 30000, f"SKILL.md must be <= 30000 chars (got {len(skill_md)})"
