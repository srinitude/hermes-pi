# Pi Extension Events (Hooks) — Reference

Pi calls these *extension events*. The user/talk colloquially calls them *hooks*; Pi
renamed `hooks/` to `extensions/` and prints a deprecation warning if it sees the
old directory (`packages/coding-agent/src/migrations.ts:217-228`). All 29 events
are declared in `packages/coding-agent/src/core/extensions/types.ts:1089-1126`
and documented in `packages/coding-agent/docs/extensions.md:266-450`. The
verbatim ASCII lifecycle diagram is captured in
[`assets/pi-event-lifecycle.txt`](../assets/pi-event-lifecycle.txt).

## Handler signature

```typescript
pi.on(eventName, async (event, ctx) => {
  // event: typed payload (see below)
  // ctx:   { sessionManager, ui, ... } — runtime context bound by extension runner
  return optionalReturnShape; // some events accept block / cancel / replacements
});
```

Source: `packages/coding-agent/src/core/extensions/types.ts:1080-1311` (the
`ExtensionAPI` interface and event subscription overloads). Event handlers run
in-process inside the pi runtime — no per-event subprocess spawn (compare
Claude Code hooks, which spawn a process on every hook).

## All 29 events (lifecycle order)

| # | Event | Return shape | Can block / cancel? | Notes |
|---|-------|--------------|--------------------|-------|
| 1 | `resources_discover` | `ResourcesDiscoverResult { skillPaths?, promptPaths?, themePaths? }` | No | Extra skill / prompt / theme paths. Fired on startup and reload. |
| 2 | `session_start` | void | No | `{ reason: "startup" \| "new" \| "resume" \| "fork" \| "reload" }` |
| 3 | `session_before_switch` | `{ cancel?: true }` | Yes (cancel) | Before `/new` or `/resume`. |
| 4 | `session_before_fork` | `{ cancel?, skipConversationRestore? }` | Yes (cancel) | Before `/fork` / `/clone`. |
| 5 | `session_before_compact` | `{ cancel?, compaction? }` | Yes (cancel + custom summary) | Replace compaction summary inline. |
| 6 | `session_compact` | void | No | After compaction completes. |
| 7 | `session_shutdown` | void | No | Cleanup before runtime tear-down. |
| 8 | `session_before_tree` | `{ cancel?, summary? }` | Yes (cancel + custom) | Before `/tree` navigation. |
| 9 | `session_tree` | void | No | After tree navigation lands. |
| 10 | `context` | `ContextEventResult { messages? }` | No, but rewrites messages | Modify message list before each LLM call. |
| 11 | `before_provider_request` | `BeforeProviderRequestEventResult { request? }` | Yes (replace payload) | Inspect or replace the outgoing provider request. |
| 12 | `after_provider_response` | void | No | Status + headers before stream consume. |
| 13 | `before_agent_start` | `BeforeAgentStartEventResult { systemPrompt?, messages? }` | Yes (replace systemPrompt) | Inject message or rewrite system prompt. |
| 14 | `agent_start` | void | No | Agent loop began. |
| 15 | `agent_end` | void | No | Agent loop ended; `event.messages` final. |
| 16 | `turn_start` | void | No | Single LLM call about to fire. |
| 17 | `turn_end` | void | No | Single LLM call returned. |
| 18 | `message_start` | void | No | Assistant message bookkeeping. |
| 19 | `message_update` | void | No | Token-level streaming update — main observability hook. |
| 20 | `message_end` | `MessageEndEventResult { suppress? }` | Yes (suppress) | Final message form. |
| 21 | `tool_execution_start` | void | No | Built-in/extension tool about to run. |
| 22 | `tool_execution_update` | void | No | Streaming partial result. |
| 23 | `tool_execution_end` | void | No | Tool finished, isError known. |
| 24 | `model_select` | void | No | User changed model (`/model` / Ctrl+P). |
| 25 | `thinking_level_select` | void | No | Thinking level changed. |
| 26 | `tool_call` | `ToolCallEventResult { block?, blockReason? }` | Yes (block) | Pre-tool gate — implement permission policy here. |
| 27 | `tool_result` | `ToolResultEventResult { result? }` | Yes (replace result) | Post-tool transform / redaction. |
| 28 | `user_bash` | `UserBashEventResult { block?, blockReason?, replaceCommand? }` | Yes (block + replace) | User-typed `!cmd` shortcut. |
| 29 | `input` | `InputEventResult { handled?, transformed? }` | Yes (intercept) | First chance at the raw user input. |

## Most useful events for Hermes orchestration

- **`message_update`** — when piping through `pi --mode json | jq`, this is the
  token-level event you filter on (see `## Fast Streaming Recipes` in `SKILL.md`).
- **`tool_call` / `tool_result`** — implement Hermes-side permission policy by
  loading a small extension that subscribes here.
- **`before_provider_request`** — record/redact provider payloads for audit.
- **`session_before_compact`** — supply a custom compaction summary (e.g. a
  Hermes-managed summarizer call).
- **`session_shutdown`** — dispose Hermes-side resources (subprocesses, locks)
  when Pi exits.

## Lifecycle diagram

See [`assets/pi-event-lifecycle.txt`](../assets/pi-event-lifecycle.txt) for the
verbatim ASCII diagram (source: `packages/coding-agent/docs/extensions.md:266-335`).
