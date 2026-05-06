"""R14 — forbidden-token regression sweep over the entire skill tree."""
from __future__ import annotations

import pathlib
import re

# Tokens that must not appear at all. The "Pi vs Claude Code" anti-pattern callout
# may reference forbidden tokens but only when paired with the word "anti-pattern"
# or "forbidden" or "do not".
FORBIDDEN = [
    "tmux send-keys",
    "pty=true",
    "expect <(echo",
    "--dangerously-skip-permissions",
]


def test_forbidden_tokens_only_in_anti_pattern_callouts(skill_root: pathlib.Path) -> None:
    issues = []
    for p in skill_root.rglob("*"):
        if not p.is_file() or p.suffix not in (".md", ".txt"):
            continue
        text = p.read_text(encoding="utf-8")
        for tok in FORBIDDEN:
            if tok not in text:
                continue
            # Allow only if every occurrence is within an anti-pattern call-out
            for line_no, line in enumerate(text.splitlines(), 1):
                if tok not in line:
                    continue
                window = "\n".join(text.splitlines()[max(0, line_no - 6):line_no + 4])
                if any(s in window.lower() for s in ("anti-pattern", "forbidden", "do not", "must not", "must never")):
                    continue
                issues.append((p.name, line_no, tok, line.strip()[:80]))
    assert not issues, f"forbidden tokens outside anti-pattern callouts: {issues}"
