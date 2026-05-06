"""R07a — assert .github/workflows/ci.yml runs the test suite on push/PR to main."""
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
    jobs = workflow.get("jobs") or {}
    runs = []
    for job in jobs.values():
        for step in job.get("steps", []):
            run = step.get("run")
            if isinstance(run, str):
                runs.append(run)
    blob = "\n".join(runs)
    assert "pytest" in blob or "mise run test" in blob, (
        "ci.yml must run `pytest` or `mise run test`"
    )


def test_workflow_uses_python_3_11(workflow: dict) -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert '"3.11"' in text or "'3.11'" in text or "python-version: 3.11" in text, (
        "ci.yml must pin Python 3.11"
    )
