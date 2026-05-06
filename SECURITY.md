# Security Policy

The `hermes-pi` skill is documentation + tests + assets. It does not execute
code on your behalf or require credentials.

## Reporting issues

Please open a GitHub issue for security-sensitive behavior such as:

- the symlink installer clobbering files outside
  `~/.hermes/skills/autonomous-ai-agents/pi/`;
- `mise run sync` performing a non-fast-forward update or rewriting history;
- the skill loading and exposing secrets from disk.

## Secret handling

Do not include real credentials, tokens, connection strings, or private `.env`
files in skill content, references, tests, assets, issues, or generated
fixtures.
