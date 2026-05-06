"""R03 — non-interactive mandate enforced."""
from __future__ import annotations

import re


def test_non_interactive_only_phrase(skill_md: str) -> None:
    assert "non-interactive only" in skill_md, "literal phrase 'non-interactive only' missing from SKILL.md"


def test_no_pi_tmux_send_keys(skill_md: str, all_md_text: str) -> None:
    forbidden = re.compile("tmux " + "send-keys" + r"[^\n]*\bpi\b", re.I)
    message = "SKILL.md must not pair " + "tmux " + "send-keys with pi"
    assert not forbidden.search(skill_md), message


def test_no_pi_pty_true(all_md_text: str) -> None:
    forbidden = re.compile("pty" + "=true" + r"[^\n]*\bpi\b", re.I)
    message = "no pi recipe may use " + "pty" + "=true"
    assert not forbidden.search(all_md_text), message
