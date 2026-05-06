"""Shared fixtures for pi-skill tests."""
from __future__ import annotations

import pathlib

import pytest

SKILL_ROOT = pathlib.Path.home() / ".hermes/skills/autonomous-ai-agents/pi"
OPENSRC_ROOT = pathlib.Path.home() / ".opensrc/repos/github.com/badlogic/pi-mono/main"
RESEARCH_ROOT = pathlib.Path.home() / "hermes-setup/skills/pi/research"


@pytest.fixture(scope="session")
def skill_root() -> pathlib.Path:
    return SKILL_ROOT


@pytest.fixture(scope="session")
def opensrc_root() -> pathlib.Path:
    return OPENSRC_ROOT


@pytest.fixture(scope="session")
def research_root() -> pathlib.Path:
    return RESEARCH_ROOT


@pytest.fixture(scope="session")
def skill_md(skill_root: pathlib.Path) -> str:
    md = skill_root / "SKILL.md"
    return md.read_text(encoding="utf-8") if md.exists() else ""


@pytest.fixture(scope="session")
def all_md_text(skill_root: pathlib.Path) -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in skill_root.rglob("*.md"))
