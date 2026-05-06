# RED test manifest

The pytest files below encode the user-facing contracts that must hold for
`hermes-pi`. Each row maps a RED id to the contract it covers; production code
is only edited after every RED test is committed and observed failing for the
documented reason.

## Mise-only CLI/task centralization (current goal)

| RED id | Test file | Contract covered |
|---|---|---|
| M00 | _this manifest_ | Records the mise-only contract before any production/doc/CI edits. |
| M01 | `tests/test_mise_tasks.py` | `mise.toml` registers every required task (`setup`, `install`, `link`, `unlink`, `sync`, `verify-sync`, `lint`, `test`, `ci`) with descriptions, sync uses `--ff-only`, link delegates to `install.sh`, no `Makefile` is present, and `mise tasks ls` lists each task. |
| M02 | `tests/test_readme_mise_only.py` | README quickstart and task table use `mise install` / `mise run …` only, the sync model documents `mise run sync`/`mise run verify-sync`, and Make is explicitly noted as unsupported with no `make ` examples. |
| M03 | `tests/test_ci_workflow.py` | `.github/workflows/ci.yml` activates mise (e.g. `jdx/mise-action`) before project commands and runs `mise run ci` as the primary project gate. |

`make` is no longer a supported interface for this repository. After GREEN, the
repository must contain no `Makefile`, no Make target tests, and no contributor
docs that instruct users to run `make`.

## Repo-sync invariants (carried forward unchanged)

| RED id | Test file | Contract covered |
|---|---|---|
| R01 | `tests/test_repo_layout.py` | Required scaffolding files exist (`install.sh`, `mise.toml`, `pyproject.toml`, `README.md`, `LICENSE`, `.github/workflows/ci.yml`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `.gitignore`, `scripts/verify-sync.sh`, `SKILL.md`). |
| R02 | `tests/test_skill_content_preserved.py` | Every file under `SKILL.md`, `references/`, `tests/`, `assets/` matches the BOOTSTRAP baseline SHA-256 manifest byte-for-byte. |
| R04 | `tests/test_install_sh_shape.py` | `install.sh` contains the symlink fallback, the backup branch, and a final atomic `ln -snf`; rejects `cp -r` style installers. |
| R05 | `tests/test_repo_sync_invariants.py` | `~/.hermes/skills/autonomous-ai-agents/pi` is a symlink whose realpath resolves to the working tree; the working tree is on `main` and clean. |
| R06 | `tests/test_remote_published.py` | `gh api repos/srinitude/hermes-pi/branches/main` returns the same SHA as the local `HEAD`. Network-only test; runs in CI only. |
| R07a | `tests/test_ci_workflow.py` | `.github/workflows/ci.yml` is valid YAML, triggers on push and pull request to `main`, and runs the test suite (now via `mise run ci`). |
| R07b | `tests/test_no_loader_breakage.py` | The symlinked path resolves to a real `SKILL.md` whose YAML frontmatter parses with `name: pi`. |
