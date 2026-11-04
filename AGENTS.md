# AGENTS.md

Self-contained instructions for coding agents working on **GatorGrader**.
Routine agent work does not require reading CONTRIBUTING.md.

## Project and setup

GatorGrader implements checks for student writing and source code. It runs
as a standalone CLI or through GatorGrade. GatorGrade's configuration,
scoring, reports, and auto-hints belong to that separate repository.

- Source: `gator/`; CLI entry: `gatorgrader.py`.
- Check plugins: `gator/checks/check_*.py`; tests: `tests/`, including
  `tests/checks/`; dependencies and tasks: `pyproject.toml`.
- Python metadata: `>=3.10,<4.0`; CI tests 3.10–3.14 on Linux, macOS, and
  Windows. Preserve compatibility across that matrix.
- Always use **uv** for dependencies, environments, and tasks; do not use
  `pip` or `venv` directly. From the repository root, run `uv sync`.
  This installs the checkout in editable mode and includes the dev group.
- To select another Python version, use `uv python pin <version>`, then
  `uv sync`. Review any pin-file changes before including them in a PR.

## Verification commands

You have permission to run the commands in this file.

| Purpose | Command |
| --- | --- |
| Required before handoff or any commit | `uv run task all` |
| All Python linters | `uv run task lint` |
| Check formatting | `uv run task format-check` |
| Rewrite formatting; review the diff | `uv run task format` |
| Tests | `uv run task test` |
| Statement and branch coverage | `uv run task cover` |
| Focused check tests | `uv run pytest tests/checks/test_check_ConfirmFileExists.py` |

- `all` runs `lint`, `test`, and `cover`; no separate coverage run is needed
  after a successful `all`. `test-coverage` is an alias for `cover`.
- Lint includes Ruff checking and formatting, Bandit, Radon complexity and
  maintainability reports, and Xenon thresholds. Individual tasks are
  `lint-ruff`, `lint-ruff-format`, `lint-bandit`, `lint-radon-cc`,
  `lint-radon-mi`, and `lint-xenon`, each run with `uv run task`.
- Maintain 100% statement and branch coverage where possible; explain any
  uncovered behavior in the PR. The configured minimum on `gator` is 99%.
  Do not lower the threshold or game tests or coverage to pass.
- CI separately lints Markdown using `.mdlrc`; `all` covers Python checks.
  No type-checking, comment-case, or Markdown task is configured in taskipy.

For manual checks, run `uv run gatorgrader --help` or
`uv run gatorgrader --nowelcome ListChecks`. From a disposable assignment
directory, run this command against the edited checkout:

```bash
uv run --project /absolute/path/to/gatorgrader gatorgrader --nowelcome \
  ConfirmFileExists --file example.txt --directory .
```

Quote a project path containing spaces. Try with the file present and
absent; expect exit codes 0 and 1 respectively. Record the working directory,
inputs, command, expected and actual results, OS, and Python version.
Verify the imported checkout with:

```bash
uv run --project /absolute/path/to/gatorgrader python -c \
  "import gator; print(gator.__file__)"
```

When .pre-commit-config.yaml is present, run uv run pre-commit install
after uv sync to enable the configured pre-commit and commit-msg hooks.
Use uv run pre-commit run --all-files for a full local hook check. Hooks
check commit messages, not PR titles, and do not replace the required
project gate. Linked Git checkouts share hooks; use a dedicated clone if
their configurations differ.

## Coding and testing rules

- Follow existing conventions and Ruff: Python line length 79; rules E, D,
  I, F, PL, Q, RUF, W, T201, with D203, D213, E501 ignored. Soft-wrap Markdown
  near 80 columns where practical.
- Add module and function docstrings; preserve each file's established
  style. Use meaningful names, snake_case functions and variables,
  PascalCase classes, and UPPER_SNAKE_CASE module constants where used.
- Group top-level imports as standard library, third-party, then local
  `from gator import ...`. Keep imports at module scope; avoid wildcards.
- Reuse `gator/constants.py` namedtuple records and `create_constants`
  rather than duplicating existing magic strings.
- Catch specific exceptions; avoid mutable defaults; use context managers
  for resource cleanup. Never add secrets, credentials, or debug leftovers.
- A check plugin exposes `get_parser()`, `parse(args)`, and
  `act(main_parsed_arguments, check_remaining_arguments)`. Mirror
  `gator/checks/check_ConfirmFileExists.py`; parsing delegates to
  `checkers.parse(get_parser, args)`.
- Preserve CLI flags, check names and arguments, external-plugin contracts,
  result/diagnostic behavior, and JSON output unless the issue calls for a
  compatibility change. Document intended changes and migration steps.
- Tests mirror source structure, use descriptive `test_` names, and group
  related cases in a readable order. Tests must be independent and work
  locally and in CI. Follow existing parametrization patterns.
- Add or update tests for new behavior and regression cases, including
  failure paths. Use temporary filesystem fixtures and reset shared report
  state with `reset_results_dictionary` where appropriate. Do not remove
  failing tests to make the suite pass. Test literals may improve readability
  (Ruff's PLR2004 exception).
- Do not import GatorGrade-only requirements such as mandatory full type
  hints, lowercase-only comments, contiguous function bodies, extraction of
  every literal, Pydantic, or unconfigured type checkers.

## Workflow and permissions

- Understand the request, create a TODO list, make a plan, and complete it
  through small, focused changes. Explain what changed and why.
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md) in project interactions.
- Update docstrings, examples, README, and contributor documentation when
  behavior changes. Include verification commands, results, environment,
  and limitations in the PR description.
- Changes normally need an issue. Decide case by case whether a minor fix
  needs a separate issue; explain the scope and reason in the PR if it does
  not, and ask a maintainer when uncertain. When working on an issue, comment
  before starting with the contributor or team names. Broader design
  discussion is encouraged but optional.
- Check for duplicates when discovering another problem, even during an open
  PR. Link relevant issues in the PR and comment its URL on every linked
  issue, including links added later.
- These workflow rules do not authorize publishing issues or comments.
  Prepare drafts unless the developer explicitly authorizes publication.
- Run `uv run task all` before handoff and before any commit. Fix introduced
  failures; report existing failures and verification limitations accurately.
  Summarize completed work, verification, challenges, and applicable rules.
- Review and test generated changes; verify APIs and references against
  project sources. Do not invent facts or verification results, and keep
  generated communication respectful.
- Identify AI-assisted work and actual verification in the handoff so the
  developer can document them in the commit body and add an
  `AI-Assisted: <tool name>` trailer. Leave human approval to the developer.
- The developer commits changes unless they explicitly ask you to commit.
  Follow the [commit message standards](docs/COMMIT_MESSAGES.md). Complete
  the PR template, including its required
  release classification; obtain maintainer reviews and passing checks
  before merge. Use Comment, Approve, or Request changes review states;
  a conversation comment does not count as an approval.
- **Never run `git stash`.** Preserve work with a separate worktree or a
  developer-authorized commit. The developer handles rebasing and cleanup.
- Ask before adding runtime dependencies, changing CI/workflows, renaming
  public APIs, or removing checks or tests.

## Notifications

Send a desktop notification when a task finishes, feedback is needed, or you
ask a question. Permission is already granted. Adapt the title and message;
use the command for the current OS and report unavailable tools.

Linux:

```bash
notify-send "Coding agent" "Task complete or feedback needed."
```

macOS:

```bash
osascript -e 'display notification "Task complete." with title "Agent"'
```

Windows, in PowerShell with BurntToast installed:

```powershell
Import-Module BurntToast
New-BurntToastNotification -Text "Coding agent", "Task complete."
```

If needed, run setup once in a regular PowerShell terminal:

```powershell
Install-Module -Name BurntToast -Scope CurrentUser
```

[BurntToast](https://github.com/Windos/BurntToast) is archived; existing
releases remain available. It is an optional notification tool, not a
GatorGrader dependency.

When running inside Zellij, also send its session notification if the tools
are available. Keep the two-second timeout and trailing message space. This
supplements the desktop notification; it does not replace it.

```bash
timeout 2 zellij pipe -- \
  "zjstatus::notify::Agent finished. This is really fun. "
```

## Task-specific references

- `scripts/tasks.py` is a legacy Invoke/pyenv helper, not normal setup. Its
  default Python 3.7.3 is unsupported, Invoke is not a declared dependency,
  and it changes the selected local Python version. Use uv directly; see
  [issue #313](https://github.com/GatorEducator/gatorgrader/issues/313).
- Consult README.md for product behavior and CONTRIBUTING.md only when
  editing or reviewing human contributor guidance. Keep these agent
  instructions independently usable and aligned with shared requirements.
- Append durable project notes here as a Markdown list when useful.
