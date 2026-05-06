# Pi Philosophy (verbatim quotes + attribution)

This reference preserves the load-bearing philosophy quotes that the `pi` skill must
surface verbatim. Every quote is attributed to its primary source. The full talk
is captured in [`assets/pi-philosophy-transcript.txt`](../assets/pi-philosophy-transcript.txt).

## Primary sources

- **YouTube:** Mario Zechner, "Pi: a malleable coding agent" (talk at Tessl, London).
  https://www.youtube.com/watch?v=Dli5slNaJu0  (video id `Dli5slNaJu0`).
- **README:** `packages/coding-agent/README.md:466-484` (the *Philosophy* section).
- **Blog post:** https://mariozechner.at/posts/2025-11-30-pi-coding-agent/

## Verbatim quotes

> "strip away everything and build a minimal extensible core"
>
> — YouTube `Dli5slNaJu0`, paraphrased thesis statement near the end of the talk.
> Transcript char offset ≈ 13900 (search the transcript for this phrase).

> "What's not in there? No MCP, no sub agents, no plan load, no background bash, no built-in to-do's"
>
> — YouTube `Dli5slNaJu0`, list of explicit non-features. Transcript char offset ≈ 17500.
> Mirrored in `packages/coding-agent/README.md:466-484` as the bulleted negation list.

> "the smallest most minimal interface a model can have to your computer"
>
> — YouTube `Dli5slNaJu0`, on the Terminal-Bench Terminus harness inspiration.
> Transcript char offset ≈ 12200.

> "almost zero extensibility ... if you compare it to what pi allows you to do, it's not as deeply integrated"
>
> — YouTube `Dli5slNaJu0`, comparing Claude Code's hook system against Pi's
> in-process TypeScript extensions. Transcript char offset ≈ 7600.

> "based on running a process when the hook event starts, which is very expensive
> if you have to start up that process over and over again"
>
> — YouTube `Dli5slNaJu0`, the explicit critique of process-spawn hook systems
> (Claude Code's hooks, OpenCode's CLI hooks). Pi answers this with TypeScript
> extensions that load once and stay resident in the agent process.
> Transcript char offset ≈ 7700.

## README Philosophy section (mirrored)

The skill reproduces, verbatim, this passage from `packages/coding-agent/README.md:466-484`:

> Pi is aggressively extensible so it doesn't have to dictate your workflow.
> Features that other tools bake in can be built with extensions, skills, or
> installed from third-party pi packages. This keeps the core minimal while
> letting you shape pi to fit how you work.
>
> **No MCP.** Build CLI tools with READMEs (see Skills), or build an extension
> that adds MCP support.
>
> **No sub-agents.** There's many ways to do this. Spawn pi instances via tmux,
> or build your own with extensions, or install a package that does it your way.
>
> **No permission popups.** Run in a container, or build your own confirmation
> flow with extensions inline with your environment and security requirements.
>
> **No plan mode.** Write plans to files, or build it with extensions, or
> install a package.
>
> **No built-in to-dos.** They confuse models. Use a TODO.md file, or build
> your own with extensions.
>
> **No background bash.** Use tmux. Full observability, direct interaction.

## Why this matters for Hermes

The "no MCP / no sub-agents / no plan mode / no permission popups / no built-in
to-dos / no background bash" list defines the boundary of what Pi will *not*
do for you. Hermes Agent recipes that depend on any of these features must
either skip them or implement them at the Hermes layer (not assume Pi will
provide them). The MCP bridge in particular is treated as opt-in / anti-pattern
by default — see `references/pi-vs-claude-code.md` and the `## MCP Bridging`
section of `SKILL.md`.

## Pi's term for "hooks"

In the talk Mario uses the word "hook" colloquially. Pi's source code and
documentation use **`extensions/`** for the same concept (the `hooks/` directory
was renamed; pi prints a deprecation warning if it sees a `hooks/` directory:
`packages/coding-agent/src/migrations.ts:217-228`). Throughout this skill we
use *extension events* in code references and *hook events* only when echoing
the user's vocabulary.
