# Contributing to GatorGrader

Thank you for helping improve GatorGrader! Contributions include code,
documentation, tests, bug reports, and pull request reviews. Start with the
[README](README.md) to understand how the tool works, and follow our
[Code of Conduct](CODE_OF_CONDUCT.md) in all project interactions.

> [!NOTE]
>
> This guide covers GatorGrader: checks for student writing and source code,
> command execution, and check plugins. For changes to GatorGrade's assignment
> configuration, scoring, reports, history, and hints, see the
> [GatorGrade contribution guide][gatorgrade-guide].

## Table of Contents

- [Use of AI](#use-of-ai)
- [Finding ways to help](#finding-ways-to-help)
- [Raising and tracking issues](#raising-and-tracking-issues)
- [Development setup](#development-setup)
- [Local checks and hooks](#local-checks-and-hooks)
- [Coding standards](#coding-standards)
- [Testing and checks](#testing-and-checks)
- [Contributor scripts](#contributor-scripts)
- [Documentation and debugging](#documentation-and-debugging)
- [Making a pull request](#making-a-pull-request)
- [Reviewing a pull request](#reviewing-a-pull-request)
- [Merging and releasing](#merging-and-releasing)
- [Getting help and external resources](#getting-help-and-external-resources)

## Use of AI

Review and test AI-assisted code, documentation, and communication for
accuracy, safety, and respectful language. You remain responsible for the
result; only claim verification you performed.

Disclose substantial AI assistance in contributions and project communication.
In affected commit bodies, explain the tool's contribution and how you
verified it, then add an `Assisted-by: <tool name>` trailer. Include the
model and version when known.

## Finding ways to help

Check [issues][issues], [pull requests][pulls], and related discussions before
starting. Look for [good-first-issue][first] and [help-wanted][help-issues]
labels. You can improve examples or documentation, report a reproducible
bug, add a regression test, or review a pull request.

Coordinate overlapping work in issue comments. Keep changes small and easy
to review and verify.

## Raising and tracking issues

Changes normally need an issue. Decide minor fixes, such as typos or small
documentation changes, case by case. If you skip an issue, explain the scope
and reason in the PR. Ask a maintainer when unsure.

- Search issues and pull requests for duplicates, then
  [open an issue][new-issue] if needed.
- Before starting, comment on the issue with your name and any teammates.
  Broader design discussion is encouraged but optional.
- Complete the bug report or feature request template. Keep reproduction
  steps, expected behavior, and environment details in the issue; see the
  [bug report template][bug-template]. For other changes, explain the
  problem, scope, and verification. Remove credentials and private
  assignment or student data from examples and output.
- Check duplicates and open an issue for other problems you discover, even
  if your PR is already open. Link related work and keep the PR focused.
- Link relevant issues in the PR and comment its URL on **each linked
  issue**, including links added later. Use closing keywords only for fully
  resolved issues; use references for partial or related work.

## Development setup

### Prerequisites

Install [Git][git] and [uv][uv-install]. Package metadata requires Python
`>=3.10,<4.0`; CI currently tests Python 3.10 through 3.14 on Linux, macOS,
and Windows. Use uv for dependency management, virtual environments, and
running project tasks.

### Fork, clone, and create a branch

Fork [GatorEducator/gatorgrader][repository] on GitHub. Replace YOUR-USERNAME
below with your GitHub username, then run:

```bash
git clone https://github.com/YOUR-USERNAME/gatorgrader.git
cd gatorgrader
git remote add upstream https://github.com/GatorEducator/gatorgrader.git
git switch -c docs/contribution-guide
```

Choose a descriptive branch name for your issue. Submit the eventual pull
request from your fork to the upstream repository's master branch.

### Base development environment

From the repository root, run:

```bash
uv sync
uv run task hooks-install
uv run gatorgrader --help
```

Sync creates the environment, installs development dependencies, and makes
this checkout editable: Python edits take effect without reinstalling.
Sync again after dependency or package metadata changes, and keep dependency
changes with their lockfile updates.

Contributors install hooks in each new clone; agents need explicit developer
authorization before installing them. They check staged changes and commit
messages, not PR titles. See [local checks and hooks](#local-checks-and-hooks) for
full checks, and isolated hook smoke tests.

### CI environment and optional dependencies

The base development environment includes the Python tools needed for
uv run task all. GatorGrader has no auto-hint extra; that feature belongs to
GatorGrade. Markdown linting uses a separate managed Ruby environment through
the local hooks; see [local checks and hooks](#local-checks-and-hooks).

To select another supported interpreter, run:

```bash
uv python pin 3.12
uv sync
uv run task test
```

This changes the local Python pin. Review pin-file changes before including
them in your PR; use the CI matrix to verify the other supported platforms.

### Local checks and hooks

The setup command installs both pre-commit and commit-msg hooks. Installation
is local to each clone; cloning or syncing alone does not enable them. The
configured Node and hook tools are installed in isolated environments on
first use, which needs network access. Runtime dependencies are unchanged.

The Markdown hook manages Ruby 3.3.10 and the existing linter. Its first
installation can require a compiler and take several minutes; native Windows
bootstrap support is not verified. It rejects an empty enabled-rule list,
checks README and selected Markdown, and excludes canonical LICENSE.md.

- Every commit runs documented-task and coverage-setting guards, plus the
  Markdown hook, which always checks README.
- Python, TOML, YAML, shell, or lock changes run uv run task all, including
  executed statement/branch coverage. Documentation-only commits avoid this
  full Python gate.
- Commit messages use the same basic Conventional Commits header checks as
  CI. Custom types and either breaking marker are accepted; PR titles are
  not checked by the hooks.

A failed hook aborts a normal commit without auto-formatting or editing
source. Fix the issue, stage the correction, and retry. Code checks run the
whole project, so unfinished untracked source can affect them too.

Check working files without installing hooks or implicitly stashing changes:

```bash
uv run pre-commit run --files AGENTS.md CONTRIBUTING.md
```

Replace the paths with the files to check. For all tracked files, use
uv run task hooks-check; it selects the full code suite and may temporarily
stash tracked edits not staged for commit. Agents must use explicit files.
These commands run pre-commit-stage checks, not the commit-message stage.

Run uv run task test-hooks for isolated rejection/recovery smoke tests of
commit messages, staged task names, Markdown, branch coverage, and Python.
The script exports the Git index, not necessarily uncommitted working files;
do not stage files merely to exercise a patch. It installs hooks and makes
synthetic commits only in a disposable checkout. CI also runs these tests.

Linked Git checkouts share hooks; use a dedicated clone for differing configs.
Hooks are opt-in and can be bypassed. They cannot prove truthful AI disclosure,
appropriate commit types, or compliance with every instruction. CI runs
independently; maintainers must configure required checks and bypass limits
for merge blocking. Hook installation does not change repository settings.
See the [configuration](.pre-commit-config.yaml),
[commit standards](docs/COMMIT_MESSAGES.md), and
[pre-commit documentation](https://pre-commit.com/) for details.

### Running the edited checkout against an assignment

From the repository root, list available checks with:

```bash
uv run gatorgrader --nowelcome ListChecks
```

Keep assignments separate from the source checkout. In a disposable
assignment directory, create an example.txt file, then run:

```bash
uv run --project /absolute/path/to/gatorgrader gatorgrader --nowelcome \
  ConfirmFileExists --file example.txt --directory .
```

Replace the project path with your checkout's absolute path; quote it if it
contains spaces. The project option selects GatorGrader's environment while
preserving the assignment as the working directory. This check should pass
with exit code 0. Remove the disposable example file and rerun it; the
check should fail with exit code 1. Use --json before the check name when
verifying machine-readable output.

Confirm the imported source comes from your checkout:

```bash
uv run --project /absolute/path/to/gatorgrader python -c \
  "import gator; print(gator.__file__)"
```

An installation of GatorGrade or a published GatorGrader release does not
automatically use these local changes. Verify the imported path before
reporting that an edit has no effect. When testing integration with
GatorGrade, verify which GatorGrader checkout that environment imports too.

## Coding standards

- Keep source in gator/ with the CLI entry in gatorgrader.py; mirror the
  source structure in tests/ and place check tests in tests/checks/.
- Use the project's Ruff formatter, configured for 79 columns, and its
  import ordering.
- Soft-wrap Markdown near 80 columns where practical.
- Add module and function docstrings and preserve the established style in
  edited files. Use meaningful names.
- Use snake_case for functions and variables, PascalCase for classes, and
  UPPER_SNAKE_CASE for constants.
- Put imports at the top of the file, grouped as standard library,
  third-party, and local imports. Use absolute local imports and trailing
  commas where the formatter requires them. Avoid wildcards.
- Reuse the namedtuple records and create_constants in gator/constants.py
  rather than duplicating existing magic strings.
- Catch specific exceptions, avoid mutable default arguments, and use
  context managers for resource cleanup. Keep secrets and credentials out
  of source and diagnostic output.

Each check plugin lives in gator/checks/check_CHECKNAME.py and exposes
`get_parser()`, `parse(args)`, and
`act(main_parsed_arguments, check_remaining_arguments)`. Start with
[check_ConfirmFileExists.py][example-check] and its [tests][example-tests].
Its parse function delegates to `checkers.parse(get_parser, args)`; follow
the existing result-reporting path so CLI and JSON behavior stay consistent.

Preserve existing CLI flags and report behavior unless the issue calls for
a compatibility change. Document intended breaking changes and their
migration path in the pull request.

This includes check names and arguments, external-plugin contracts, result
and diagnostic behavior, and JSON output. Maintain behavior across the
Python versions and operating systems in CI.
There is no configured static type-checking task; do not present an
unconfigured checker as a required gate. GatorGrade's separate type-checking,
comment-case, Pydantic, and blanket literal-extraction rules do not apply here.

## Testing and checks

Run tasks from the repository root. Start with focused tests while developing,
then run the required checks before submitting or updating a pull request.

```bash
uv run task all
```

The all task runs lint, test, and cover, in that order. The test task runs
pytest with stop-on-first-failure enabled. Useful commands are:

| Purpose | Command |
| --- | --- |
| Required combined checks | `uv run task all` |
| Linting and format checks | `uv run task lint` |
| Check Python formatting | `uv run task format-check` |
| Fix Python formatting | `uv run task format` |
| Tests | `uv run task test` |
| Statement and branch coverage | `uv run task cover` |

### Writing tests

To run one existing test:

```bash
uv run pytest tests/checks/test_check_ConfirmFileExists.py
```

Focused tests do not replace the required checks. Report failures and
environment limitations in your PR.

- Name tests descriptively with a test_ prefix. Group them by the function
  they exercise and order them logically within each group.
- Keep tests independent and runnable locally and in CI.
- Add or update tests for new behavior and regression cases, including
  relevant failure paths. Do not remove failing tests to make the suite pass.
- Follow existing pytest parametrization patterns. Use temporary filesystem
  fixtures and reset shared report state with the reset_results_dictionary
  fixture where appropriate.
- Test literals may improve readability and are permitted by Ruff's PLR2004
  exception.

### Test coverage

Aim for full function, statement, and branch coverage. If complete coverage
is not possible, explain the uncovered behavior in the PR. The configured
minimum for executed statement and branch coverage is 99% on gator/. Do not
lower the threshold or game coverage to pass.

```bash
uv run task cover
```

The test-coverage task is an alias for cover. A successful all run already
includes this coverage check; no extra coverage invocation is required.

### Code linting

Ruff checks formatting, imports, docstrings, snake_case function names, and
absolute imports. Pytest rejects unregistered markers through the root
pytest.ini configuration.

Ruff's selected rule families are E, D, I, F, PL, Q, RUF, W, and T201, with
D203, D213, and E501 ignored. Ruff also rejects broad exception handlers
and mutable default arguments in its configured file scope.
Bandit checks security patterns; Radon reports
complexity and maintainability; Xenon enforces complexity thresholds.

```bash
uv run task lint
```

Individual tasks are lint-ruff, lint-ruff-format, lint-bandit,
lint-radon-cc, lint-radon-mi, and lint-xenon; run each with uv run task.
The format task **modifies files**; format-check and lint-ruff-format only
check them.

Fix commands modify files; inspect their diffs before including changes in
your PR.

### Continuous integration

[GitHub Actions][ci] runs the project's automated checks. The test matrix
covers the Python versions and operating systems listed under
[Prerequisites](#prerequisites). CI also checks commit headers and runs
isolated installed-hook smoke tests.

Python linting and coverage run on Ubuntu. A separate job checks Markdown
using markdownlint and the [.mdlrc](.mdlrc)
configuration. Markdown linting is not part of uv run task all, and no
Markdown task is configured in taskipy.

Run local checks and review CI results. Report failures and limitations;
only claim checks passed if you ran them.

## Contributor scripts

### Automated contribution policy

The pull request template provides fields checked by the Contribution Policy
workflow: problem, changes, compatibility, verification, contributors,
linked issues or a minor-change exception, AI assistance, documentation
changes, and limitations. Complete these fields and target master. For AI
assistance, choose none or used; if used, identify the tool, its contribution,
and your verification. Keep the required release-classification statement.
These declarations cannot prove truth or test quality.

Metadata validation runs trusted base-branch code, not PR code. The workflow
and validator must first be merged into the target branch; later policy
changes take effect after merge. Fenced examples do not supply declarations.

Local hooks can be bypassed; maintainers must configure required CI checks
and reviews in GitHub for merge-time enforcement.

[scripts/tasks.py](scripts/tasks.py) is a legacy Invoke/pyenv helper around
the same test and cover tasks. It is not required for development. Its
default Python 3.7.3 is outside the current supported range, its wording
still mentions Pipenv, and Invoke is not a declared dependency. It also
changes the local Python selection. Use uv directly as shown above while
[issue #313][legacy-script] tracks whether to fix or retire it.

There are no GatorGrade comment/version/direct-test checkers or mutation
helpers in this repository. Mutation-testing support is separate work in
[issue #312][mutation-issue].

## Documentation and debugging

Update the README for installation, configuration, CLI, or report changes;
update this guide for contributor workflow changes. Keep docstrings and
examples accurate. Documentation-only changes still need Markdown linting
and the applicable CI documentation checks.

For debugging, start with the smallest failing test or disposable assignment.
Use `uv run pytest -x --pdb` to enter the debugger on a test failure, or use
[Snoop][snoop], which is installed with development dependencies. For a
temporary trace, add `import snoop` and decorate the target function with
`@snoop.snoop`. Remove debugging code before submitting the PR.

Record manual checks with:

- Working directory, configuration, input files, and exact command.
- Expected and actual output, exit code, OS, and Python version.
- Passing and failing cases where relevant, including JSON report output.

Use disposable files to trigger checks. Remove credentials and private data
from shared logs.

## Making a pull request

Follow [GitHub Flow][flow] and the [pull request template][pr-template]:

1. Create or find an issue when required; comment with your name and
   teammates. For a minor change without an issue, explain why in the PR.
1. Work on a descriptive branch in your fork and keep the change focused.
1. Add tests and documentation, then run the required checks.
1. Follow the [commit message standards](docs/COMMIT_MESSAGES.md), based on
   Conventional Commits 1.0.0, including body and breaking-change footers.
1. Push your branch and open a pull request targeting the master branch of
   GatorEducator/gatorgrader. Use a draft if work is incomplete.
1. Complete every applicable template field. Explain the problem, resulting
   behavior, compatibility changes, verification commands and results, and
   anything you could not test. List contributors and link every relevant
   issue. Use `Closes #123` only for an issue the PR fully resolves.
1. Keep the template's required release-classification statement, choosing
   small change, feature, compatibility breaking update, or non-versioned
   change as appropriate. Do not delete it as boilerplate.
1. Comment the PR URL on every linked issue, including later additions.
1. Respond to review feedback and rerun relevant checks after changes.

When reorganizing documentation, list moved or removed sections and their
new locations in the PR description. Preserve useful links and entry points;
adding a guide does not require deleting other documentation.

## Reviewing a pull request

Reviews are contributions too. Read the linked issue, description, and diff,
then check out the branch. With the [GitHub CLI][github-cli]:

```bash
gh pr checkout 123 --repo GatorEducator/gatorgrader
```

Save existing work before switching branches. Follow
[Base development environment](#base-development-environment) and
[CI environment and optional dependencies][ci-environment]
to set up the checkout, then run focused tests and required checks. Test
user-visible changes against a disposable assignment. Report commands,
results, OS, Python version, and anything you could not verify.

Submit a GitHub review: Comment, Approve, or Request changes. A favorable
conversation comment is not approval. Approve only changes you can endorse
based on your review and verification.

Address human and automated feedback. Verify suggestions; explain incorrect
ones with evidence. Summarize your updates and request another review.

## Merging and releasing

Before merge, required checks must pass and maintainers must review the PR.
Follow the review requirements shown on the PR.

Maintainers merge and publish releases. A merge does not mean a release is
immediately available; use the editable checkout until then. Publishing
workflows and detailed release procedures remain in maintainer documentation.

## Getting help and external resources

Ask change-specific questions in the issue or PR. For general help, search
existing issues before opening one. Report conduct concerns using the
contact in the [Code of Conduct](CODE_OF_CONDUCT.md).

- [Project README](README.md)
- [uv installation][uv-install]
- [uv project documentation][uv-projects]
- [Git documentation][git]
- [pytest documentation][pytest]
- [Conventional Commits 1.0.0][conventional-commits]
- [GitHub pull request reviews][rv]

These presentations explain the project's teaching goals and history; their
older Travis CI examples are not the current development setup:

- [A Hands-on Guide to Teaching Programming with GitHub, Travis CI, and Python][pyohio]
  (PyOhio 2018).
- [Using GitHub, Travis CI, and Python to Introduce Collaborative Software Development][pycon]
  (PyCon Education Summit 2018).
- [Using Python, Travis CI, and GitHub to Effectively Teach Programming][pygotham]
  (PyGotham 2018).

[bug-template]: .github/ISSUE_TEMPLATE/bug_report.md
[ci]: .github/workflows/main.yml
[ci-environment]: #ci-environment-and-optional-dependencies
[conventional-commits]: https://www.conventionalcommits.org/en/v1.0.0/
[example-check]: gator/checks/check_ConfirmFileExists.py
[example-tests]: tests/checks/test_check_ConfirmFileExists.py
[first]: https://github.com/GatorEducator/gatorgrader/labels/good-first-issue
[flow]: https://docs.github.com/en/get-started/using-github/github-flow
[gatorgrade-guide]: https://github.com/GatorEducator/gatorgrade#development
[git]: https://git-scm.com/doc
[github-cli]: https://cli.github.com/manual/gh_pr_checkout
[help-issues]: https://github.com/GatorEducator/gatorgrader/labels/help-wanted
[issues]: https://github.com/GatorEducator/gatorgrader/issues
[legacy-script]: https://github.com/GatorEducator/gatorgrader/issues/313
[mutation-issue]: https://github.com/GatorEducator/gatorgrader/issues/312
[new-issue]: https://github.com/GatorEducator/gatorgrader/issues/new/choose
[pr-template]: .github/pull_request_template.md
[pulls]: https://github.com/GatorEducator/gatorgrader/pulls
[pygotham]: https://speakerdeck.com/gkapfham/using-python-travis-ci-and-github-to-effectively-teach-programming
[pyohio]: https://speakerdeck.com/gkapfham/a-hands-on-guide-to-teaching-programming-with-github-travis-ci-and-python
[pycon]: https://speakerdeck.com/gkapfham/using-github-travis-ci-and-python-to-introduce-collaborative-software-development
[pytest]: https://docs.pytest.org/en/stable/
[repository]: https://github.com/GatorEducator/gatorgrader
[rv]: https://docs.github.com/pull-requests/reviewing-changes-in-pull-requests
[snoop]: https://github.com/alexmojaki/snoop
[uv-install]: https://docs.astral.sh/uv/getting-started/installation/
[uv-projects]: https://docs.astral.sh/uv/guides/projects/
