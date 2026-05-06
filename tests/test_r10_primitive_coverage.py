"""R10 — every Pi primitive token mentioned by exact string."""
from __future__ import annotations

REQUIRED_TOKENS = [
    "extensions", "skills", "prompts", "themes", "pi packages",
    "AGENTS.md", "SYSTEM.md", "~/.pi/agent", ".pi/",
    "--tools", "--no-tools", "--no-builtin-tools",
    "--session", "--fork", "--no-session",
    "--mode text", "--mode json", "--mode rpc",
    "-p/--print", "--offline",
    "PI_OFFLINE", "PI_SKIP_VERSION_CHECK",
    "non-interactive only",
    "AgentSessionEvent", "tool_call", "before_provider_request",
    "session_before_compact", "opt-in", "anti-pattern by default",
]


def test_required_tokens_present(all_md_text: str) -> None:
    missing = [t for t in REQUIRED_TOKENS if t not in all_md_text]
    assert not missing, f"missing required tokens: {missing}"
