# Local contribution checks

These hooks reuse project commands and the commitlint configuration in CI.

## Setup

Prepare the project's uv environment first, following CONTRIBUTING.md.

```bash
uv sync
```

The Markdown hook manages Ruby 3.3.10 and the existing Ruby Markdown linter.
The config uses an array so whitespace cannot disable every Markdown rule.
A small wrapper also rejects an empty enabled-rule list; CI uses that same
hook. It checks the README and staged Markdown on every commit.
Canonical LICENSE.md is excluded from style checks and kept byte-for-byte.
Existing prose/template formatting is corrected so enabled rules can pass.
Its first installation can require a compiler and take several minutes.
Native Windows support for that Ruby bootstrap is not verified here.
The bundled builder lacks Ruby 3.3.13; update that bootstrap before adopting
the latest Ruby patch in a production rollout.

Install both Git hook stages using uv:

```bash
uv run task hooks-install
```

This uses pre-commit 4.6.0 from the project development dependencies; runtime
dependencies are unchanged.
Node 24.22.2 and hook tools are isolated and installed on first use.
The LTS pin avoids the incompatible system npm 12 flags in pre-commit 4.6.
First setup needs network access. Install again after cloning; Git does
not clone hooks.

## What an ordinary commit checks

- Every commit: the small documented-task and coverage-setting guards.
- Markdown changes: the project's Markdown rules.
- Python, TOML, YAML, shell, or lock changes: uv run task all. This already
  includes executed statement/branch coverage.
- Commit messages: the same basic Conventional Commits header checks as CI,
  accepting custom types and either breaking marker without requiring both.
  PR titles do not need a type prefix and are not checked by these hooks.

Checks report failures and abort a normal commit. They do not auto-format or
edit source. Fix the problem, stage the correction, and retry.
The code gate runs the whole project, so unfinished untracked source can
also affect it; hooks do not delete those files.
Documentation-only commits avoid the full code suite.

To run the pre-commit-stage checks against all tracked files:

```bash
uv run task hooks-check
```

That command includes the full code suite because code files are selected;
it does not invent a new coverage threshold or replace CI.

## Test the installed hooks

Run uv run task test-hooks to test real Git commits in a temporary clone.
It checks bad commit messages, bad staged task names, malformed Markdown,
disabled branch coverage, and invalid Python, then verifies recovery.
It does not install hooks in your working clone or change its history.
CI runs this smoke test separately from the application test suite.

Linked Git checkouts share a hook directory. Installing hooks in one can
affect the others; use a dedicated clone when they need different configs.

## Enforcement limits

Local hooks are opt-in and can be bypassed through Git options or settings.
They cannot prove someone read instructions or truthfully disclosed AI use,
chose the correct commit type, or identified a real breaking change.

Keep required CI lint, tests, coverage, Markdown/spelling, and commit-message
checks on the protected target branch. Maintainers must make them required
and restrict bypass permissions if they want merge-time enforcement.
Installing hooks does not change GitHub repository settings.

See [pre-commit documentation](https://pre-commit.com/) and the project's
[commit-message standards](COMMIT_MESSAGES.md).
