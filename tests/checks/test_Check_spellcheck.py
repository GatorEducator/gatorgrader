"""File to ensure the check spellcheck file is correct."""

import pytest

from gator import spelling
from gator.checks import check_spellcheck


def test_no_arguments_incorrect_system_exit(capsys):
    """Ensure that the appropriate output is provided when no arguments are inputted."""
    with pytest.raises(SystemExit):
        _ = check_spellcheck.parse([])
    captured = capsys.readouterr()
    # there is no standard output
    counted_newlines = captured.out.count("\n")
    assert counted_newlines == 0
    # standard error has two lines from pytest
    assert "usage:" in captured.err
    counted_newlines = captured.err.count("\n")
    assert counted_newlines == 3


@pytest.mark.parameterize(
    "commandline_arguments",
    [ 
        (["--file"],
        (["--fileWRONG", "filename"])

        ),
    ],
)
def test_required_commandline_arguments_cannot_parse():
    """Check that all required command line arguments are used."""


def test_required_commandline_arguments_can_parse():
    """Check that all required command line arguments are used."""


def test_optional_commandline_arguments_cannot_parse():
    """Check that all optional arguments are used correctly."""


def test_optional_commandline_arguments_can_parse():
    """Check that all optional arguments are used correctly."""


def test_optional_commandline_arguments_can_parse_created_parser(
    commandline_arguments, not_raises
):


def test_act_produces_output():
    """ """


def test_act_produces_output_complex_regex():
    """ """
