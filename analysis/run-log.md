# Hermes Pi Skill Repo Sync — Run Log

Source goal contract: `/Users/kiren/dev/throwaway/.worktrees/hermes-2f1719cd/hermes-pi-spec-out/hermes-pi-skill-repo-sync.md`
Source TDD task list:  `/Users/kiren/dev/throwaway/.worktrees/hermes-2f1719cd/hermes-pi-spec-out/hermes-pi-skill-repo-sync-tdd-tasks.yaml`

## ANALYSIS

### A01 — Probe environment readiness

| Command | Exit | Notes |
|---|---|---|
| `git --version` | 0 | git version 2.50.1 (Apple Git-155) |
| `gh --version` | 0 | gh version 2.87.3 |
| `gh auth status` | 0 | Authenticated as `srinitude`, scopes include `repo`, `workflow`, `gist`, `read:org`, `admin:public_key` |
| `mise --version` | 0 | 2026.5.0 macos-arm64 |
| `python3 --version` | 0 | 3.9.6 (system); mise provides 3.11.15 / 3.12.13 |
| `firecrawl --status` | 0 | firecrawl cli v1.16.0 authenticated |
| `opensrc --version` | 0 | 0.7.2 |

### A02 — Baseline SHA-256 manifest of the in-Hermes pi skill

```
find ~/.hermes/skills/autonomous-ai-agents/pi -type f -print0 | sort -z \
  | xargs -0 shasum -a 256 > analysis/baseline-manifest.sha256
```

Captured 29 files. Frontmatter parses as `name: pi`, `version: 0.1.0`.

### A03 — Remote state of `srinitude/hermes-pi`

```
gh repo view srinitude/hermes-pi --json name,visibility,isEmpty,defaultBranchRef,pushedAt
{"defaultBranchRef":{"name":""},"isEmpty":true,"name":"hermes-pi","pushedAt":"2026-05-06T18:09:27Z","visibility":"PUBLIC"}
gh api repos/srinitude/hermes-pi/branches => []
```

Repo is empty; safe to push without rewriting history.

### A04 — Hermes skill loader treats symlinks identically

`agent/skill_utils.iter_skill_index_files` walks the skills tree with
`os.walk(skills_dir, followlinks=True)`. Symlinked skill directories are
followed identically to regular ones; no skill-cache invalidation step is
required after re-symlinking.

### A05 — Companion-repo conventions

Borrowed file shapes from `~/dev/hermes-prompt-enhancer/` (Makefile + install.sh
patterns) and `~/dev/hermes-goal-prompt-generator/` (LICENSE, CHANGELOG.md,
CONTRIBUTING.md, SECURITY.md, mise.toml + uv, pyproject.toml + pytest,
.github/workflows/quality.yml).

## RED phase

### Deliberate-regression demonstrations

The contract requires Makefile and install.sh targets to be present before any
RED test references them (Phase 0 BOOTSTRAP step 7). Some RED tests therefore
pass at the moment they are committed because BOOTSTRAP legitimately created
the test-runner scaffolding. To prove the tests are not vacuous I performed
deliberate-regression demonstrations:

* `tests/test_makefile_targets.py::test_makefile_link_target_invokes_install_sh`
  — Removed the `link:` target from `Makefile`. Re-ran the test:
  `assert 'install.sh' in text` failed for the documented reason. Restored
  `Makefile` from a one-shot backup; test passed.
* `tests/test_install_sh_shape.py::test_install_sh_uses_ln_snf` /
  `::test_install_sh_rejects_cp_r_installer` — Replaced `ln -snf` with
  `cp -r` in `install.sh`. Re-ran the test: both assertions failed for the
  documented reason (forbidden token / missing `ln -snf`). Restored
  `install.sh`; tests passed.
* `tests/test_ci_workflow.py` — same approach.

The regression cycle never mutates committed scaffolding; the temporary
corruption is restored before the next git commit.

### R01 / R02 / R05 / R06 / R07

These RED tests fail naturally at commit time:

* **R01** — `test_repo_layout.py` fails because `SKILL.md`, `references/`, and
  `assets/` are not yet copied from the in-Hermes path.
* **R02** — `test_skill_content_preserved.py` fails on every entry from the
  baseline manifest because skill files are not present at the repo root.
* **R05** — `test_repo_sync_invariants.py` fails because the in-Hermes path is
  still a regular directory, not a symlink to the repo.
* **R06** — `test_remote_published.py` fails because no commit has been pushed
  to `srinitude/hermes-pi:main`.
* **R07** — `test_no_loader_breakage.py` fails because the symlinked SKILL.md
  is not yet at the repo root.
