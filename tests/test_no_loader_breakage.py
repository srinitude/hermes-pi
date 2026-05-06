"""R07b — assert the symlinked skill still parses with name: pi.

Walks the in-Hermes path (after `make link` runs in GREEN), confirms it
resolves to a real ``SKILL.md``, parses the YAML frontmatter, and asserts
``name == 'pi'`` so the Hermes skill loader continues to discover the
skill identically through the symlink.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

LINK_PATH = Path.home() / ".hermes/skills/autonomous-ai-agents/pi"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    assert m, f"{path} must start with --- YAML frontmatter ---"
    data = yaml.safe_load(m.group(1)) or {}
    assert isinstance(data, dict), f"{path} frontmatter must be a YAML mapping"
    return data


def test_in_hermes_path_resolves_through_symlink() -> None:
    assert LINK_PATH.is_symlink(), f"{LINK_PATH} must be a symlink"
    skill_md = LINK_PATH / "SKILL.md"
    assert skill_md.is_file(), f"{skill_md} must exist (resolved through symlink)"


def test_skill_frontmatter_name_is_pi() -> None:
    fm = _frontmatter(LINK_PATH / "SKILL.md")
    assert fm.get("name") == "pi", f"SKILL.md name must be 'pi', got {fm.get('name')!r}"


def test_skill_frontmatter_has_version() -> None:
    fm = _frontmatter(LINK_PATH / "SKILL.md")
    assert "version" in fm, "SKILL.md frontmatter must declare a version"


def test_references_dir_visible_through_symlink() -> None:
    refs = LINK_PATH / "references"
    assert refs.is_dir(), f"{refs} must be reachable through the symlink"
    md_files = list(refs.glob("*.md"))
    assert md_files, f"{refs} must contain reference markdown files"
