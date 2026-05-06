# hermes-pi

Standalone source for the Hermes Agent `pi` skill (delegate coding tasks to
[Pi](https://pi.dev), the `@mariozechner/pi-coding-agent` CLI).

This repository is the canonical home of the skill. The copy that Hermes loads
from `~/.hermes/skills/autonomous-ai-agents/pi/` is a **symlink** to a checkout
of this repo at `~/dev/hermes-pi/`. Edit here, commit, push, run
`mise run sync` on any host, and the in-Hermes path picks up the change without
a restart.

> **Make is intentionally unsupported.** This repository has no `Makefile` and
> no `make` targets. Every contributor task lives in `mise.toml` and is invoked
> through `mise run <task>`. There is no Make compatibility shim.

## Layout

```
SKILL.md          Hermes skill index (frontmatter + body)
references/       Long-form references the skill links to
tests/            Pytest suite that validates the skill (R01..R17)
assets/           Pi CLI snapshots and transcripts
.github/          GitHub Actions CI (enters through `mise run ci`)
install.sh        Symlink installer with backup + idempotent ln -snf
mise.toml         mise tool + task definitions (sole task registry)
pyproject.toml    pytest config + dev deps
analysis/         baseline / post-copy manifests + run-log.md
```

## Quickstart

```bash
git clone git@github.com:srinitude/hermes-pi.git ~/dev/hermes-pi
cd ~/dev/hermes-pi
mise install            # install pinned python + uv from mise.toml
mise run setup          # install dev dependencies via uv
mise run link           # backup existing in-Hermes dir, then symlink
mise run verify-sync    # symlink + clean tree + HEAD == origin/main
mise run ci             # lint + verify-sync + test (local CI gate)
```

`mise tasks ls` lists every contributor task with its description.

## mise tasks

| Task | Description |
|---|---|
| `mise run setup` | Install local development dependencies (`uv sync --extra dev`). |
| `mise run install` | Alias for `mise run link` (idempotent symlink installer). |
| `mise run link` | Backup existing in-Hermes dir, symlink to this checkout. |
| `mise run unlink` | Remove the in-Hermes symlink (does not delete the backup). |
| `mise run sync` | Fast-forward this checkout to `origin/main` (`--ff-only`). |
| `mise run verify-sync` | Symlink + clean-tree + `HEAD == origin/main` check. |
| `mise run lint` | Python syntax check (`uv run python -m compileall`). |
| `mise run test` | Run the pytest suite (`uv run pytest`). |
| `mise run ci` | Local CI: lint + verify-sync + test. |

## Sync model

* The working tree at `~/dev/hermes-pi/` is the **source of truth**.
* `~/.hermes/skills/autonomous-ai-agents/pi` is a symlink whose `realpath`
  resolves to `~/dev/hermes-pi`.
* `mise run link` backs up any pre-existing in-Hermes directory under
  `~/.hermes/skills/autonomous-ai-agents/.backup/pi-<ISO8601>/` and replaces it
  with the symlink atomically (`ln -snf`).
* `mise run sync` is **fast-forward only**:
  `git fetch origin && git switch main && git merge --ff-only origin/main`.
  It refuses to rebase or force-update — diverged state is surfaced to the
  user.
* `mise run verify-sync` exits 0 only when (a) the in-Hermes path is a symlink
  to this checkout, (b) the working tree is clean, and (c)
  `HEAD == origin/main`.

Never edit files at `~/.hermes/skills/autonomous-ai-agents/pi/` directly. All
edits flow through this repo + git.

## Local CI

`mise run ci` is the local gate. It depends on `lint`, `verify-sync`, and
`test`, so it mirrors what GitHub Actions runs in `.github/workflows/ci.yml`.
The workflow installs mise via `jdx/mise-action` and then invokes
`mise run ci`, so local and remote validation share a single entrypoint.

## Contributing on `main`

This repository ships from `main`. The contributor flow is:

1. `mise run sync` to fast-forward the local checkout.
2. Edit, then run `mise run ci` locally.
3. `git commit` and `git push origin main` once CI is green.
4. Watch the GitHub Actions run for the pushed SHA finish successfully.

## Source

* Pi (the upstream CLI): [`pi.dev`](https://pi.dev),
  [`badlogic/pi-mono`](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent).
* Skill version: `SKILL.md` frontmatter `version: 0.1.0`.
