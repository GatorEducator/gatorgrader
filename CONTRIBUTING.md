# Contributing to GatorGrader

Thank you for helping improve GatorGrader! Contributions include code,
documentation, tests, bug reports, and pull request reviews. Start with the
[README](README.md) to learn what the tool does.

This guide covers GatorGrader's checks for student writing and source code,
including its standalone CLI and check plugins. For GatorGrade's assignment
configuration, scoring, reports, history, or auto-hints, see the separate
[GatorGrade contributor documentation][gatorgrade-guide].

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Use of AI](#use-of-ai)
- [Finding ways to help](#finding-ways-to-help)
- [Raising an Issue](#raising-an-issue)
- [Project Standards](#project-standards)
   - [Development Environment](#development-environment)
   - [Running the edited checkout](#running-the-edited-checkout)
   - [Coding and check plugins](#coding-and-check-plugins)
   - [Automated Testing](#automated-testing)
   - [Test Coverage](#test-coverage)
   - [Code Linting](#code-linting)
   - [Continuous Integration](#continuous-integration)
   - [Program Debugging](#program-debugging)
   - [Contributor scripts](#contributor-scripts)
- [Making a Pull Request](#making-a-pull-request)
- [Reviewing, merging, and releasing](#reviewing-merging-and-releasing)
- [External Resources](#external-resources)

## Code of Conduct

Follow the [Code of Conduct](CODE_OF_CONDUCT.md) in all project interactions.
Report conduct concerns to [@gkapfham](https://github.com/gkapfham).

## Use of AI

You are responsible for reviewing and testing AI-assisted code,
documentation, and communication for accuracy, safety, and respectful language.
Review output before submitting it; only claim verification you performed.

Disclose substantial AI assistance in contributions and project communication.
In affected commits, describe what the tool contributed and how you verified
it in the body, and add an `AI-Assisted: <tool name>` trailer.

## Finding ways to help

Browse the [issue tracker][issues] and [open pull requests][pulls]. Look for
the [good-first-issue][first] and [help-wanted][help-wanted] labels. You can
also improve an example, report a reproducible bug, strengthen a regression
test, or review a pull request. Read related discussions and coordinate
overlapping work in the issue comments.

## Raising an Issue

Proposed changes normally need an issue. Decide case by case whether a minor
change, such as a typo or small documentation fix, needs a separate issue.
If you proceed without one, explain the scope and reason in the PR. Ask a
maintainer when uncertain.

Search existing issues and pull requests for duplicates, then
[open an issue][new] when needed. Choose the bug report or feature request
template and complete its prompts. The [bug report template][bug-template]
asks for reproduction steps, expected behavior, and environment details.
Keep those details in the issue rather than scattering them across
conversations. For other changes, describe the problem, proposed scope,
and how the result can be verified. Remove credentials and private student
or assignment data from examples.

When working on an issue, comment before starting to identify yourself and
any teammates working on it. Broader design discussion in the issue comments is
encouraged but optional. Make small, focused changes that reviewers can
understand and verify.

If you discover another problem while working, check for duplicates and
create an issue if needed, even when your pull request is already open.
Link related work and keep the current pull request focused.

Every pull request must link any relevant issues. Comment the PR URL on
**each linked issue**, including issues linked after the PR opens. Use a
closing keyword only when the PR resolves an issue; use a reference for
partial or related
work. Agents must prepare drafts unless explicitly authorized to publish
issues or comments.

## Project Standards

### Development Environment

Install [Git][git] and [uv][uv-install]. Package metadata requires Python
`>=3.10,<4.0`; CI currently tests Python 3.10 through 3.14. Use uv for
dependency management, virtual environments, and project commands.

Fork [GatorEducator/gatorgrader][repository] on GitHub, then replace
YOUR-USERNAME with your username:

```bash
git clone https://github.com/YOUR-USERNAME/gatorgrader.git
cd gatorgrader
git remote add upstream https://github.com/GatorEducator/gatorgrader.git
git switch -c docs/contributor-guide
uv sync
uv run task hooks-install
uv run gatorgrader --help
```

Choose a branch name that describes your issue. Submit the PR from your fork
to the upstream repository's master branch.

The sync command creates the environment, installs development dependencies
from the default dev group, and installs this checkout in editable mode.
Python source edits are available on the next run without reinstalling.
Run sync again after dependency or package metadata changes, and keep
dependency and lockfile updates together. GatorGrader has no auto-hint extra;
that feature belongs to GatorGrade.

Install hooks in every new clone. They check staged changes and commit
messages; PR titles need no prefix. See [local checks](docs/PRE_COMMIT.md)
for setup, full checks, and the isolated hook smoke tests.

To select another supported interpreter, run:

```bash
uv python pin 3.12
uv sync
uv run task test
```

This changes the local Python pin. Review pin-file changes before including
them in your PR; use the CI matrix to verify the other supported platforms.

### Running the edited checkout

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

Replace the project path with your checkout's absolute path and quote it if
it contains spaces. The uv project option selects the editable environment
while preserving the assignment as the working directory. This check should
pass with exit code 0. Remove the disposable example file and rerun it; the
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

### Coding and check plugins

- Keep source in gator/ with the CLI entry in gatorgrader.py; mirror the
  source structure in tests/ and place check tests in tests/checks/.
- Follow Ruff formatting and import ordering, with a Python line
  length of 79. Soft-wrap Markdown near 80 columns where practical.
- Add module and function docstrings and preserve the established style in
  edited files. Use meaningful names, snake_case functions and variables,
  PascalCase classes, and UPPER_SNAKE_CASE module constants where used.
- Group top-level imports as standard library, third-party, then local
  absolute imports such as `from gator import checkers`. Avoid wildcards.
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

Preserve CLI flags, check names and arguments, external-plugin contracts,
result and diagnostic behavior, and JSON output unless your issue calls for
a compatibility change. Explain intended breaking changes and migration
steps in the PR. Maintain behavior across the Python and OS versions in CI.
There is no configured static type-checking task; do not present an
unconfigured checker as a required gate. GatorGrade's separate type-checking,
comment-case, Pydantic, and blanket literal-extraction rules do not apply here.

### Automated Testing

Run focused tests while developing, then the complete verification gate
before submitting or updating a PR:

```bash
uv run pytest tests/checks/test_check_ConfirmFileExists.py
uv run task all
```

The all task runs lint, test, and cover, in that order. The test task runs
pytest with stop-on-first-failure enabled. Useful commands are:

| Purpose | Command |
| --- | --- |
| Required combined gate | `uv run task all` |
| Tests | `uv run task test` |
| Statement and branch coverage | `uv run task cover` |
| All Python linters | `uv run task lint` |
| Check formatting | `uv run task format-check` |
| Rewrite formatting | `uv run task format` |

Name tests descriptively with a test_ prefix; group and order related cases
for readability. Keep tests independent and runnable locally and in CI.
Follow existing pytest parametrization patterns. Add or update tests for
new behavior and regression cases, including failure paths. Use temporary
filesystem fixtures and reset shared report state with the
reset_results_dictionary fixture where appropriate. Test literals may improve
readability and are permitted by Ruff's PLR2004 exception. Do not remove
failing tests to make the suite pass.

### Test Coverage

Maintain 100% statement and branch coverage where possible. If complete
coverage is not possible, explain the uncovered behavior in the PR. The
configured minimum is 99% on gator/, with branch coverage enabled. Do not
lower the threshold or game coverage to pass.

```bash
uv run task cover
```

The test-coverage task is an alias for cover. A successful all run already
includes this coverage check; no extra coverage invocation is required.

### Code Linting

Ruff checks snake_case function names and absolute imports. Pytest rejects
unregistered markers instead of treating them as warnings.

Ruff checks formatting, imports, docstrings, and other Python conventions.
Its selected rule families are E, D, I, F, PL, Q, RUF, W, and T201, with
D203, D213, and E501 ignored. Broad exception handlers are rejected by Ruff.
Bandit checks security patterns; Radon reports
complexity and maintainability; Xenon enforces complexity thresholds.

```bash
uv run task lint
```

Individual tasks are lint-ruff, lint-ruff-format, lint-bandit,
lint-radon-cc, lint-radon-mi, and lint-xenon; run each with uv run task.
The format task **modifies files**; format-check and lint-ruff-format only
check them. Review formatter diffs before including them in your PR.

### Continuous Integration

[GitHub Actions][ci] runs Python linting and coverage on Ubuntu for Python
3.10–3.14, and tests on Linux, macOS, and Windows for those versions. A
separate job checks Markdown using markdownlint and the [.mdlrc](.mdlrc)
configuration. Markdown linting is not part of uv run task all, and no
Markdown task is configured in taskipy.

Run the local checks and inspect the PR's CI results. Record failures and
environment limitations accurately rather than claiming unrun checks passed.
Update the README, examples, docstrings, and this guide when the behavior or
contributor workflow they describe changes.

### Program Debugging

Start with the smallest failing test or disposable assignment. Use
`uv run pytest -x --pdb` to enter the debugger on a test failure, or use
[Snoop][snoop], which is installed with development dependencies. For a
temporary trace, add `import snoop` and decorate the target function with
`@snoop.snoop`. Remove debugging code before submitting the PR.

For manual verification, record the working directory, input files, exact
command, expected and actual output, exit code, OS, and Python version.
Exercise both passing and failing behavior where relevant, including JSON
output if the change affects reports. Remove private data from shared logs.

### Contributor scripts

[scripts/tasks.py](scripts/tasks.py) is a legacy Invoke/pyenv helper around
the same test and cover tasks. It is not required for development. Its
default Python 3.7.3 is outside the current supported range, its wording
still mentions Pipenv, and Invoke is not a declared dependency. It also
changes the local Python selection. Use uv directly as shown above while
[issue #313][legacy-script] tracks whether to fix or retire it.

There are no GatorGrade comment/version/direct-test checkers or mutation
helpers in this repository. Mutation-testing support is separate work in
[issue #312][mutation-issue].

## Making a Pull Request

Follow [GitHub Flow][flow] and the [PR template][pr-template]:

1. Find or open an issue when required; comment with your name and teammates.
   For a minor change without an issue, explain why in the PR.
1. Work on a descriptive branch in your fork and keep the change focused.
1. Add tests and documentation, then run uv run task all.
1. Follow the [commit message standards](docs/COMMIT_MESSAGES.md), based on
   Conventional Commits 1.0.0, including body and breaking-change footers.
1. Push the branch and open a PR targeting GatorEducator/gatorgrader's
   master branch; use a draft if work is incomplete.
1. Complete every applicable template field. Explain the problem, resulting
   behavior, compatibility changes, verification commands and results, and
   anything you could not test. List all contributors and linked issues.
1. Keep the template's required release-classification statement, choosing
   small change, feature, compatibility breaking update, or non-versioned
   change as appropriate. Do not delete it as boilerplate.
1. Comment the PR URL on every linked issue, including later additions.
1. Respond to feedback and rerun relevant checks after changes.

When consolidating documentation, identify moved or removed sections and
their replacement destinations in the PR description. Keep useful links and
entry points discoverable; adding a guide does not itself require deleting
other documentation files.

## Reviewing, merging, and releasing

Review the linked issue, description, and diff, then check out the proposed
branch and run uv sync, relevant tests, and uv run task all. Save existing
work before switching branches. Verify user-visible changes against a
disposable assignment and report the environment and results.

Submit a formal GitHub review using Comment, Approve, or Request changes.
A favorable conversation comment is not an approval. Authors should address
human and automated review feedback, explain disagreements with evidence,
and request another review when ready.

Before merge, required checks must pass and maintainers must review the PR.
Follow the review requirements shown on the PR. Maintainers handle merging
and releases; a merge does not guarantee immediate package availability.
Keep using the editable checkout to test changes before a release. The
publishing workflow and operational release instructions remain separate.

## External Resources

Ask change-specific questions in the relevant issue or PR so others can find
the discussion. For general help, search existing issues before opening one.

- [GatorGrader README](README.md)
- [uv installation][uv-install] and [project documentation][uv-projects]
- [Git documentation][git]
- [pytest documentation][pytest]
- [Conventional Commits 1.0.0][commits]
- [GitHub pull request reviews][reviews]

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
[commits]: https://www.conventionalcommits.org/en/v1.0.0/
[example-check]: gator/checks/check_ConfirmFileExists.py
[example-tests]: tests/checks/test_check_ConfirmFileExists.py
[first]: https://github.com/GatorEducator/gatorgrader/labels/good-first-issue
[flow]: https://docs.github.com/en/get-started/using-github/github-flow
[gatorgrade-guide]: https://github.com/GatorEducator/gatorgrade#development
[git]: https://git-scm.com/doc
[help-wanted]: https://github.com/GatorEducator/gatorgrader/labels/help-wanted
[issues]: https://github.com/GatorEducator/gatorgrader/issues
[legacy-script]: https://github.com/GatorEducator/gatorgrader/issues/313
[mutation-issue]: https://github.com/GatorEducator/gatorgrader/issues/312
[new]: https://github.com/GatorEducator/gatorgrader/issues/new/choose
[pr-template]: .github/pull_request_template.md
[pulls]: https://github.com/GatorEducator/gatorgrader/pulls
[pygotham]: https://speakerdeck.com/gkapfham/using-python-travis-ci-and-github-to-effectively-teach-programming
[pyohio]: https://speakerdeck.com/gkapfham/a-hands-on-guide-to-teaching-programming-with-github-travis-ci-and-python
[pycon]: https://speakerdeck.com/gkapfham/using-github-travis-ci-and-python-to-introduce-collaborative-software-development
[pytest]: https://docs.pytest.org/en/stable/
[repository]: https://github.com/GatorEducator/gatorgrader
[reviews]: https://docs.github.com/pull-requests/reviewing-changes-in-pull-requests
[snoop]: https://github.com/alexmojaki/snoop
[uv-install]: https://docs.astral.sh/uv/getting-started/installation/
[uv-projects]: https://docs.astral.sh/uv/guides/projects/
