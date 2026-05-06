"""R04 — fast-streaming recipe contains the canonical flag set."""
from __future__ import annotations

import re

CANONICAL_FLAGS = (
    "--mode json",
    "--offline",
    "--no-context-files",
    "--no-skills",
    "--no-prompt-templates",
    "--no-themes",
    "--no-extensions",
    "PI_SKIP_VERSION_CHECK",
)


def _fenced_blocks(text: str) -> list[str]:
    return re.findall(r"```[a-zA-Z]*\n(.*?)```", text, re.S)


def test_canonical_flag_set_in_one_block(all_md_text: str) -> None:
    blocks = _fenced_blocks(all_md_text)
    hits = [b for b in blocks if all(flag in b for flag in CANONICAL_FLAGS)]
    assert hits, f"no fenced block contains all canonical fast-startup flags: {CANONICAL_FLAGS}"


def test_jq_filter_present(all_md_text: str) -> None:
    blocks = _fenced_blocks(all_md_text)
    assert any("jq" in b for b in blocks), "at least one example must pipe through jq for stream filtering"
