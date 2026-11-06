"""Validate mechanically checkable pull request requirements."""

import argparse
import json
import os
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = (
    "problem",
    "changes",
    "compatibility",
    "verification",
    "contributors",
    "linked issues",
    "ai assistance",
    "documentation changes",
    "limitations",
)
COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)
HEADING_PATTERN = re.compile(r"^## ([^#].*?)\s*#*\s*$")
PLACEHOLDER_PATTERN = re.compile(r"(?:todo|tbd|your title|@|#0+)", re.I)
ISSUE_PATTERN = re.compile(
    r"(?<![\w/])#[1-9]\d*\b|"
    r"https://github\.com/[^\s/]+/[^\s/]+/issues/[1-9]\d*\b"
)
EXCEPTION_PATTERN = re.compile(
    r"^Minor-change exception:\s*(\S.*)$", re.M | re.I
)
CONTRIBUTOR_PATTERN = re.compile(
    r"(?<![\w.+-])@[a-z\d](?:[a-z\d-]{0,38})\b", re.I
)
AI_PATTERN = re.compile(r"^AI assistance: (none|used)\s*$", re.M | re.I)
RELEASE_PATTERN = re.compile(
    r"^This PR is a (small change|feature|compatibility breaking update|"
    r"non-versioned change)\.?\s*$",
    re.M,
)
AI_FIELDS = ("Tool", "Contribution", "Verification")
EMPTY = ""
NEWLINE = "\n"
FENCES = ("```", "~~~")
HEADING_GROUP = 1
DECLARATION_COUNT = 1
FIRST_INDEX = 0
BODY_KEY = "body"
BASE_KEY = "base"
REF_KEY = "ref"
PR_KEY = "pull_request"
EVENT_ENV = "GITHUB_EVENT_PATH"
EVENT_ARGUMENT = "--event-file"
BASE_ARGUMENT = "--base"
RELEASE_ARGUMENT = "--require-release"
SUCCESS = 0
FAILURE = 1


def sections(body: str) -> dict[str, str]:
    """Read level-two sections without treating fenced examples as headings."""
    contents: dict[str, list[str]] = {}
    heading = EMPTY
    fence = EMPTY
    for line in COMMENT_PATTERN.sub(EMPTY, body).splitlines():
        stripped = line.strip()
        if fence:
            if stripped.startswith(fence):
                fence = EMPTY
        elif stripped.startswith(FENCES):
            fence = stripped[: len(FENCES[FIRST_INDEX])]
        elif match := HEADING_PATTERN.fullmatch(line):
            heading = match.group(HEADING_GROUP).strip().lower()
            contents.setdefault(heading, [])
            continue
        if heading:
            contents[heading].append(line)
    return {
        heading: NEWLINE.join(lines).strip()
        for heading, lines in contents.items()
    }


def has_content(text: str) -> bool:
    """Reject empty sections and unchanged placeholder values."""
    return bool(text.strip()) and not PLACEHOLDER_PATTERN.fullmatch(
        text.strip()
    )


def validate_pull_request(
    body: str,
    base: str,
    expected_base: str,
    require_release: bool = False,
) -> list[str]:
    """Return actionable errors without judging the truth of declarations."""
    errors = []
    contents = sections(body)
    if base != expected_base:
        errors.append(f"Target branch must be {expected_base}.")
    for heading in REQUIRED_SECTIONS:
        if not has_content(contents.get(heading, EMPTY)):
            errors.append(f"Complete the '{heading}' section.")
    linked = contents.get("linked issues", EMPTY)
    exception = EXCEPTION_PATTERN.search(linked)
    if not ISSUE_PATTERN.search(linked) and not (
        exception and has_content(exception.group(HEADING_GROUP))
    ):
        errors.append("Link an issue or explain a Minor-change exception:.")
    if not CONTRIBUTOR_PATTERN.search(contents.get("contributors", EMPTY)):
        errors.append("List contributors using their GitHub @usernames.")
    assistance = contents.get("ai assistance", EMPTY)
    declarations = AI_PATTERN.findall(assistance)
    if len(declarations) != DECLARATION_COUNT:
        errors.append(
            "Declare 'AI assistance: none' or 'AI assistance: used'."
        )
    elif declarations[FIRST_INDEX].lower() == "used":
        for field in AI_FIELDS:
            value = re.search(rf"^{field}:\s*(\S.*)$", assistance, re.M)
            if value is None or not has_content(value.group(HEADING_GROUP)):
                errors.append(f"Explain AI assistance in '{field}:'.")
    clean_body = COMMENT_PATTERN.sub(EMPTY, body)
    classifications = RELEASE_PATTERN.findall(clean_body)
    if require_release and len(classifications) != DECLARATION_COUNT:
        errors.append(
            "Keep a valid 'This PR is a ...' release classification."
        )
    return errors


def main() -> int:
    """Check a GitHub event file without interpolating its untrusted contents."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(BASE_ARGUMENT, required=True)
    parser.add_argument(RELEASE_ARGUMENT, action="store_true")
    parser.add_argument(EVENT_ARGUMENT, default=os.environ.get(EVENT_ENV))
    arguments = parser.parse_args()
    if arguments.event_file is None:
        parser.error("Supply --event-file or GITHUB_EVENT_PATH.")
    try:
        event = json.loads(Path(arguments.event_file).read_text())
        pull_request = event[PR_KEY]
        body = pull_request[BODY_KEY] or EMPTY
        base = pull_request[BASE_KEY][REF_KEY]
        if not isinstance(body, str) or not isinstance(base, str):
            raise ValueError("Pull request body and base must be strings.")
    except (OSError, ValueError, KeyError, TypeError):
        sys.stderr.write("Cannot read a valid pull request event.\n")
        return FAILURE
    errors = validate_pull_request(
        body, base, arguments.base, arguments.require_release
    )
    if errors:
        sys.stderr.write(NEWLINE.join(errors) + NEWLINE)
        return FAILURE
    return SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())
