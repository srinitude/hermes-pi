# hermes-pi

Standalone source for the Hermes Agent `pi` skill (delegate coding tasks to
[Pi](https://pi.dev), the `@mariozechner/pi-coding-agent` CLI).

This repository is the canonical home of the skill. The copy that Hermes loads
from `~/.hermes/skills/autonomous-ai-agents/pi/` is a **symlink** to a checkout
of this repo at `~/dev/hermes-pi/`. Edit here, commit, push, run `make sync` on
any host, and the in-Hermes path picks up the change without a restart.

## Layout

```
SKILL.md          Hermes skill index (frontmatter + body)
references/       Long-form references the skill links to
tests/            Pytest suite that validates the skill (R01..R17)
assets/           Pi CLI snapshots and transcripts
.github/          GitHub Actions CI
Makefile          Top-level capability targets
install.sh        Symlink installer with backup + idempotent ln -snf
mise.toml         mise tool + task definitions
pyproject.toml    pytest config + dev deps
analysis/         baseline / post-copy manifests + run-log.md
```

## Sync model

* The working tree at `~/dev/hermes-pi/` is the **source of truth**.
* `~/.hermes/skills/autonomous-ai-agents/pi` is a symlink whose `realpath`
  resolves to `~/dev/hermes-pi`.
* `make link` backs up any pre-existing in-Hermes directory under
  `~/.hermes/skills/autonomous-ai-agents/.backup/pi-<ISO8601>/` and replaces it
  with the symlink atomically (`ln -snf`).
* `make sync` is **fast-forward only**:
  `git fetch origin && git switch main && git merge --ff-only origin/main`.
  It refuses to rebase or force-update — diverged state is surfaced to the user.
* `make verify-sync` exits 0 only when (a) the in-Hermes path is a symlink to
  this checkout, (b) the working tree is clean, and (c) `HEAD == origin/main`.

Never edit files at `~/.hermes/skills/autonomous-ai-agents/pi/` directly. All
edits flow through this repo + git.

## Quickstart

```bash
git clone git@github.com:srinitude/hermes-pi.git ~/dev/hermes-pi
cd ~/dev/hermes-pi
mise install
mise run setup
make link            # backs up existing in-Hermes dir, then symlinks
make verify-sync     # asserts symlink + clean tree + HEAD == origin/main
make ci              # lint + tests
```

## Make targets

| Target | Description |
|---|---|
| `make install` | Same as `make link` (symlink installer). |
| `make link` | Backup existing in-Hermes dir, symlink to this checkout. |
| `make unlink` | Remove the in-Hermes symlink (does not delete the backup). |
| `make sync` | Fast-forward this checkout to `origin/main`. |
| `make verify-sync` | Symlink + clean-tree + `HEAD == origin/main` check. |
| `make test` | `mise run test` (pytest). |
| `make lint` | `mise run lint` (Python syntax check). |
| `make ci` | lint + verify-sync + test. |

## Source

* Pi (the upstream CLI): [`pi.dev`](https://pi.dev),
  [`badlogic/pi-mono`](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent).
* Skill version: `SKILL.md` frontmatter `version: 0.1.0`.
