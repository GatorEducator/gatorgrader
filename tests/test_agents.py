"""Guard essential agent instruction text without claiming behavioral enforcement."""

from pathlib import Path

import pytest

ROOT_INDEX = 1
AGENT_FILE = Path(__file__).resolve().parents[ROOT_INDEX] / "AGENTS.md"
ENCODING = "utf-8"
EMPTY = ""
SPACE = " "
LINE_BREAK = "\n"
CLAUSE_PARAMETER = "clause"
REQUIRED_CLAUSES = (
    "Before handoff or any authorized commit",
    "uv run task all",
    "pre-commit run --files",
    "Install only with developer authorization.",
    "notify-send",
    "osascript",
    "powershell.exe -NoProfile -ExecutionPolicy Bypass",
    "Import-Module BurntToast",
    "Install-Module -Name BurntToast -Scope CurrentUser",
    "inside Zellij",
    "does not replace the desktop notification.",
    "timeout 2 zellij pipe --",
    '"zjstatus::notify::Agent finished. This is really fun. "',
    "gator/",
    "tests/",
    "Use descriptive test_ names",
    "Tests must be independent",
    "work locally and in CI.",
    "function, statement, and branch coverage",
    "Never run `git stash`",
    "The software developer commits.",
    "Always create and follow a TODO list.",
)


def normalize_policy(text: str) -> str:
    """Ignore wrapping while retaining the required policy wording."""
    return SPACE.join(text.split())


def assert_agent_policy(text: str) -> None:
    """Reject removal of narrowly specified essential instruction text."""
    normalized = normalize_policy(text)
    for clause in REQUIRED_CLAUSES:
        assert normalize_policy(clause) in normalized, clause


def test_assert_agent_policy() -> None:
    """Accept the current instruction file with all essential clauses."""
    assert_agent_policy(AGENT_FILE.read_text(encoding=ENCODING))


@pytest.mark.parametrize(CLAUSE_PARAMETER, REQUIRED_CLAUSES)
def test_assert_agent_policy_rejects_removal(clause: str) -> None:
    """Reject a deleted clause and accept the original corrected document."""
    original = AGENT_FILE.read_text(encoding=ENCODING)
    changed = normalize_policy(original).replace(
        normalize_policy(clause), EMPTY
    )
    with pytest.raises(AssertionError):
        assert_agent_policy(changed)
    assert_agent_policy(original)


def test_normalize_policy() -> None:
    """Accept policy prose despite different line wrapping."""
    assert normalize_policy(LINE_BREAK.join(REQUIRED_CLAUSES)) == SPACE.join(
        map(normalize_policy, REQUIRED_CLAUSES)
    )
