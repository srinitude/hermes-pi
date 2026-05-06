# Pi Non-Interactive Cookbook (Hermes recipes only)

Every recipe below uses Hermes' `terminal()` boundary and one of pi's three
non-interactive modes: `pi -p` (text), `pi --mode json` (event stream), or
`pi --mode rpc` (long-lived JSONL session). Interactive TUI flows are explicit
anti-patterns and are not documented here.

## Recipe 1 — fast one-shot text response

```python
terminal(
    command="PI_OFFLINE=1 PI_SKIP_VERSION_CHECK=1 pi -p --offline --no-extensions --no-skills --no-prompt-templates --no-themes --no-context-files --thinking off 'List the files in src/'",
    workdir="/Users/kiren/repos/myapp",
    timeout=60,
)
```

Cite: `packages/coding-agent/src/cli/args.ts:123-129` (`-p`/`--print`),
`packages/coding-agent/src/cli/args.ts:163-164` (`--offline`).

## Recipe 2 — JSON event stream filtered by jq

```bash
PI_OFFLINE=1 PI_SKIP_VERSION_CHECK=1 \
  pi --mode json --offline --no-extensions --no-skills \
     --no-prompt-templates --no-themes --no-context-files \
     'Summarize README.md' \
  | jq -rj 'select(.type=="message_update") | .assistantMessageEvent.delta // empty'
```

Hermes form:

```python
terminal(
    command="""bash -c 'PI_OFFLINE=1 PI_SKIP_VERSION_CHECK=1 pi --mode json --offline --no-extensions --no-skills --no-prompt-templates --no-themes --no-context-files "Summarize README.md" | jq -rj "select(.type==\\"message_update\\") | .assistantMessageEvent.delta // empty"'""",
    workdir="/Users/kiren/repos/myapp",
    timeout=120,
)
```

Cite: `packages/coding-agent/docs/json.md:1-82`.

## Recipe 3 — read-only review (no edits possible)

```python
terminal(
    command="pi -p --tools read,grep,find,ls --no-skills --no-extensions --no-context-files 'Review src/api/ for SQL injection risk'",
    workdir="/Users/kiren/repos/myapp",
    timeout=300,
)
```

Cite: `packages/coding-agent/src/cli/args.ts:108-112` (`--tools` allowlist).

## Recipe 4 — ephemeral session, no JSONL written

```python
terminal(
    command="pi -p --no-session --offline --no-extensions --no-skills --no-context-files 'What is the diff between HEAD and origin/main?'",
    workdir="/Users/kiren/repos/myapp",
    timeout=60,
)
```

Cite: `packages/coding-agent/src/cli/args.ts:94-95` (`--no-session`).

## Recipe 5 — resume by explicit session id (never interactive picker)

```python
terminal(
    command="pi -p --session 0d7e0b56 'Continue: now run the tests.'",
    workdir="/Users/kiren/repos/myapp",
    timeout=300,
)
```

Cite: `packages/coding-agent/src/cli/args.ts:96-97` (`--session <path|id>`).
The bare `--resume`/`-r` flag opens an interactive picker and is forbidden.

## Recipe 6 — fork an existing session into a new branch

```python
terminal(
    command="pi -p --fork 0d7e0b56 --no-session 'Fork from here, try a different approach'",
    workdir="/Users/kiren/repos/myapp",
    timeout=300,
)
```

Cite: `packages/coding-agent/src/cli/args.ts:98-99` (`--fork`).

## Recipe 7 — pipe stdin into the prompt

```python
terminal(
    command="bash -c 'cat docs/spec.md | pi -p --offline --no-extensions --no-skills --no-context-files \"Summarize this spec\"'",
    workdir="/Users/kiren/repos/myapp",
    timeout=120,
)
```

Cite: `packages/coding-agent/src/cli/initial-message.ts:16-19` (stdin / @file
/ CLI message merge contract).

## Recipe 8 — long-running RPC session driven via Hermes process()

```python
session = process(
    action="start",
    command="pi --mode rpc --offline --no-extensions --no-skills --no-context-files",
    workdir="/Users/kiren/repos/myapp",
)
process(action="write", session_id=session.id, data='{"id":"r1","type":"prompt","message":"Begin refactor"}\n')
# Drain events:
for chunk in process(action="poll", session_id=session.id):
    ...
process(action="write", session_id=session.id, data='{"id":"r2","type":"steer","message":"actually start with src/api/"}\n')
process(action="write", session_id=session.id, data='{"id":"r3","type":"abort"}\n')
process(action="kill", session_id=session.id)
```

Cite: `packages/coding-agent/docs/rpc.md:1-120`,
`packages/coding-agent/src/modes/rpc/jsonl.ts:14-19` (LF-only framing).

## Forbidden anti-patterns

The following recipes are **NOT** allowed in Hermes Pi orchestration. Each is
explicitly an anti-pattern for headless Pi:

- Wrapping pi in a terminal-multiplexer send-keys flow to drive its TUI.
- Setting a PTY on a Pi `terminal()` call (do not use `pty=true` here).
- Using bare `--resume` (no id) — opens an interactive session picker.
- Using bare `--continue` without `-p` — drops Hermes into the TUI.
- Using a TTY-emulator script to send keystrokes to pi.

If a workflow seems to need any of the above, route through `pi --mode rpc`
and `process(action='write', session_id=..., data=...)` instead.
