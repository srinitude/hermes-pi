# Repo-sync RED test manifest

The following pytest files implement the RED contract for the
`hermes-pi-skill-repo-sync` goal. Each test corresponds to one or more
acceptance criteria from the goal Markdown.

| RED id | Test file | Contract covered |
|---|---|---|
| R01 | `tests/test_repo_layout.py` | Scaffolding files exist (`Makefile`, `install.sh`, `mise.toml`, `pyproject.toml`, `README.md`, `LICENSE`, `.github/workflows/ci.yml`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `.gitignore`). |
| R02 | `tests/test_skill_content_preserved.py` | Every file under `SKILL.md`, `references/`, `tests/`, `assets/` matches the BOOTSTRAP baseline SHA-256 manifest byte-for-byte. |
| R03 | `tests/test_makefile_targets.py` | `make -n install link unlink sync verify-sync test lint ci` all exit 0. |
| R04 | `tests/test_install_sh_shape.py` | `install.sh` contains the symlink fallback path, the backup branch, and a final `ln -snf` invocation; rejects `cp -r` style installers. |
| R05 | `tests/test_repo_sync_invariants.py` | `~/.hermes/skills/autonomous-ai-agents/pi` is a symlink whose realpath resolves to the working tree; the working tree is on `main` and clean. |
| R06 | `tests/test_remote_published.py` | `gh api repos/srinitude/hermes-pi/branches/main` returns the same SHA as the local `HEAD`. Network-only test; runs in CI only. |
| R07a | `tests/test_ci_workflow.py` | `.github/workflows/ci.yml` is valid YAML, triggers on push and pull request to `main`, and runs the test suite. |
| R07b | `tests/test_no_loader_breakage.py` | Walks the symlinked path and confirms `SKILL.md` frontmatter still parses with `name: pi`. |

The hard gate: no production-code or scaffolding-body edits are permitted
between this commit and the start of GREEN; every RED test must be committed
and observed failing for the documented reason first.
