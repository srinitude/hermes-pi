---
name: pi
description: >
  Delegate coding tasks to Pi (the @mariozechner/pi-coding-agent CLI from
  pi.dev) in non-interactive only mode. Use when the user asks to use Pi,
  pi.dev, the pi coding agent, or wants Hermes to drive Pi headlessly via
  -p / --mode json / --mode rpc, with fast streaming through jq, RPC
  framing over stdin/stdout, or extensions/skills/prompts/themes/pi
  packages. Use when comparing Pi to Claude Code, Codex, OpenCode, or
  Amp. Do NOT use for general coding without Pi context, for raspberry pi
  / mathematical pi questions, or when the user explicitly wants Claude
  Code, Codex, or another coding agent.
version: 0.1.0
license: MIT
author: Hermes Agent
metadata:
  hermes:
    tags: [Coding-Agent, Pi, Non-Interactive, JSON-Stream, RPC, Hermes-Integration, Streaming, Extensions]
    related_skills: [claude-code, codex, opencode, hermes-agent]
---

# Pi — Hermes Orchestration Guide

Delegate coding tasks to [Pi](https://pi.dev) (the `@mariozechner/pi-coding-agent`
CLI) via Hermes' `terminal()` and `process()` boundaries. Pi runs **non-interactive
only** in this skill; interactive TUI flows are explicit anti-patterns.
Source-of-truth: `~/.opensrc/repos/github.com/badlogic/pi-mono/main/`, pinned to
`@mariozechner/pi-coding-agent@0.73.0`.

## Prerequisites

- **Node** ≥ 20.6.0 (`packages/coding-agent/package.json` `engines.node`).
- **Install:** `npm install -g @mariozechner/pi-coding-agent`.
- **Verify:** `terminal(command="pi --version")` → must print `0.73.0`.
  `terminal(command="pi --help")` → must contain `--mode <mode>` literal.
- **Auth (headless):** export one of `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`,
  `GEMINI_API_KEY`, `GROQ_API_KEY`, `OPENROUTER_API_KEY`, etc. Pi's full env-var
  list is in `pi --help` and `packages/coding-agent/README.md:622-634`. Avoid
  `pi /login` in headless flows — it opens an interactive OAuth dialog.
- **Source mirror:** `opensrc path badlogic/pi-mono` returns the cache used by
  every citation in this skill.

## Pi Philosophy

Pi is "aggressively extensible so it doesn't have to dictate your workflow"
(`packages/coding-agent/README.md:466-484`). The philosophy thesis is:

> "strip away everything and build a minimal extensible core"

> "What's not in there? No MCP, no sub agents, no plan load, no background bash, no built-in to-do's"

(Both quotes from Mario Zechner's talk, https://www.youtube.com/watch?v=Dli5slNaJu0,
captured to `assets/pi-philosophy-transcript.txt`. Full quote table:
`references/pi-philosophy.md`.)

The README list `packages/coding-agent/README.md:466-484` is reproduced
verbatim: **No MCP**, **No sub-agents**, **No permission popups**, **No plan
mode**, **No built-in to-dos**, **No background bash**. Every one of these is
solved by Pi's extension layer instead of by core features. Hermes recipes
must respect this — when Pi lacks a feature, Hermes either skips it or
implements it at the Hermes layer.

Pi's hook system *is* its extension system: in-process TypeScript files that
subscribe to events, no per-event subprocess spawn (the talk explicitly calls
this out as "very expensive if you have to start up that process over and
over again"). See `references/pi-philosophy.md` and
`references/pi-extension-events.md`.

## Pi Primitives

| Primitive | Path / flag | Source |
|-----------|------------|--------|
| extensions | `~/.pi/agent/extensions/` (global) and `.pi/extensions/` (project) | `packages/coding-agent/src/migrations.ts:217-228` (rename from `hooks/`) |
| skills | `~/.pi/agent/skills/` and `.pi/skills/`, `--skill <path>` | `packages/coding-agent/docs/skills.md` |
| prompts | prompt templates: `~/.pi/agent/prompts/`, `--prompt-template <path>` | `packages/coding-agent/docs/prompt-templates.md` |
| themes | `~/.pi/agent/themes/`, `--theme <path>` | `packages/coding-agent/docs/themes.md` |
| pi packages | `pi install npm:|git:|https:|ssh:` | `packages/coding-agent/README.md:380-405` |
| AGENTS.md | auto-loaded context file | `packages/coding-agent/src/cli/args.ts:152-153` (`--no-context-files`) |
| SYSTEM.md | `.pi/SYSTEM.md` / `APPEND_SYSTEM.md` overrides system prompt | `packages/coding-agent/README.md` Customization section |
| sessions | JSONL files with `id`/`parentId` tree branching | `packages/coding-agent/docs/session-format.md` |
| built-in tools | `read`, `bash`, `edit`, `write`, `grep`, `find`, `ls` | `pi --help` "Built-in Tool Names" |
| tool allowlist | `--tools`, `--no-tools`, `--no-builtin-tools` | `packages/coding-agent/src/cli/args.ts:104-112` |
| ExtensionAPI | `registerTool`, `registerCommand`, `registerShortcut`, `registerFlag`, `registerProvider`, `registerMessageRenderer`, `sendMessage`, `sendUserMessage`, `appendEntry`, `setSessionName`, `setLabel`, `exec`, `getActiveTools`, `getAllTools`, `setActiveTools`, `getCommands`, `setModel`, `getThinkingLevel`, `setThinkingLevel`, `events` | `packages/coding-agent/src/core/extensions/types.ts:1080-1311` |

## Pi Extension Events (Hooks)

Pi calls them *extension events*; the user/talk says *hooks*. Pi explicitly
renamed `hooks/` → `extensions/` (`packages/coding-agent/src/migrations.ts:217-228`).
All 29 events are declared in
`packages/coding-agent/src/core/extensions/types.ts:1089-1126` and documented
with semantics in `packages/coding-agent/docs/extensions.md:266-450`. The full
table is in `references/pi-extension-events.md`. The verbatim ASCII lifecycle
diagram is `assets/pi-event-lifecycle.txt`.

## Non-Interactive Mode (Mandatory)

This skill is **non-interactive only**. Every recipe uses one of:

- `pi -p` / `--print` (`packages/coding-agent/src/cli/args.ts:123-129`) — text result.
- `pi --mode json` (`packages/coding-agent/src/cli/args.ts:74-78`) — JSON event stream.
- `pi --mode rpc` (`packages/coding-agent/docs/rpc.md`) — long-lived JSONL agent driver.

The contract on stdin/`@file`/CLI-message merging in non-interactive mode is
`packages/coding-agent/src/cli/initial-message.ts:16-19`.

**Forbidden patterns** (sentinel'd by `tests/test_r14_forbidden_tokens.py`):

- Driving the coding agent via terminal-multiplexer send-keys (anti-pattern).
- Setting `pty=true` on a `terminal()` call (anti-pattern; do not use).
- `--resume` without an explicit session id (interactive picker).
- `--continue` without `-p` (drops Hermes into the TUI).

## Fast Streaming Recipes

Pi has no `--bare` flag (Claude Code's term). Pi's equivalent is the explicit
`--no-*` set + `--offline` + `PI_SKIP_VERSION_CHECK=1`. Canonical fast
command:

```bash
PI_OFFLINE=1 PI_SKIP_VERSION_CHECK=1 pi \
  --mode json --offline \
  --no-context-files --no-skills --no-prompt-templates --no-themes --no-extensions \
  --no-session --thinking off --tools read,grep,find,ls \
  "What does src/index.ts export?" \
  | jq -rj 'select(.type=="message_update") | .assistantMessageEvent.delta // empty'
```

`message_update` is the token-level streaming event; `jq -rj` flushes per
record so Hermes sees the first token as soon as the provider streams it. Full
recipe set: `references/pi-fast-streaming-recipes.md`.

## Hermes Integration Patterns

Short prompt, foreground:

```
terminal(command="pi -p --offline --no-extensions --no-skills --no-context-files 'List exports in src/index.ts'", workdir="/repo", timeout=60)
```

Long task, background + notify:

```
terminal(command="pi --mode json --offline --no-extensions --no-skills --no-context-files 'Refactor src/api/' | tee /tmp/pi.jsonl | jq -rj 'select(.type==\"message_update\") | .assistantMessageEvent.delta // empty'", workdir="/repo", timeout=1800, background=True, notify_on_complete=True)
```

Long-lived RPC session:

```
process(action="start", command="pi --mode rpc --offline --no-extensions --no-skills --no-context-files", workdir="/repo")
process(action="write", session_id="<id>", data='{"id":"r1","type":"prompt","message":"Begin refactor"}\n')
process(action="poll", session_id="<id>")
process(action="kill", session_id="<id>")
```

Skill discovery / view:

```
mcp_skill_view(name="pi")
mcp_skills_list(category="autonomous-ai-agents")
```

## Worktree Isolation (Mandatory)

Pi has **no native `--worktree` flag** (literal: no native --worktree branch
in the parser) — verified by reading the entire flag parser at
`packages/coding-agent/src/cli/args.ts:70-189`. There is no `--worktree`
parser branch, no `result.worktree` field. Worktree creation is therefore a
Hermes-side responsibility.

Pi *can* run inside a worktree because its git detection handles `.git` as a
file (worktree pointer):
`packages/coding-agent/src/core/footer-data-provider.ts:12-15`. Combine the
two facts as the wrapper pattern:

```
terminal(command="git worktree add /tmp/pi-work-X feature/X", workdir="/repo", timeout=30)
terminal(command="pi -p --mode json --offline --no-extensions --no-skills --no-context-files 'Implement feature X'", workdir="/tmp/pi-work-X", timeout=600)
terminal(command="git -C /tmp/pi-work-X diff --stat", workdir="/repo", timeout=30)
terminal(command="git worktree remove /tmp/pi-work-X --force", workdir="/repo", timeout=30)
```

Every Pi recipe that may mutate a repository follows this isolation flow. Full
guide: `references/pi-worktree-isolation.md`.

## CLI Reference

Captured verbatim in `assets/pi-cli-help-snapshot.txt` (run-time `pi --help`
snapshot). Source of the help printer: `packages/coding-agent/src/cli/args.ts:191-353`.
The flag parser is `packages/coding-agent/src/cli/args.ts:70-189`.

Most-used flags for headless Hermes orchestration:

| Flag | Purpose | Source line |
|------|---------|-------------|
| `-p`, `--print` (i.e. `-p/--print`) | Non-interactive print mode | `args.ts:123-129` |
| `--mode <text\|json\|rpc>` (i.e. `--mode text`, `--mode json`, `--mode rpc`) | Output mode | `args.ts:74-78` |
| `--no-context-files`, `-nc` | Skip AGENTS.md / CLAUDE.md | `args.ts:152-153` |
| `--no-skills`, `-ns` | Skip skill discovery | `args.ts:146-147` |
| `--no-prompt-templates`, `-np` | Skip prompt templates | `args.ts:148-149` |
| `--no-themes` | Skip theme load | `args.ts:150-151` |
| `--no-extensions`, `-ne` | Skip extension discovery | `args.ts:135-136` |
| `--no-tools`, `-nt` | Disable all tools | `args.ts:104-105` |
| `--no-builtin-tools`, `-nbt` | Keep extension tools, drop built-ins | `args.ts:106-107` |
| `--tools`, `-t <list>` | Allowlist tool names | `args.ts:108-112` |
| `--offline` | Skip startup network ops | `args.ts:163-164` |
| `--session <path\|id>` | Resume specific session | `args.ts:96-97` |
| `--fork <path\|id>` | Fork into a new session | `args.ts:98-99` |
| `--no-session` | Ephemeral run | `args.ts:94-95` |
| `--session-dir <dir>` | Session storage dir | `args.ts:100-101` |
| `--thinking <level>` | off, minimal, low, medium, high, xhigh | `args.ts:113-122` |
| `--extension`, `-e <path>` | Load an extension explicitly | `args.ts:132-134` |

## Settings & Configuration

- Global config: `~/.pi/agent/settings.json`. Override dir with
  `PI_CODING_AGENT_DIR` (`packages/coding-agent/README.md:626`).
- Project config: `.pi/settings.json`. Auto-discovered from `cwd`.
- System prompt overrides: `.pi/SYSTEM.md` (replace) or
  `.pi/APPEND_SYSTEM.md` (append).
- Context files (auto-loaded unless `--no-context-files`): `AGENTS.md`,
  `CLAUDE.md`.
- Package directory override: `PI_PACKAGE_DIR`
  (`packages/coding-agent/README.md:628`).

## Sessions

Pi sessions are JSONL files with `id`/`parentId` tree branching. Recipes,
non-interactive only:

```
# Resume by explicit id (never the interactive picker):
terminal(command="pi -p --session 0d7e0b56 'Continue work'", workdir="/repo", timeout=300)

# Fork from a session into a new branch:
terminal(command="pi -p --fork 0d7e0b56 --no-session 'Try alternative approach'", workdir="/repo", timeout=300)

# Ephemeral, no JSONL written:
terminal(command="pi -p --no-session --offline 'One-shot question'", workdir="/repo", timeout=60)

# Custom session dir:
terminal(command="pi -p --session-dir /tmp/pi-sessions --no-session 'Test run'", workdir="/repo", timeout=60)
```

Cite: `packages/coding-agent/src/cli/args.ts:94-101`. Session format:
`packages/coding-agent/docs/session-format.md`.

## Skills, Prompt Templates, Themes, Pi Packages

Pi installs packages from four schemes (`packages/coding-agent/README.md:380-405`):

```
pi install npm:@foo/pi-tools
pi install git:github.com/user/repo
pi install https://github.com/user/repo@v1
pi install ssh://git@github.com/user/repo
```

`-l` makes the install project-local (under `.pi/`) instead of global
(`~/.pi/agent/`). Each package contributes any subset of `extensions/`,
`skills/`, `prompts/`, `themes/` (manifest in its `package.json` `pi` key).
`pi list`, `pi update`, `pi remove`, and `pi config` round out the lifecycle.
`pi config` is a TUI and therefore not used inside Hermes orchestration.

## Extensions Authoring (Headless-Friendly Patterns)

Minimal `tool_call`-blocking extension:

```typescript
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI): void {
  pi.on("tool_call", async (event) => {
    const cmd = String(event.args?.command ?? "");
    if (/\brm\s+-rf\s+\//.test(cmd)) {
      pi.appendEntry("hermes-policy", { blocked: cmd });
      return { block: true, blockReason: "rm -rf / blocked by Hermes policy" };
    }
    return undefined;
  });
}
```

Run with `pi -e ./policy.ts --mode rpc --no-extensions ...` so only this
extension is loaded. Extensions must use top-level imports (no inline
`await import(...)`) and avoid `any` (per pi-mono repo conventions in the
top-level `AGENTS.md`; line ceiling is 200 LOC per file).

## RPC Mode

`pi --mode rpc` accepts JSON commands on stdin and emits JSON events on
stdout, framed strictly LF-only.

> "RPC mode uses strict JSONL semantics with LF (`\n`) as the only record
> delimiter. ... In particular, Node `readline` is not protocol-compliant
> for RPC mode because it also splits on U+2028 and U+2029, which are valid
> inside JSON strings."
>
> — `packages/coding-agent/docs/rpc.md:29-36`,
> `packages/coding-agent/src/modes/rpc/jsonl.ts:14-19`.

**Do not use Node readline** for RPC clients. The reference implementation
in `packages/coding-agent/src/modes/rpc/jsonl.ts:14-19` is the LF-only
contract. Implement an LF-only line splitter or use the framing helper
`attachJsonlLineReader` shipped in that file.

The event stream is the same `AgentSessionEvent` union (verbatim from
`packages/coding-agent/docs/json.md:14-21`):

```typescript
type AgentSessionEvent =
  | AgentEvent
  | { type: "queue_update"; steering: readonly string[]; followUp: readonly string[] }
  | { type: "compaction_start"; reason: "manual" | "threshold" | "overflow" }
  | { type: "compaction_end"; reason: "manual" | "threshold" | "overflow"; result: CompactionResult | undefined; aborted: boolean; willRetry: boolean; errorMessage?: string }
  | { type: "auto_retry_start"; attempt: number; maxAttempts: number; delayMs: number; errorMessage: string }
  | { type: "auto_retry_end"; success: boolean; attempt: number; finalError?: string };
```

Base events (`packages/coding-agent/docs/json.md:28-43`):

```typescript
type AgentEvent =
  // Agent lifecycle
  | { type: "agent_start" }
  | { type: "agent_end"; messages: AgentMessage[] }
  // Turn lifecycle
  | { type: "turn_start" }
  | { type: "turn_end"; message: AgentMessage; toolResults: ToolResultMessage[] }
  // Message lifecycle
  | { type: "message_start"; message: AgentMessage }
  | { type: "message_update"; message: AgentMessage; assistantMessageEvent: AssistantMessageEvent }
  | { type: "message_end"; message: AgentMessage }
  // Tool execution
  | { type: "tool_execution_start"; toolCallId: string; toolName: string; args: any }
  | { type: "tool_execution_update"; toolCallId: string; toolName: string; args: any; partialResult: any }
  | { type: "tool_execution_end"; toolCallId: string; toolName: string; result: any; isError: boolean };
```

RPC commands (`packages/coding-agent/docs/rpc.md:38-120`): `prompt`,
`steer`, `follow_up`, `abort`, `set_steering_mode`, `set_follow_up_mode`. With
`streamingBehavior: "steer" | "followUp"` for queueing during streaming.

## SDK Mode

For Node.js consumers, prefer the SDK over RPC. From
`packages/coding-agent/README.md:434-450`:

```typescript
import { AuthStorage, createAgentSession, ModelRegistry, SessionManager } from "@mariozechner/pi-coding-agent";

const authStorage = AuthStorage.create();
const modelRegistry = ModelRegistry.create(authStorage);
const { session } = await createAgentSession({
  sessionManager: SessionManager.inMemory(),
  authStorage,
  modelRegistry,
});

await session.prompt("What files are in the current directory?");
```

For multi-session runtimes, use `createAgentSessionRuntime()` and
`AgentSessionRuntime`.

## MCP Bridging (Opt-In, Anti-Pattern by Default)

Pi has no native MCP. The README states **No MCP. Build CLI tools with READMEs
(see Skills), or build an extension that adds MCP support**
(`packages/coding-agent/README.md:470`). MCP is therefore **opt-in** in this
skill, treated as **anti-pattern by default**, and never assumed.

Two opt-in routes if Hermes really must bridge MCP:

1. Install a community pi-package that bridges MCP — e.g. search npm/Discord
   for `pi-package` keyword.
2. Author an extension that imports `@modelcontextprotocol/sdk` and wires
   discovered tools into `pi.registerTool(...)`
   (`packages/coding-agent/src/core/extensions/types.ts:1131-1135`).

Use either only when the workflow truly needs an MCP server. Default Hermes
recipes never enable MCP for Pi.

## Environment Variables

From `packages/coding-agent/README.md:622-634`:

| Variable | Purpose |
|----------|---------|
| `PI_CODING_AGENT_DIR` | Override config dir (default `~/.pi/agent`). |
| `PI_CODING_AGENT_SESSION_DIR` | Override session storage dir (overridden by `--session-dir`). |
| `PI_PACKAGE_DIR` | Override package dir (Nix/Guix friendly). |
| `PI_OFFLINE` | Disable startup network ops (update check + telemetry). |
| `PI_SKIP_VERSION_CHECK` | Skip the version update check only. |
| `PI_TELEMETRY` | Override install/update telemetry. |
| `PI_CACHE_RETENTION` | `long` enables 1h Anthropic / 24h OpenAI prompt cache. |
| `VISUAL`, `EDITOR` | External editor for Ctrl+G in the TUI (irrelevant headless). |

## Cost & Performance Tips

- Set `--offline` (or `PI_OFFLINE=1`) on every headless run for deterministic
  startup (`packages/coding-agent/src/cli/args.ts:163-164`).
- Pin `--thinking off` for cheap throughput, `--thinking high` for hard tasks
  (`packages/coding-agent/src/cli/args.ts:113-122`).
- `PI_CACHE_RETENTION=long` for prompt caching across runs
  (`packages/coding-agent/README.md:632`).
- `--no-session` for ephemeral runs to skip JSONL writes
  (`packages/coding-agent/src/cli/args.ts:94-95`).
- `--tools read,grep,find,ls` for read-only review (no write/edit/bash)
  (`packages/coding-agent/src/cli/args.ts:108-112`).
- Use `--mode json | jq` for incremental output. Avoid buffering wrappers.

## Pitfalls & Gotchas

- `bin.pi` resolves only after npm-global install; a stale `~/.npm` cache
  can leave a half-broken binary. If `pi` errors with `ERR_MODULE_NOT_FOUND`,
  reinstall: `npm install -g @mariozechner/pi-coding-agent`.
- `--mode rpc` requires LF-only framing; do not use Node `readline`
  (`packages/coding-agent/src/modes/rpc/jsonl.ts:14-19`).
- Pi has no `--bare` flag; the equivalent is the explicit `--no-*` set
  (`packages/coding-agent/src/cli/args.ts:135-153`).
- Pi treats a `hooks/` directory as deprecated and prints a warning
  (`packages/coding-agent/src/migrations.ts:217-228`). Use `extensions/`.
- `pi --resume` opens an interactive picker; pass `--session <id>` instead
  (`packages/coding-agent/src/cli/args.ts:81-82`, `96-97`).
- `pi /login` is interactive; for headless flows, set provider env vars and
  pass `--api-key` only when intentionally overriding.
- macOS may not have GNU `timeout`; prefer Hermes `terminal(timeout=N)` for
  smoke tests and long-running Pi calls instead of shelling out to `timeout`.
- The `pi config` subcommand is a TUI — not for Hermes recipes.

## Rules for Hermes Agents

1. Always pass `--offline` on headless runs.
2. Always wrap pi in `terminal(timeout=N)` (or `process(action='kill')` on
   cancel). Never rely on Pi's internal timeouts.
3. Never expect interactive prompts. Skip `--continue`/`--resume` without
   explicit session ids.
4. Always parse `--mode json` output with `jq` or a real JSON parser, never
   regex.
5. Never use Node `readline` for `--mode rpc` framing. Implement LF-only
   line splitting.
6. Restrict `--tools` to a least-privilege allowlist for review tasks.
7. Use `--no-session` for ephemeral runs; otherwise log the
   `{"type":"session",...}` first JSON line for audit.
8. Resume sessions only by `--session <id>`, never the interactive picker.
9. Mutating recipes always run inside a Hermes-created git worktree
   (see `## Worktree Isolation (Mandatory)`).
10. Treat MCP as opt-in / anti-pattern by default. Never auto-enable MCP for Pi.

## Pi vs Claude Code (Side-By-Side)

Full matrix in `references/pi-vs-claude-code.md`. Highlights:

- **Pi:** non-interactive `-p` / `--mode json` / `--mode rpc`; in-process TS
  extensions; no MCP; sessions are tree-shaped JSONL; no `--worktree` flag
  (Hermes wraps).
- **Claude Code:** non-interactive `-p`; process-spawn hooks; native MCP;
  linear sessions; native `--worktree`. See
  `~/.hermes/skills/autonomous-ai-agents/claude-code/SKILL.md`.

## Resources

- Pi docs: https://pi.dev/docs/latest
- Quickstart: https://pi.dev/docs/latest/quickstart
- JSON event stream: https://pi.dev/docs/latest/json
- RPC mode: https://pi.dev/docs/latest/rpc
- Skills: https://pi.dev/docs/latest/skills
- Source: https://github.com/badlogic/pi-mono
- Philosophy talk: https://www.youtube.com/watch?v=Dli5slNaJu0
