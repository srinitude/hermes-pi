"""R05 — all 29 extension events documented + lifecycle asset present."""
from __future__ import annotations

import pathlib

EVENTS = [
    "resources_discover", "session_start", "session_before_switch",
    "session_before_fork", "session_before_compact", "session_compact",
    "session_shutdown", "session_before_tree", "session_tree", "context",
    "before_provider_request", "after_provider_response", "before_agent_start",
    "agent_start", "agent_end", "turn_start", "turn_end", "message_start",
    "message_update", "message_end", "tool_execution_start",
    "tool_execution_update", "tool_execution_end", "model_select",
    "thinking_level_select", "tool_call", "tool_result", "user_bash", "input",
]


def test_all_29_events_present(all_md_text: str) -> None:
    assert len(EVENTS) == 29, "test bug: must enumerate exactly 29 events"
    missing = [e for e in EVENTS if e not in all_md_text]
    assert not missing, f"missing events: {missing}"


def test_lifecycle_diagram_asset_exists(skill_root: pathlib.Path) -> None:
    asset = skill_root / "assets/pi-event-lifecycle.txt"
    assert asset.exists() and asset.read_text(), "assets/pi-event-lifecycle.txt must be non-empty"
    text = asset.read_text()
    assert "session_start" in text and "agent_start" in text and "turn_start" in text
