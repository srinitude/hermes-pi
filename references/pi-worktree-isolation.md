# Pi Worktree Isolation (Mandatory for mutating recipes)

Pi has **no native `--worktree` flag** — verified by reading the entire flag
parser at `packages/coding-agent/src/cli/args.ts:70-189`. There is no
`--worktree` parser branch, no `result.worktree` field, no `WORKTREE` config
key. Worktree creation is therefore a Hermes-side responsibility, not a Pi
CLI feature.

What Pi *does* support is running inside an existing worktree. Pi's git
detection walks up from `cwd` and handles the worktree case where `.git` is a
file (not a directory) — see
`packages/coding-agent/src/core/footer-data-provider.ts:12-15`:

> Find git metadata paths by walking up from cwd. Handles both regular git
> repos (.git is a directory) and worktrees (.git is a file).

Pi then resolves the real git common dir from the `gitdir:` redirection inside
the `.git` file, so `git status`, footer/branch display, and Pi's bash tool all
work correctly inside a worktree. This is exactly the contract Hermes needs.

## Mandatory Hermes wrapper pattern

For **any** Pi recipe that may mutate files, Hermes MUST:

1. Create or select a dedicated git worktree.
2. Invoke Pi with `terminal(..., workdir=<worktree>)`.
3. Inspect the diff in the worktree (still under Hermes control).
4. Merge / cherry-pick / discard explicitly.
5. Remove the worktree.

### Step 1 — create the worktree

```python
terminal(
    command="git worktree add /tmp/pi-work-add-feature feature/add-feature",
    workdir="/Users/kiren/repos/myapp",
    timeout=30,
)
```

If the branch does not exist yet, use `git worktree add -b feature/add-feature /tmp/pi-work-add-feature`.

### Step 2 — drive Pi inside the worktree

```python
terminal(
    command=(
        "PI_OFFLINE=1 PI_SKIP_VERSION_CHECK=1 "
        "pi -p --mode json --offline --no-extensions --no-skills "
        "--no-prompt-templates --no-themes --no-context-files "
        "'Add error handling to src/api/users.ts'"
    ),
    workdir="/tmp/pi-work-add-feature",
    timeout=600,
)
```

The `workdir=` argument is the Hermes-side enforcement of the worktree boundary.
Pi will cd into the worktree, detect the `.git` file (footer-data-provider lines
12-15), and only modify files inside the worktree.

### Step 3 — inspect the diff (Hermes side, not Pi)

```python
terminal(
    command="git -C /tmp/pi-work-add-feature diff --stat",
    workdir="/Users/kiren/repos/myapp",
    timeout=30,
)
```

### Step 4 — accept or reject

Accept (merge into main worktree):

```python
terminal(
    command="git merge --no-ff feature/add-feature",
    workdir="/Users/kiren/repos/myapp",
    timeout=60,
)
```

Reject (discard the branch entirely):

```python
terminal(
    command="git branch -D feature/add-feature",
    workdir="/Users/kiren/repos/myapp",
    timeout=15,
)
```

### Step 5 — clean up the worktree

Always run `git worktree remove`. The contract requires this even on failure
paths so the local checkout never ends up cluttered with stale worktrees:

```python
terminal(
    command="git worktree remove /tmp/pi-work-add-feature --force",
    workdir="/Users/kiren/repos/myapp",
    timeout=30,
)
```

## Why this matters

Without Hermes-side worktree isolation, every Pi run would mutate the same
checkout the rest of Hermes is operating on. Concurrent Pi runs would race;
a failed Pi run would leave half-applied edits in the live tree; rollback
would mean `git restore` instead of `git worktree remove`. The wrapper
pattern above turns every Pi mutation into an isolated, atomic, revertable
unit.

## Citations

- `packages/coding-agent/src/cli/args.ts:70-189` — full Pi flag parser; no
  `--worktree` branch present.
- `packages/coding-agent/src/core/footer-data-provider.ts:12-15` — Pi's git
  detection handles `.git` as a worktree file; this is what makes Hermes-
  managed worktree isolation work.
