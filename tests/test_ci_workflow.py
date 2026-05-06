"""R07a + M03 — `.github/workflows/ci.yml` triggers correctly and enters the
project gate through ``mise run ci``.

R07a (carried forward) asserts the workflow triggers on push/PR to ``main`` and
runs the test suite. M03 layers on the new mise-only contract: the workflow
must activate mise (e.g. via ``jdx/mise-action`` or ``mise install``) before
project commands and run ``mise run ci`` as the primary project gate, instead
of inlining ``uv run pytest`` / ``uv sync`` / ``uv run python -m compileall``.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = REPO_ROOT / ".github/workflows/ci.yml"


@pytest.fixture(scope="module")
def workflow() -> dict:
    assert WORKFLOW.is_file(), f"{WORKFLOW} missing"
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def _all_run_blobs(workflow: dict) -> list[str]:
    runs: list[str] = []
    for job in (workflow.get("jobs") or {}).values():
        for step in job.get("steps", []):
            run = step.get("run")
            if isinstance(run, str):
                runs.append(run)
    return runs


def test_workflow_has_name(workflow: dict) -> None:
    assert workflow.get("name"), "workflow must declare a name"


def test_workflow_triggers_push_to_main(workflow: dict) -> None:
    # PyYAML loads `on:` as the boolean True, so accept either key.
    on = workflow.get("on") or workflow.get(True)
    assert on, "workflow must declare an `on:` block"
    push = on.get("push") or {}
    branches = push.get("branches") or []
    assert "main" in branches, "workflow must trigger on push to main"


def test_workflow_triggers_pull_request_to_main(workflow: dict) -> None:
    on = workflow.get("on") or workflow.get(True)
    pr = on.get("pull_request") or {}
    branches = pr.get("branches") or []
    assert "main" in branches, "workflow must trigger on pull_request to main"


def test_workflow_runs_pytest(workflow: dict) -> None:
    blob = "\n".join(_all_run_blobs(workflow))
    assert "pytest" in blob or "mise run test" in blob or "mise run ci" in blob, (
        "ci.yml must run pytest (directly or via `mise run test` / `mise run ci`)"
    )


def test_workflow_uses_python_3_11(workflow: dict) -> None:
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    mise_text = (REPO_ROOT / "mise.toml").read_text(encoding="utf-8")
    pinned = (
        '"3.11"' in workflow_text
        or "'3.11'" in workflow_text
        or "python-version: 3.11" in workflow_text
        or 'python = "3.11"' in mise_text
        or "python = '3.11'" in mise_text
    )
    assert pinned, "Python 3.11 must be pinned in ci.yml or mise.toml"


# ---------------------------------------------------------------------------
# M03 — mise-only CI entrypoint contract
# ---------------------------------------------------------------------------


def test_workflow_activates_mise_before_project_commands() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    activates_mise = (
        "jdx/mise-action" in text
        or "mise install" in text
        or "mise activate" in text
    )
    assert activates_mise, (
        "ci.yml must activate mise (e.g. `jdx/mise-action`, `mise install`) "
        "before running project commands"
    )


def test_workflow_runs_mise_run_ci_as_primary_gate(workflow: dict) -> None:
    blob = "\n".join(_all_run_blobs(workflow))
    assert "mise run ci" in blob, (
        "ci.yml must run `mise run ci` as the primary project gate"
    )


def test_workflow_does_not_inline_uv_or_python_commands(workflow: dict) -> None:
    blob = "\n".join(_all_run_blobs(workflow))
    forbidden = (
        "uv run pytest",
        "uv run python -m compileall",
        "uv sync --extra dev",
    )
    for needle in forbidden:
        assert needle not in blob, (
            f"ci.yml must run `mise run ci` rather than inline `{needle}`"
        )
