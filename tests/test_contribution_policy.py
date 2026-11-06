"""Exercise pull request policy acceptance and rejection."""

import json
import sys
from pathlib import Path

import pytest

from scripts import contribution_policy as policy

BASE = "master"
OTHER_BASE = "unexpected-branch"
BODY = """## Problem
The contribution workflow has gaps.
## Changes
Add deterministic validation.
## Compatibility
No CLI or configuration changes.
## Verification
uv run task all passed; coverage was not run locally.
## Contributors
@contributor
## Linked Issues
Refs #123
## AI Assistance
AI assistance: none
## Documentation Changes
Updated the contributor guide.
## Limitations
Live repository rules were not inspected.
"""
AI_USED = """AI assistance: used
Tool: coding assistant
Contribution: drafted validation tests
Verification: ran the focused pytest suite
"""
RELEASE = "This PR is a feature\n"
EVENT_NAME = "event.json"
ENCODING = "utf-8"
INVALID_JSON = "{"
EMPTY = ""
NEWLINE = "\n"
FAILURE = 1
ROOT_INDEX = 1
SUCCESS = 0


@pytest.mark.parametrize(
    "linked",
    [
        "Refs #123",
        "https://github.com/example/project/issues/123",
        "Minor-change exception: fix a documentation typo",
    ],
)
def test_validate_pull_request_accepts_documented_issue_options(
    linked: str,
) -> None:
    """Accept references and explained minor-change exceptions."""
    body = BODY.replace("Refs #123", linked)
    assert policy.validate_pull_request(body, BASE, BASE) == []


@pytest.mark.parametrize("heading", policy.REQUIRED_SECTIONS)
def test_validate_pull_request_rejects_missing_sections(heading: str) -> None:
    """Reject missing required fields independently."""
    body = NEWLINE.join(
        line for line in BODY.splitlines() if line.lower() != f"## {heading}"
    )
    assert policy.validate_pull_request(body, BASE, BASE)


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("Refs #123", "Closes #00"),
        ("Refs #123", "Minor-change exception: TODO"),
        ("@contributor", "@"),
        ("@contributor", "person@example.org"),
        ("AI assistance: none", "TBD"),
        ("AI assistance: none", "AI assistance: none\nAI assistance: used"),
        ("AI assistance: none", "<!-- AI assistance: none -->"),
        ("The contribution workflow has gaps.", "<!-- explain here -->"),
        ("Add deterministic validation.", "TODO"),
    ],
)
def test_validate_pull_request_rejects_placeholders(
    old: str, new: str
) -> None:
    """Reject unchanged template values and comments posing as evidence."""
    assert policy.validate_pull_request(BODY.replace(old, new), BASE, BASE)


def test_validate_pull_request_rejects_wrong_base() -> None:
    """Require the repository-specific target branch."""
    assert policy.validate_pull_request(BODY, OTHER_BASE, BASE)


def test_validate_pull_request_accepts_disclosed_assistance() -> None:
    """Accept assistance with tool, contribution, and verification details."""
    body = BODY.replace("AI assistance: none", AI_USED)
    assert policy.validate_pull_request(body, BASE, BASE) == []


@pytest.mark.parametrize("field", policy.AI_FIELDS)
def test_validate_pull_request_rejects_incomplete_assistance(
    field: str,
) -> None:
    """Require each declaration detail when assistance is acknowledged."""
    assistance = NEWLINE.join(
        line for line in AI_USED.splitlines() if not line.startswith(field)
    )
    body = BODY.replace("AI assistance: none", assistance)
    assert policy.validate_pull_request(body, BASE, BASE)


@pytest.mark.parametrize(
    "classification",
    [
        "small change",
        "feature",
        "compatibility breaking update",
        "non-versioned change",
    ],
)
def test_validate_pull_request_accepts_release_categories(
    classification: str,
) -> None:
    """Preserve every documented GatorGrader release category."""
    body = BODY + RELEASE.replace("feature", classification)
    assert policy.validate_pull_request(body, BASE, BASE, True) == []


def test_validate_pull_request_rejects_missing_release() -> None:
    """Reject omitted or commented-out required release statements."""
    body = BODY + f"<!-- {RELEASE} -->"
    assert policy.validate_pull_request(body, BASE, BASE, True)


def test_validate_pull_request_rejects_conflicting_categories() -> None:
    """Reject contradictory release classifications."""
    body = BODY + RELEASE + RELEASE.replace("feature", "small change")
    assert policy.validate_pull_request(body, BASE, BASE, True)


def test_default_template_requires_contributor_input() -> None:
    """Keep the unedited template from satisfying its own policy checks."""
    root = Path(__file__).resolve().parents[ROOT_INDEX]
    template = root / ".github" / "pull_request_template.md"
    assert policy.validate_pull_request(
        template.read_text(encoding=ENCODING), BASE, BASE, True
    )


def test_sections_ignores_headings_inside_fenced_examples() -> None:
    """Keep example headings from supplying missing real sections."""
    body = "```markdown\n" + BODY + "```\n"
    assert policy.sections(body) == {}
    assert policy.validate_pull_request(body, BASE, BASE)


@pytest.mark.parametrize("base", [BASE, OTHER_BASE])
def test_main_reads_event_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, base: str
) -> None:
    """Read event data as data and return the policy exit status."""
    event = tmp_path / EVENT_NAME
    event.write_text(
        json.dumps({"pull_request": {"body": BODY, "base": {"ref": base}}}),
        encoding=ENCODING,
    )
    monkeypatch.setattr(
        sys, "argv", ["policy", "--base", BASE, "--event-file", str(event)]
    )
    assert policy.main() == (SUCCESS if base == BASE else FAILURE)


@pytest.mark.parametrize("payload", [INVALID_JSON, "{}", "[]", "null"])
def test_main_rejects_malformed_events(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, payload: str
) -> None:
    """Fail closed on missing or malformed pull request payloads."""
    event = tmp_path / EVENT_NAME
    event.write_text(payload, encoding=ENCODING)
    monkeypatch.setenv(policy.EVENT_ENV, str(event))
    monkeypatch.setattr(sys, "argv", ["policy", "--base", BASE])
    assert policy.main() == FAILURE
