"""M01 — mise.toml is the sole project task registry; no Makefile interface.

User-facing contract: contributors invoke project work through ``mise install``,
``mise tasks ls``, and ``mise run <task>``. Make is intentionally unsupported,
so the repository must not ship a ``Makefile`` and ``mise.toml`` must register
every task a contributor needs (setup, install, link, unlink, sync, verify-sync,
lint, test, ci) with clear descriptions and the sync/link semantics preserved.
"""
from __future__ import annotations

import shutil
import subprocess
import tomllib
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
MISE_TOML = REPO_ROOT / "mise.toml"

REQUIRED_TASKS = (
    "setup",
    "install",
    "link",
    "unlink",
    "sync",
    "verify-sync",
    "lint",
    "test",
    "ci",
)


def _load_tasks() -> dict[str, Any]:
    data = tomllib.loads(MISE_TOML.read_text(encoding="utf-8"))
    tasks = data.get("tasks") or {}
    assert isinstance(tasks, dict), "mise.toml [tasks] must be a table"
    return tasks


def _payload_text(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    bits: list[str] = []
    run = payload.get("run")
    if isinstance(run, str):
        bits.append(run)
    elif isinstance(run, list):
        bits.extend(str(part) for part in run)
    description = payload.get("description")
    if isinstance(description, str):
        bits.append(description)
    return "\n".join(bits)


@pytest.mark.parametrize("name", REQUIRED_TASKS)
def test_mise_toml_registers_required_task_with_description(name: str) -> None:
    tasks = _load_tasks()
    assert name in tasks, f"mise.toml must register required task '{name}'"
    payload = tasks[name]
    assert isinstance(payload, dict), f"task '{name}' must be a TOML table"
    description = payload.get("description")
    assert isinstance(description, str) and description.strip(), (
        f"mise task '{name}' must have a non-empty description"
    )


def test_mise_sync_task_is_fast_forward_only() -> None:
    tasks = _load_tasks()
    text = _payload_text(tasks.get("sync"))
    assert "--ff-only" in text, "mise sync task must use `--ff-only` merge"
    assert "rebase" not in text.lower(), (
        "mise sync task must not rebase (sync is fast-forward only)"
    )


def test_mise_link_task_delegates_to_install_sh() -> None:
    tasks = _load_tasks()
    text = _payload_text(tasks.get("link"))
    assert "install.sh" in text, (
        "mise link task must invoke install.sh for the symlink installer"
    )


def test_mise_install_task_aliases_link() -> None:
    tasks = _load_tasks()
    install = tasks.get("install") or {}
    deps = install.get("depends") if isinstance(install, dict) else None
    text = _payload_text(install)
    delegated = bool(deps) and "link" in deps
    assert delegated or "install.sh" in text, (
        "mise install task must depend on `link` or invoke install.sh directly"
    )


def test_mise_verify_sync_task_runs_verify_sync_script() -> None:
    tasks = _load_tasks()
    text = _payload_text(tasks.get("verify-sync"))
    assert "verify-sync.sh" in text, (
        "mise verify-sync task must invoke scripts/verify-sync.sh"
    )


def test_mise_ci_task_depends_on_lint_verify_sync_and_test() -> None:
    tasks = _load_tasks()
    ci = tasks.get("ci") or {}
    depends = ci.get("depends") if isinstance(ci, dict) else None
    assert isinstance(depends, list), "mise ci task must declare a `depends` list"
    for required in ("lint", "verify-sync", "test"):
        assert required in depends, (
            f"mise ci must depend on '{required}'; depends={depends}"
        )


def test_no_makefile_in_repository() -> None:
    makefile = REPO_ROOT / "Makefile"
    assert not makefile.exists(), (
        "Makefile must not exist; mise.toml is the sole project task registry"
    )


@pytest.mark.parametrize("name", REQUIRED_TASKS)
def test_mise_tasks_ls_lists_required_task(name: str) -> None:
    if shutil.which("mise") is None:
        pytest.skip("mise CLI is not available on PATH")
    cmd = ["mise", "tasks", "ls", "--name-only", "--no-header"]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=30,
    )
    assert result.returncode == 0, (
        f"`mise tasks ls --name-only` failed (exit={result.returncode})\n"
        f"stdout={result.stdout!r}\nstderr={result.stderr!r}"
    )
    listed = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    assert name in listed, (
        f"`mise tasks ls` must list '{name}'; saw {sorted(listed)}"
    )
