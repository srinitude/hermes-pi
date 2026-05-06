"""Repo-root pytest hooks — skip skill tests that require optional resources.

The in-Hermes pi tests under ``tests/test_r0*.py`` need three external
prerequisites that may not be present in every environment (CI, fresh clone,
etc.):

* the upstream ``pi`` CLI on ``PATH`` (used by ``test_r12_smoke``),
* the opensrc cache for ``github.com/badlogic/pi-mono`` at
  ``~/.opensrc/repos/github.com/badlogic/pi-mono/main`` (used by ``test_r06``
  and ``test_r11``),
* the research scrapes at ``~/hermes-setup/skills/pi/research``.

This hook applies pytest skip markers when those preconditions are missing so
the repo-sync invariant suite stays green in clean CI runners while the full
skill test suite still runs locally with all dependencies in place.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

OPENSRC_PI_ROOT = Path.home() / ".opensrc/repos/github.com/badlogic/pi-mono/main"
RESEARCH_ROOT = Path.home() / "hermes-setup/skills/pi/research"

PI_BIN_TESTS = ("test_r12_smoke",)
OPENSRC_TESTS = ("test_r06_source_traceability", "test_r11_agent_session_event")
RESEARCH_TESTS = ()


def _has_pi_binary() -> bool:
    return shutil.which("pi") is not None


def _has_opensrc_cache() -> bool:
    return OPENSRC_PI_ROOT.exists()


def _has_research() -> bool:
    return RESEARCH_ROOT.exists()


def pytest_collection_modifyitems(config, items):
    """Apply skipif markers when external prerequisites are missing."""
    skip_pi = pytest.mark.skip(reason="pi CLI not on PATH")
    skip_opensrc = pytest.mark.skip(
        reason=f"opensrc cache missing: {OPENSRC_PI_ROOT}"
    )
    skip_research = pytest.mark.skip(reason=f"research dir missing: {RESEARCH_ROOT}")

    pi_ok = _has_pi_binary()
    opensrc_ok = _has_opensrc_cache()
    research_ok = _has_research()

    for item in items:
        node = item.nodeid
        if not pi_ok and any(name in node for name in PI_BIN_TESTS):
            item.add_marker(skip_pi)
        if not opensrc_ok and any(name in node for name in OPENSRC_TESTS):
            item.add_marker(skip_opensrc)
        if not research_ok and any(name in node for name in RESEARCH_TESTS):
            item.add_marker(skip_research)
