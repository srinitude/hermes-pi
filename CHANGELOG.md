# Changelog

## [0.1.0] - 2026-05-06

- Initial extraction of the Hermes `pi` skill from
  `~/.hermes/skills/autonomous-ai-agents/pi/` into a standalone repository.
- Adds companion-repo scaffolding: `Makefile`, `install.sh`, `mise.toml`,
  `pyproject.toml`, `README.md`, `LICENSE`, `.gitignore`, `CHANGELOG.md`,
  `CONTRIBUTING.md`, `SECURITY.md`, `.github/workflows/ci.yml`.
- Adds repo-sync invariant tests under `tests/test_repo_*` /
  `tests/test_no_loader_breakage.py` / `tests/test_remote_published.py` /
  `tests/test_ci_workflow.py` / `tests/test_install_sh_shape.py` /
  `tests/test_makefile_targets.py`.
- `make link` replaces the in-Hermes skill directory with a symlink to this
  checkout, after backing the original up to
  `~/.hermes/skills/autonomous-ai-agents/.backup/pi-<ISO8601>/`.
- `make sync` is fast-forward only.
- Skill content (`SKILL.md`, `references/`, `tests/r01..r17`, `assets/`) is
  copied byte-for-byte from the in-Hermes path; SHA-256 manifest match is
  enforced by `tests/test_skill_content_preserved.py`.
