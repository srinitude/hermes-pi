"""R01 — SKILL.md frontmatter shape."""
from __future__ import annotations

import pathlib
import re


def test_skill_md_has_valid_frontmatter(skill_md: str) -> None:
    assert skill_md, "SKILL.md must exist and be non-empty"
    assert skill_md.startswith("---\n"), "must start with YAML frontmatter"
    end = skill_md.find("\n---\n", 4)
    assert end != -1, "frontmatter must close with ---"
    fm = skill_md[4:end]
    assert re.search(r"^name:\s*pi\s*$", fm, re.M), "name: pi required"
    assert re.search(r"^description:\s*", fm, re.M), "description: required"
    assert "Use when" in fm or "use when" in fm.lower(), "trigger phrasing required"
    assert "Do NOT use" in fm or "do not use" in fm.lower(), "anti-trigger phrasing required"
    assert re.search(r"^license:", fm, re.M), "license required"
    assert re.search(r"^version:", fm, re.M), "version required"


def test_skill_md_tags_and_related(skill_md: str) -> None:
    assert skill_md, "SKILL.md must exist"
    end = skill_md.find("\n---\n", 4)
    fm = skill_md[4:end]
    for token in ("Coding-Agent", "Pi", "Non-Interactive", "JSON-Stream", "RPC", "Hermes-Integration"):
        assert token in fm, f"frontmatter missing tag/keyword: {token}"
    assert "claude-code" in fm, "related_skills must include claude-code"
