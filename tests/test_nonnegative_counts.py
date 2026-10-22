"""Reject invalid count thresholds consistently before running any checker."""

import importlib
import subprocess
import sys

import pytest

from gator.exceptions import InvalidCheckArgumentsError

FILE_ARGS = ["--file", "example.txt", "--directory", "."]
COUNT_CHECKS = [
    ("CountCommits", []),
    ("CountCommandOutput", ["--command", "echo example"]),
    ("CountFileLines", FILE_ARGS),
    ("CountFileParagraphs", FILE_ARGS),
    ("CountFileWords", FILE_ARGS),
    ("CountParagraphWords", FILE_ARGS),
    ("CountMarkdownTags", [*FILE_ARGS, "--tag", "paragraph"]),
    ("CountMultipleLineComments", [*FILE_ARGS, "--language", "Python"]),
    ("CountSingleLineComments", [*FILE_ARGS, "--language", "Python"]),
    ("MatchCommandFragment", ["--command", "echo TODO", "--fragment", "TODO"]),
    ("MatchCommandRegex", ["--command", "echo TODO", "--regex", "TODO"]),
    ("MatchFileFragment", [*FILE_ARGS, "--fragment", "TODO"]),
    ("MatchFileRegex", [*FILE_ARGS, "--regex", "TODO"]),
]


@pytest.mark.parametrize("name,required", COUNT_CHECKS)
@pytest.mark.parametrize("value", ["-1", "not-an-integer"])
def test_invalid_count_raises_normal_argument_error(name, required, value):
    """Negative and malformed thresholds cannot silently pass a check."""
    checker = importlib.import_module(f"gator.checks.check_{name}")
    with pytest.raises(InvalidCheckArgumentsError) as error:
        checker.parse([*required, "--count", value])
    assert error.value.check_name == name
    assert "--count" in error.value.error


@pytest.mark.parametrize("name,required", COUNT_CHECKS)
@pytest.mark.parametrize("value", ["0", "1"])
@pytest.mark.parametrize("exact", [False, True])
def test_nonnegative_counts_remain_valid(name, required, value, exact):
    """Zero and positive thresholds remain available in both comparison modes."""
    checker = importlib.import_module(f"gator.checks.check_{name}")
    args = [*required, "--count", value]
    if exact:
        args.append("--exact")
    parsed = checker.parse(args)
    assert parsed.count == int(value)
    assert parsed.exact is exact


@pytest.mark.parametrize("name,required", COUNT_CHECKS)
def test_count_help_documents_nonnegative_range(name, required):
    """Each count checker exposes the accepted range in its own help."""
    checker = importlib.import_module(f"gator.checks.check_{name}")
    assert "integer >= 0" in " ".join(
        checker.get_parser().format_help().split()
    )


def test_negative_count_cli_cannot_pass_a_missing_file(tmp_path):
    """Exercise the real CLI path from the reported false-positive example."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "gatorgrader",
            "CountFileLines",
            "--file",
            "missing.txt",
            "--directory",
            str(tmp_path),
            "--count",
            "-1",
            "--nowelcome",
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    assert result.returncode != 0
    assert "non-negative" in result.stdout + result.stderr
