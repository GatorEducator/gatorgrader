# AGENTS.md

This document provides guidelines for AI agents contributing to this repository.

## Overview of Instructions

- **Always use `uv`:** Use uv for all dependency management, virtual
  environments, and task running. Do not use pip or venv directly.
- **Follow all guidelines:** Follow this file and applicable nested AGENTS.md.
  Routine agent work does not require reading CONTRIBUTING.md; consult it
  when editing contributor guidance or preparing issues, PRs, and reviews.
- **Verify your changes:** Before handoff or any authorized commit, run all
  linters and tests with `uv run task all`; report failures and limitations.
- **Line width:** All text files should have a line width of 80 characters.
- **Permission to run commands:** You may run verification commands here;
  this does not authorize publication, hook installation, or Git mutations.
- **Incremental changes:** Make small, incremental changes; avoid unrelated
  repairs. Inspect git status and diffs first and preserve existing work.
- **Communicate clearly:** Explain what changed and why.
- **Create and Follow a TODO List:** Always create and follow a TODO list.
  Use tool results to verify completion; report blockers honestly.

## Notification Instructions

Send a desktop notification for questions, feedback requests, and completion.
Standing permission covers notification calls, not installation. Adapt the
message; report unavailable tools or desktop access. See
[AI Agent Permissions](README.md#ai-agent-permissions).

Linux:

```bash
notify-send "Coding agent" "Task complete or feedback needed."
```

macOS:

```bash
osascript -e 'display notification "Task complete." with title "Agent"'
```

Windows, in PowerShell with BurntToast installed (process-only policy bypass):

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command {
  Import-Module BurntToast
  New-BurntToastNotification -Text "Agent", "Task complete."
}
```

One-time setup in a regular PowerShell terminal, only with authorization:

```powershell
Install-Module -Name BurntToast -Scope CurrentUser
```

Optionally, inside Zellij with the tools available, also send a session
notification. It does not replace the desktop notification. Keep the
two-second timeout and trailing message space; no special font is needed.

```bash
timeout 2 zellij pipe -- \
  "zjstatus::notify::Agent finished. This is really fun. "
```

## Build, Lint, and Test Commands

Run from the repository root; review diffs after fix commands.

- **Install dependencies:** `uv sync` (includes dev dependencies).
  Keep dependency and lock updates together.
- **Run all tasks:** `uv run task all` (lint, test, cover).
- **Run all linters:** `uv run task lint` (Ruff checks/formatting, Bandit,
  Radon complexity/maintainability reports, and Xenon thresholds).
- **Format code:** `uv run task format-check` (check),
  `uv run task format` (fix)
- **Test all:** `uv run task test`
- **Test with coverage:** `uv run task cover`; included in all.
  `uv run task test-coverage` is an alias, not an additional requirement.
- **Run a focused test:**
  `uv run pytest tests/checks/test_check_ConfirmFileExists.py`
- **Markdown lint:** Use the existing Markdown hook with explicit files;
  all covers Python, not Markdown. No type-checking or comment-case task
  is configured. Use the Markdown hook only when its configuration exists.
- **Local hooks:** Only use hooks when their configuration exists.
  Install only with developer authorization. Check working
  files with `uv run pre-commit run --files` followed by explicit paths;
  never implicitly stash. Hooks check commit messages, not PR titles.
  Smoke tests export the Git index, not the working tree; do not stage to
  test them. Linked checkouts share hooks.

## Code Requirements

All Python code, including tests, should follow these standards:

- **Docstrings:** Add module/function docstrings; preserve established style.
- **Imports:** Group standard library, third-party, then local imports.
  Use absolute imports such as `from gator import checkers`;
  put imports at module scope and avoid wildcards.
- **Formatting:** Use configured Ruff formatting (79 columns and trailing
  commas); soft-wrap Markdown near 80 columns where practical.
- **Naming:** Meaningful snake_case functions/variables, PascalCase classes,
  UPPER_SNAKE_CASE module constants where used.
- **Constants over literals:** Reuse namedtuple records and create_constants
  in [gator/constants.py](gator/constants.py) instead of duplicating magic
  strings. Readable test literals are permitted.
- **Error handling:** Catch specific exceptions, not generic Exception;
  provide meaningful messages, avoid mutable defaults, and use context
  managers for cleanup. Never add secrets or debugger/Snoop leftovers.
- GatorGrade-only contiguous bodies, mandatory full type hints, lowercase
  comments, source-prose backtick bans, universal literal extraction,
  pathlib-only operations, and Pydantic are not adopted here.

## Project Structure Requirements

- Source code belongs in gator/; CLI entry is gatorgrader.py. Tests mirror
  source under tests/, including tests/checks/ for check plugins.
- Use uv for dependency management, environments, and task running.
- Preserve compatibility with Python 3.10–3.14 on macOS, Linux, and Windows
  (CI); metadata requires >=3.10,<4.0.
- Check plugins live in gator/checks/check_CHECKNAME.py and expose
  get_parser(), parse(args), and
  act(main_parsed_arguments, check_remaining_arguments). Delegate parsing
  to checkers.parse(get_parser, args) and follow existing reporting;
  mirror [ConfirmFileExists](gator/checks/check_ConfirmFileExists.py).
- Preserve CLI flags, check names/arguments, external-plugin contracts,
  results, diagnostics, and JSON output unless the request calls for a
  change; document intended migration steps. GatorGrade configuration,
  scoring, and auto-hints belong to the separate repository.

## Testing Requirements

- Tests follow the Python code requirements above.
- Use descriptive test_ names; group by function and order logically.
- Tests must be independent, support random ordering, and work locally and
  in CI. Add behavior, regression, and relevant failure-path tests.
- Aim for full function, statement, and branch coverage; explain uncovered
  behavior. Preserve the 99% executed floor and branch measurement on gator;
  never lower or game measurement or remove failing tests merely to pass.
- Follow existing parametrization, temporary filesystem fixtures, and
  reset_results_dictionary for shared report state where appropriate.
  Use registered pytest markers.

## Making Changes

1. **Understand:** Explore the request and relevant code. Follow the
   [Code of Conduct](CODE_OF_CONDUCT.md); review generated work and verify
   APIs/references against sources. Claim only verification actually done.
1. **Plan:** Create a clear plan before changing files.
1. **Implement:** Make small changes; update affected docstrings, examples,
   README, and contributor documentation. Ask before adding runtime
   dependencies, changing CI, renaming public APIs, or removing checks/tests
   unless explicitly requested.
1. **Verify:** Run `uv run task all` (includes executed coverage). Fix
   introduced failures and report existing ones. For user-visible changes,
   test a disposable assignment against the edited checkout and verify its
   import origin; record directory, inputs/configuration, command, expected
   and actual output, exit code, OS, and Python version, including relevant
   passing/failing JSON cases. Redact credentials and private student data.
1. **Commit:** The software developer commits. Do not stage, commit, create
   branches, switch checkouts, push, or publish without explicit authorization.
   Follow [commit standards](docs/COMMIT_MESSAGES.md); disclose substantial
   AI assistance, known model/version, and actual verification so the
   developer can include the required body and Assisted-by trailer.
1. **Rules:** Changes normally need an issue: check duplicates, prepare an
   issue/team comment before starting, or justify a minor-change exception
   in the PR; ask a maintainer when unsure. Complete the PR template, target
   master, include the release classification (small change, feature,
   compatibility breaking update, or non-versioned change), link relevant
   issues, and prepare the PR URL comment for every
   linked issue, including later links. Draft communication unless publishing
   is authorized. Before merge, require passing CI and a team member plus
   Integration team review; use formal reviews, not conversation approvals.
1. **Completion:** Summarize completed tasks, methods, challenges, applicable
   rules, verification commands/results, environment, and limitations.

## Additional Notes for the Coding Agent

Append durable project notes as a Markdown list when useful, not routine logs.

- **Legacy tooling:** scripts/tasks.py is an Invoke/pyenv helper with an
  unsupported Python 3.7.3 default, not normal setup. Use uv directly.
- **Never run `git stash`:** Preserve existing tracked, untracked, and staged
  work. Use a separate worktree or developer-authorized commit if necessary;
  the developer handles rebasing and cleanup.
- **Creativity is welcome:** Occasional natural flair is optional.
- Keep documented task names and inline local file references valid.
