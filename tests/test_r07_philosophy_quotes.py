"""R07 — verbatim philosophy quotes preserved with attribution."""
from __future__ import annotations

import pathlib

YT_QUOTE = "strip away everything and build a minimal extensible core"
README_QUOTE = "No MCP, no sub agents, no plan load, no background bash, no built-in to-do"


def test_yt_quote_in_philosophy(skill_root: pathlib.Path) -> None:
    f = skill_root / "references/pi-philosophy.md"
    assert f.exists(), "references/pi-philosophy.md missing"
    text = f.read_text()
    assert YT_QUOTE in text, f"missing verbatim YouTube quote: {YT_QUOTE!r}"


def test_readme_negation_list_in_philosophy(skill_root: pathlib.Path) -> None:
    f = skill_root / "references/pi-philosophy.md"
    text = f.read_text()
    assert README_QUOTE in text, f"missing verbatim quote: {README_QUOTE!r}"


def test_attribution_present(skill_root: pathlib.Path) -> None:
    f = skill_root / "references/pi-philosophy.md"
    text = f.read_text()
    assert "Dli5slNaJu0" in text or "youtube.com" in text.lower(), "YouTube attribution required"
    assert "README.md:466" in text or "Philosophy" in text, "README.md Philosophy attribution required"
