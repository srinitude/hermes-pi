# Pi Fast Streaming Recipes (Latency-budgeted)

Pi has no `--bare` flag (that is Claude Code terminology). Pi's equivalent
is the explicit `--no-*` set. Combined with `--offline` / `PI_OFFLINE=1` /
`PI_SKIP_VERSION_CHECK=1`, these flags collapse Pi's startup cost to roughly
node-startup-time + provider-handshake.

Source citations:
- `packages/coding-agent/src/cli/args.ts:135-136` (`--no-extensions`/`-ne`)
- `packages/coding-agent/src/cli/args.ts:146-147` (`--no-skills`/`-ns`)
- `packages/coding-agent/src/cli/args.ts:148-149` (`--no-prompt-templates`/`-np`)
- `packages/coding-agent/src/cli/args.ts:150-151` (`--no-themes`)
- `packages/coding-agent/src/cli/args.ts:152-153` (`--no-context-files`/`-nc`)
- `packages/coding-agent/src/cli/args.ts:104-105` (`--no-tools`/`-nt`)
- `packages/coding-agent/src/cli/args.ts:163-164` (`--offline`)

## Canonical fast-streaming command (≤ 1 s first-token TTL on warm node cache)

Combines all eight startup-cost-reduction flags in a single block:

```bash
PI_OFFLINE=1 PI_SKIP_VERSION_CHECK=1 pi \
  --mode json \
  --offline \
  --no-context-files \
  --no-skills \
  --no-prompt-templates \
  --no-themes \
  --no-extensions \
  --thinking off \
  --no-session \
  --tools read,grep,find,ls \
  "What does src/index.ts export?" \
  | jq -rj 'select(.type=="message_update") | .assistantMessageEvent.delta // empty'
```

The `jq` filter prints only token-level deltas — first byte appears as soon as
the provider streams its first token. No buffering pitfalls because `jq -rj`
flushes per-record and pi writes events one JSON line per `message_update`
(`packages/coding-agent/src/modes/print-mode.ts`).

## Variant A — measure first-token TTL

Hermes can wrap the canonical command in `time` and capture stderr to a metric
sink. Budget: `< 500 ms` cold node startup is unrealistic, but `< 1 s` first
JSON line on warm cache is achievable.

```python
terminal(
    command=(
        "/usr/bin/time -p bash -c '"
        "PI_OFFLINE=1 PI_SKIP_VERSION_CHECK=1 pi --mode json --offline "
        "--no-context-files --no-skills --no-prompt-templates --no-themes "
        "--no-extensions --thinking off --no-session "
        "--tools read,grep,find,ls \"echo hi\" "
        "| jq -c \"select(.type==\\\"message_update\\\")\" | head -1'"
    ),
    workdir="/Users/kiren/repos/myapp",
    timeout=30,
)
```

## Variant B — drain to a file in the background, poll for tail

```python
session = process(
    action="start",
    command="pi --mode json --offline --no-extensions --no-skills --no-context-files --no-prompt-templates --no-themes 'Long task...'",
    workdir="/Users/kiren/repos/myapp",
)
# Hermes notify_on_complete=True trips when the process exits.
# Meanwhile, poll incrementally:
for batch in process(action="poll", session_id=session.id):
    handle(batch)  # parse LF-delimited JSON lines
```

## Variant C — pin to lowest-cost model with PI_CACHE_RETENTION

`PI_CACHE_RETENTION=long` opts into Anthropic 1-hour / OpenAI 24-hour prompt
caching (`packages/coding-agent/README.md:632`). Hermes can set it once per
turn:

```python
terminal(
    command="PI_CACHE_RETENTION=long PI_OFFLINE=1 PI_SKIP_VERSION_CHECK=1 pi --mode json --offline --no-extensions --no-skills --no-prompt-templates --no-themes --no-context-files --provider openai --model gpt-4o-mini --thinking off 'Tell me about file foo.ts'",
    workdir="/Users/kiren/repos/myapp",
    timeout=120,
)
```

## What NOT to do

- `pi -p` without `--offline`: pi will attempt a startup network call to
  `pi.dev/api/latest-version`, adding ~100-300 ms cold start.
- Parsing pi JSON output with regex: events are JSON objects, sometimes with
  embedded U+2028/U+2029. Use `jq` or a real JSON parser.
- Using Node `readline` to consume `--mode rpc` output: it splits on
  Unicode line separators and corrupts JSON payloads
  (`packages/coding-agent/src/modes/rpc/jsonl.ts:14-19`).
