# Pi Skill Tests (RED → GREEN harness)

Runs structural and behavioral assertions on `~/.hermes/skills/autonomous-ai-agents/pi/`.

## Run

```bash
python3 -m pytest /Users/kiren/.hermes/skills/autonomous-ai-agents/pi/tests/ -x -q
```

## RED → GREEN map

| RED ID | Test file | Asserts |
|--------|-----------|---------|
| R01    | test_r01_frontmatter.py | SKILL.md frontmatter (name, description, license, related_skills, tags) |
| R02    | test_r02_required_sections.py | All required `##` headings in order |
| R03    | test_r03_non_interactive_mandate.py | Phrase "non-interactive only" present |
| R04    | test_r04_fast_streaming_recipe.py | Canonical fast-streaming command + jq filter |
| R05    | test_r05_extension_events.py | All 29 events documented + lifecycle diagram asset |
| R06    | test_r06_source_traceability.py | Every cited opensrc path resolves |
| R07    | test_r07_philosophy_quotes.py | Verbatim YouTube + README quotes preserved |
| R08    | test_r08_hermes_integration.py | Code blocks use terminal()/process()/mcp_skill_* |
| R09    | test_r09_rpc_framing.py | Warns against Node readline + cites jsonl.ts:14-19 |
| R10    | test_r10_primitive_coverage.py | Every Pi primitive token mentioned by exact string |
| R11    | test_r11_agent_session_event.py | AgentSessionEvent / AgentEvent unions match docs/json.md |
| R12    | test_r12_smoke.py | pi --version, pi --help, pi -p exit deterministically |
| R13    | test_r13_skill_register.py | Skill is discoverable via mcp_skills_list |
| R14    | test_r14_forbidden_tokens.py | No tmux send-keys, pty=true, etc. anywhere |
| R15    | test_r15_mcp_anti_pattern.py | MCP framed as opt-in / anti-pattern by default |
| R16    | test_r16_pi_vs_claude_code.py | Comparison matrix has >=12 cited rows |
| R17    | test_r17_worktree_isolation.py | Mandatory worktree section + git worktree add + workdir= |

A successful RED phase has all of these tests **failing**. After GREEN content is written, all
must pass; the tests are the regression suite for REFACTOR.
