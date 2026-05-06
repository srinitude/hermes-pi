# Contributing

Thanks for improving the Hermes `pi` skill.

## Quality bar

- All edits to skill content (`SKILL.md`, `references/`, `tests/`, `assets/`)
  flow through this repo + git, never through the in-Hermes path directly.
- Keep `make sync` fast-forward only — never rebase, never force-push.
- Keep `make verify-sync` green: symlink + clean tree + `HEAD == origin/main`.
- Keep new files within the styleguide: ≤ 200 LOC per file, ≤ 30 LOC per
  function/class/test, max nesting depth 3.

## Local checks

```bash
mise install
mise run setup
make ci
```

`make ci` runs the lint + verify-sync + test pipeline that GitHub Actions
mirrors. The CI workflow lives at `.github/workflows/ci.yml`.

## Release checklist

1. Bump `SKILL.md` frontmatter `version`.
2. Append a `## [x.y.z] - <ISO date>` section to `CHANGELOG.md`.
3. Tag the release with `git tag -a vX.Y.Z` and push the tag.
