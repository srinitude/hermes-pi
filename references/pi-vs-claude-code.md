# Pi vs Claude Code — Side-By-Side

Every row cites both Pi and Claude Code. Pi citations are
`packages/coding-agent/<path>:<line>` paths under
`~/.opensrc/repos/github.com/badlogic/pi-mono/main/`. Claude Code citations
point at the existing Hermes `claude-code` skill or Anthropic's published
docs.

| Dimension | Pi | Claude Code |
|-----------|----|-------------|
| Non-interactive flag | `pi -p` / `--print` (`packages/coding-agent/src/cli/args.ts:123-129`) | `claude -p` / `--print` (`autonomous-ai-agents/claude-code/SKILL.md` Print-Mode section, lines 38-54) |
| Streaming JSON event source | `pi --mode json` emits `AgentSessionEvent` JSON lines (`packages/coding-agent/docs/json.md:1-82`) | `claude -p --output-format stream-json --verbose --include-partial-messages` (`autonomous-ai-agents/claude-code/SKILL.md`, Streaming-JSON section, ~line 174) |
| Hook / extension model | In-process TypeScript extensions, 29 events, no per-event subprocess (`packages/coding-agent/src/core/extensions/types.ts:1080-1311`) | Process-spawn hooks invoked by name with JSON over stdin/stdout (https://docs.claude.com/en/docs/claude-code/hooks) |
| MCP support | None native — opt-in via package or extension (`packages/coding-agent/README.md:466-484`) | Native (`claude mcp add/list/remove`, see `autonomous-ai-agents/claude-code/SKILL.md` `## CLI Subcommands` ~line 137) |
| Sub-agents | None native — "spawn pi via tmux" (`packages/coding-agent/README.md:472`) | Native — `claude agents` command (`autonomous-ai-agents/claude-code/SKILL.md` ~line 139) |
| Plan mode | None native — write `PLAN.md` or build an extension (`packages/coding-agent/README.md:476`) | `--permission-mode plan` / Plan mode UI (https://docs.claude.com/en/docs/claude-code/plan-mode) |
| Permission popups (anti-pattern in headless Pi: do not bypass via `--dangerously-skip-permissions`-style flags; this is sanctioned only as a Claude-Code reference) | None native — implement with `tool_call` extension event (`packages/coding-agent/src/core/extensions/types.ts:1123`) | Built-in dialogs; bypass with `--dangerously-skip-permissions` (`autonomous-ai-agents/claude-code/SKILL.md` ~line 96) |
| Sessions / branching | JSONL with `id`/`parentId` tree branching, `--session/--fork/--no-session/--session-dir` (`packages/coding-agent/src/cli/args.ts:94-101`, `packages/coding-agent/docs/sessions.md`) | Linear sessions, `claude -c` / `claude -r <id>` (`autonomous-ai-agents/claude-code/SKILL.md` ~line 132) |
| Fast-startup flags | Explicit set: `--no-extensions`, `--no-skills`, `--no-prompt-templates`, `--no-themes`, `--no-context-files`, `--no-tools`, `--offline`, `PI_OFFLINE`, `PI_SKIP_VERSION_CHECK` (`packages/coding-agent/src/cli/args.ts:135-164`, `packages/coding-agent/README.md:622-634`) | `--bare` (a single flag that skips hooks + CLAUDE.md), no fine-grained per-resource toggles (`autonomous-ai-agents/claude-code/SKILL.md` `--bare` recipe; Claude Code v2.x CLI reference) |
| RPC mode | `pi --mode rpc` LF-delimited JSONL over stdin/stdout (`packages/coding-agent/src/modes/rpc/rpc-mode.ts`, `packages/coding-agent/docs/rpc.md:1-120`) | No equivalent. `claude -p --input-format stream-json --output-format stream-json` is closest (`autonomous-ai-agents/claude-code/SKILL.md` Bidirectional-Streaming section ~line 188) |
| Fallback model | `--models <patterns>` with comma-separated globs (`packages/coding-agent/src/cli/args.ts:102-103`) | `--fallback-model` flag (https://docs.claude.com/en/docs/claude-code/cli-reference) |
| Structured output schema | Output is the `AgentSessionEvent` union; no `--json-schema` (`packages/coding-agent/docs/json.md:14-21`) | `claude --json-schema <path>` (`autonomous-ai-agents/claude-code/SKILL.md` Structured-Output section) |
| Built-in tools | `read`, `bash`, `edit`, `write`, `grep`, `find`, `ls` (`packages/coding-agent/README.md:466-484`, `pi --help`) | `Read`, `Edit`, `Write`, `Bash`, `Grep`, `Glob`, `WebFetch`, ... (`autonomous-ai-agents/claude-code/SKILL.md` Tools allowlist section) |
| Worktree | No native flag; Hermes wraps with `git worktree add` + `terminal(workdir=...)` (`packages/coding-agent/src/cli/args.ts:70-189` parser; `packages/coding-agent/src/core/footer-data-provider.ts:12-15` cwd detection) | Native `--worktree <name>` flag (https://docs.claude.com/en/docs/claude-code/cli-reference) |

## Reading the table

Where Claude Code has a built-in feature, Pi typically has a primitive
(extension event + a small TypeScript file) that lets the user *build* the
feature. The Pi philosophy quote that motivates this design choice lives in
[`pi-philosophy.md`](pi-philosophy.md).

The two rows that matter most for Hermes orchestration are:

1. **Hook/extension model.** Pi extensions load once and live for the entire
   session — Hermes can register an extension that subscribes to `tool_call`
   and `tool_result` to enforce permission policy with zero per-event
   subprocess cost. Claude Code hooks spawn a process per event, which is
   noticeable on bash-heavy turns.
2. **RPC mode.** Pi's `--mode rpc` is a first-class long-lived agent driver;
   Hermes drives it via `process(action='start' | 'write' | 'poll' | 'kill')`
   with LF-delimited JSONL framing. Claude Code's bidirectional stream-json
   is similar but session-scoped to a single `claude -p` invocation.
