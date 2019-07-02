"""Tests for the input and checking of command-line arguments."""

import pytest

from gator import arguments

EMPTY_STRING = ""
ERROR = "error:"

VERIFIED = True
NOT_VERIFIED = False

# Region: Simple fixture-based Tests {{{


@pytest.fixture
def no_gg_args():
    """Return no command-line arguments."""
    return []


@pytest.fixture
def verifiable_gg_args():
    """Return arguments that are verifiable."""
    return ["--directory", "D", "--file", "a", "--exists"]


# pylint: disable=redefined-outer-name
def test_default_argument_values_correct(no_gg_args):
    """The default command-line arguments are correct."""
    gg_arguments = arguments.parse(no_gg_args)
    arguments_args_verified = arguments.verify(gg_arguments)
    assert arguments_args_verified == NOT_VERIFIED


# pylint: disable=redefined-outer-name
def test_arguments_verified(verifiable_gg_args):
    """Run arguments with verifiable arguments and it is verified."""
    gg_arguments = arguments.parse(verifiable_gg_args)
    gg_args_verified = arguments.verify(gg_arguments)
    assert gg_args_verified == VERIFIED


# }}}

# Region: Incorrect Arguments Tests {{{


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--directoryy", "D"]),
        (["--directory", "D", "F"]),
        (["--filles", "F"]),
        (["--file", "m", "f"]),
        (["-file", "f"]),
        (["-directory", "D"]),
        (
            [
                "--directory",
                "D",
                "--file",
                "f",
                "--single",
                "2",
                "--language",
                "JavaScript",
            ]
        ),
        (
            [
                "--directory",
                "D",
                "--file",
                "f",
                "--multiple",
                "2",
                "--language",
                "JavaScript",
            ]
        ),
    ],
)
def test_module_argument_not_verifiable_syserror(chosen_arguments, capsys):
    """Check that not valid arguments will not verify correctly.."""
    with pytest.raises(SystemExit):
        arguments.parse(chosen_arguments)
    standard_out, standard_err = capsys.readouterr()
    assert standard_out is EMPTY_STRING
    assert ERROR in standard_err


# }}}

# Region: Not Verified Arguments Tests for verify {{{


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome"]),
        (["--nowelcome", "--directory", "D"]),
        (["--directory", "D"]),
        (["--nowelcome", "--file", "f"]),
        (["--file", "F"]),
        (["--command", "run this command", "--file", "f"]),
        (["--command", "run this command", "--file", "f", "--directory", "D"]),
        (["--file", "f", "--directory", "D", "--executes"]),
        (["--file", "f", "--directory", "D", "--multiple", "2"]),
        (["--file", "f", "--directory", "D", "--single", "2"]),
        (["--file", "f", "--directory", "D", "--multiple", "2", "--executes"]),
        (["--file", "f", "--directory", "D", "--single", "2", "--executes"]),
        (["--file", "f", "--directory", "D", "--total-words", "2", "--words", "4"]),
        (["--file", "f", "--directory", "D", "--words", "2", "--total-words", "4"]),
        (["--nowelcome", "--command", "run", "--paragraphs", "3"]),
        (["--nowelcome", "--command", "run", "--paragraphs", "3", "--executes"]),
        (
            [
                "--command",
                "run this command",
                "--file",
                "f",
                "--directory",
                "D",
                "--executes",
            ]
        ),
        (["--file", "f", "--directory", "D", "--executes"]),
        (["--directory", "D", "--executes"]),
        (["--file", "f", "--executes"]),
        (["--file", "f", "--directory", "D", "--commits", "10"]),
        (["--command", "run", "--executes", "--commits", "10"]),
        (["--directory", "D", "--count", "10"]),
        (["--file", "f", "--count", "10"]),
        (["--command", "run", "--executes", "--count", "10"]),
    ],
)
def test_invalid_argument_combinations_not_accepted(chosen_arguments):
    """Check that not valid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.verify(parsed_arguments)
    assert verified_arguments is False


# }}}

# Region: Verified Arguments Tests for verify {{{


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--file", "f", "--exists"]),
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--single",
                "2",
                "--language",
                "Java",
            ]
        ),
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--single",
                "2",
                "--language",
                "Java",
            ]
        ),
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--multiple",
                "2",
                "--language",
                "Java",
            ]
        ),
        (["--nowelcome", "--directory", "D", "--file", "f", "--paragraphs", "2"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--words", "100"]),
        (["--nowelcome", "--command", "run", "--executes"]),
        (["--nowelcome", "--command", "run", "--fragment", "hi", "--count", "2"]),
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--fragment",
                "hi",
                "--count",
                "2",
            ]
        ),
        (["--nowelcome", "--commits", "10"]),
        (["--commits", "10"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--count", "2"]),
        (["--nowelcome", "--command", "run", "--count", "2"]),
    ],
)
def test_valid_argument_combinations_accepted(chosen_arguments):
    """Check that valid argument combinations do verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.verify(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--file", "f"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--command", "run"]),
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--multiple",
                "2",
                "--command",
                "run",
            ]
        ),
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--single",
                "2",
                "--command",
                "run",
            ]
        ),
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--paragraphs",
                "2",
                "--command",
                "run",
            ]
        ),
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--words",
                "2",
                "--command",
                "run",
            ]
        ),
    ],
)
def test_invalid_argument_combinations_accepted(chosen_arguments):
    """Check that not valid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.verify(parsed_arguments)
    assert verified_arguments is False


# }}}

# Region: Not Verified Arguments Tests for helper functions {{{


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D"]),
        (["--directory", "D"]),
        (["--nowelcome", "--file", "F"]),
        (["--file", "F"]),
    ],
)
def test_is_valid_file_not_valid(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_file_and_directory(parsed_arguments)
    assert verified_arguments is False
    verified_arguments = arguments.is_valid_file_or_directory(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--command", "run"]),
        (["--paragraphs", "4"]),
        (["--nowelcome", "--words", "5"]),
        (["--command", "run"]),
    ],
)
def test_is_valid_file_or_directory_not_valid(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_file_or_directory(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome"]),
        (["--nowelcome", "--directory", "D", "--single", "2"]),
        (["--nowelcome", "--directory", "D", "--multiple", "1"]),
        (["--directory", "D", "--single", "2"]),
        (["--directory", "D", "--multiple", "3"]),
        (["--nowelcome", "--file", "F", "--single", "1"]),
        (["--nowelcome", "--file", "F", "--multiple", "2"]),
        (["--file", "F", "--single", "1"]),
        (["--file", "F", "--multiple", "1"]),
        (["--directory", "D", "--file", "F", "--paragraphs", "1"]),
        (["--directory", "D", "--file", "F", "--words", "1"]),
    ],
)
def test_is_not_valid_file_not_valid_comments_wrong(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_comments(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome"]),
        (["--nowelcome", "--directory", "D", "--paragraphs", "2"]),
        (["--directory", "D", "--paragraphs", "2"]),
        (["--nowelcome", "--file", "F", "--paragraphs", "1"]),
        (["--file", "F", "--paragraphs", "1"]),
        (["--directory", "D", "--file", "F", "--single", "1"]),
        (["--directory", "D", "--file", "F", "--multiple", "1"]),
        (["--directory", "D", "--file", "F", "--words", "1"]),
    ],
)
def test_is_not_valid_file_not_valid_paragraphs_wrong(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_paragraphs(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome"]),
        (["--nowelcome", "--directory", "D", "--words", "2"]),
        (["--directory", "D", "--words", "2"]),
        (["--nowelcome", "--file", "F", "--words", "1"]),
        (["--file", "F", "--words", "1"]),
        (["--directory", "D", "--file", "F", "--single", "1"]),
        (["--directory", "D", "--file", "F", "--multiple", "1"]),
        (["--directory", "D", "--file", "F", "--paragraphs", "1"]),
    ],
)
def test_is_not_valid_file_not_valid_words_wrong(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_words(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--language", "Java"]),
        (["--nowelcome", "--directory", "D", "--language", "Python"]),
        (["--directory", "D", "--language", "Java"]),
        (["--directory", "D", "--language", "Python"]),
        (["--nowelcome", "--file", "F", "--language", "Java"]),
        (["--nowelcome", "--file", "F", "--language", "Python"]),
        (["--file", "F", "--language", "Java"]),
        (["--file", "F", "--language", "Python"]),
        (["--directory", "D", "--file", "F", "--language", "Java"]),
        (["--directory", "D", "--file", "F", "--language", "Python"]),
        (
            [
                "--directory",
                "D",
                "--file",
                "F",
                "--fragment",
                "it",
                "--count",
                "2",
                "--language",
                "Java",
            ]
        ),
        (
            [
                "--directory",
                "D",
                "--file",
                "F",
                "--fragment",
                "it",
                "--count",
                "2",
                "--language",
                "Python",
            ]
        ),
    ],
)
def test_is_not_valid_language_combinations_wrong(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_language(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--fragment", "it"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--count", "2"]),
        (["--nowelcome", "--directory", "D", "--fragment", "it", "--count", "2"]),
        (["--nowelcome", "--file", "f", "--fragment", "it", "--count", "2"]),
        (["--nowelcome", "--command", "run", "--fragment", "it"]),
        (["--nowelcome", "--command", "run", "--count", "2"]),
    ],
)
def test_is_invalid_fragment_with_file_or_command(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_fragment(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome"]),
        (["--nowelcome", "--directory", "D", "--count", "2"]),
        (["--nowelcome", "--file", "f", "--count", "2"]),
        (["--nowelcome", "--command", "run", "--fragment", "2"]),
        (["--nowelcome", "--command", "run", "--fragment", "2", "--count", "2"]),
    ],
)
def test_is_invalid_count_with_file_or_command(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_count(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--command", "run", "--paragraphs", "3"]),
        (["--nowelcome", "--command", "run", "--words", "3"]),
        (["--nowelcome", "--command", "run", "--single", "3"]),
        (["--nowelcome", "--command", "run", "--multiple", "3"]),
    ],
)
def test_is_not_command_ancillary(chosen_arguments):
    """Check that file ancillary detection verifies correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    # note that this function is only checking for the presence
    # of the ancillary arguments like fragment and count
    verified_arguments = arguments.is_command_ancillary(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [(["--nowelcome", "--directory", "D", "--single", "2", "--exact"])],
)
def test_exact_count_check_not_valid(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_exact(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [(["--nowelcome", "--directory", "D", "--file", "f", "--words", "50"])],
)
def test_exact_count_check_is_not_valid_cover_branch(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_exact(parsed_arguments)
    assert verified_arguments is False


# }}}

# Region: Verified Arguments Tests for helper functions {{{


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--file", "f"]),
        (["--nowelcome", "--file", "f", "--directory", "D"]),
        (["--file", "f", "--directory", "D"]),
        (["--directory", "D", "--file", "F"]),
    ],
)
def test_is_valid_file_valid(chosen_arguments):
    """Check that valid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_file_and_directory(parsed_arguments)
    assert verified_arguments is True
    verified_arguments = arguments.is_valid_file_or_directory(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--file", "f", "--single", "2"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--multiple", "2"]),
        (["--nowelcome", "--file", "f", "--directory", "D", "--single", "2"]),
        (["--nowelcome", "--file", "f", "--directory", "D", "--multiple", "2"]),
        (["--file", "f", "--directory", "D", "--single", "2"]),
        (["--file", "f", "--directory", "D", "--multiple", "2"]),
        (["--directory", "D", "--file", "F", "--single", "2"]),
        (["--directory", "D", "--file", "F", "--multiple", "2"]),
    ],
)
def test_is_valid_comments_valid(chosen_arguments):
    """Check that valid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_comments(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--file", "f", "--exists"]),
        (["--nowelcome", "--file", "f", "--directory", "D", "--exists"]),
        (["--file", "f", "--directory", "D", "--exists"]),
        (["--directory", "D", "--file", "F", "--exists"]),
    ],
)
def test_is_valid_exists(chosen_arguments):
    """Check that valid argument combinations do verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_exists(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--file", "f", "--exists"]),
        (["--nowelcome", "--directory", "D", "--exists"]),
        (["--file", "f", "--exists"]),
        (["--directory", "D", "--exists"]),
    ],
)
def test_is_not_valid_exists(chosen_arguments):
    """Check that valid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_exists(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--command", "C", "--executes"]),
        (["--command", "C", "--executes"]),
    ],
)
def test_is_valid_executes(chosen_arguments):
    """Check that valid argument combinations do verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_executes(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [(["--nowelcome", "--file", "f", "--executes"]), (["--file", "f", "--executes"])],
)
def test_is_not_valid_executes(chosen_arguments):
    """Check that valid argument combinations do verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_executes(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--single",
                "2",
                "--language",
                "Java",
            ]
        ),
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--multiple",
                "2",
                "--language",
                "Java",
            ]
        ),
        (
            [
                "--nowelcome",
                "--file",
                "f",
                "--directory",
                "D",
                "--single",
                "2",
                "--language",
                "Java",
            ]
        ),
        (
            [
                "--nowelcome",
                "--file",
                "f",
                "--directory",
                "D",
                "--multiple",
                "2",
                "--language",
                "Java",
            ]
        ),
        (["--file", "f", "--directory", "D", "--single", "2", "--language", "Java"]),
        (["--file", "f", "--directory", "D", "--multiple", "2", "--language", "Java"]),
        (["--directory", "D", "--file", "F", "--single", "2", "--language", "Java"]),
        (["--directory", "D", "--file", "F", "--multiple", "2", "--language", "Java"]),
    ],
)
def test_is_valid_comments_and_language_valid(chosen_arguments):
    """Check that valid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_language(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--file", "f", "--paragraphs", "2"]),
        (["--nowelcome", "--file", "f", "--directory", "D", "--paragraphs", "2"]),
        (["--file", "f", "--directory", "D", "--paragraphs", "2"]),
        (["--directory", "D", "--file", "F", "--paragraphs", "2"]),
    ],
)
def test_is_valid_paragraphs_valid(chosen_arguments):
    """Check that valid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_paragraphs(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--file", "f", "--words", "2"]),
        (["--nowelcome", "--file", "f", "--directory", "D", "--words", "2"]),
        (["--file", "f", "--directory", "D", "--words", "2"]),
        (["--directory", "D", "--file", "F", "--words", "2"]),
    ],
)
def test_is_valid_words_valid(chosen_arguments):
    """Check that valid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_words(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments,validity",
    [
        (
            ["--nowelcome", "--directory", "D", "--file", "f", "--total-words", "2"],
            True,
        ),
        (
            ["--nowelcome", "--file", "f", "--directory", "D", "--total-words", "2"],
            True,
        ),
        (["--file", "f", "--directory", "D", "--total-words", "2"], True),
        (["--directory", "D", "--file", "F", "--total-words", "2"], True),
        (["--nowelcome"], False),
        (["--nowelcome", "--directory", "D", "--total-words", "2"], False),
        (["--directory", "D", "--total-words", "2"], False),
        (["--nowelcome", "--file", "F", "--total-words", "1"], False),
        (["--file", "F", "--total-words", "1"], False),
        (["--directory", "D", "--file", "F", "--single", "1"], False),
        (["--directory", "D", "--file", "F", "--multiple", "1"], False),
        (["--directory", "D", "--file", "F", "--paragraphs", "1"], False),
        # This is true, but should be false after verify() since words will also be true
        (
            ["--directory", "D", "--file", "F", "--total-words", "4", "--words", "2"],
            True,
        ),
        (
            ["--directory", "D", "--file", "F", "--words", "4", "--total-words", "2"],
            True,
        ),
    ],
)
def test_is_valid_total_words(chosen_arguments, validity):
    """Check that valid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_total_words(parsed_arguments)
    assert verified_arguments is validity


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--command", "run", "--paragraphs", "3"]),
        (["--nowelcome", "--command", "run", "--words", "3"]),
        (["--nowelcome", "--command", "run", "--single", "3"]),
        (["--nowelcome", "--command", "run", "--multiple", "3"]),
    ],
)
def test_is_file_ancillary(chosen_arguments):
    """Check that file ancillary detection verifies correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    # note that this function is only checking for the presence
    # of the ancillary arguments like paragraphs or words
    verified_arguments = arguments.is_file_ancillary(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--command", "run", "--executes"]),
        (["--command", "run", "--executes"]),
    ],
)
def test_is_command_ancillary(chosen_arguments):
    """Check that file ancillary detection verifies correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    # note that this function is only checking for the presence
    # of the ancillary arguments like fragment and count
    verified_arguments = arguments.is_command_ancillary(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--fragment",
                "it",
                "--count",
                "2",
            ]
        ),
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--count",
                "2",
                "--fragment",
                "it",
            ]
        ),
        (["--nowelcome", "--command", "run", "--fragment", "it", "--count", "2"]),
        (["--nowelcome", "--command", "run", "--count", "2", "--fragment", "it"]),
    ],
)
def test_is_valid_fragment_with_file_or_command(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_fragment(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--file", "f", "--count", "2"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--count", "2"]),
        (["--nowelcome", "--command", "run", "--count", "2"]),
    ],
)
def test_is_valid_count_with_file_or_command(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_count(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--commits", "2", "--exact"]),
        (["--nowelcome", "--exact", "--commits", "2"]),
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--single",
                "2",
                "--exact",
            ]
        ),
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--multiple",
                "2",
                "--exact",
            ]
        ),
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--paragraphs",
                "2",
                "--exact",
            ]
        ),
        (["--nowelcome", "--directory", "D", "--file", "f", "--words", "2", "--exact"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--count", "2", "--exact"]),
        (
            [
                "--nowelcome",
                "--directory",
                "D",
                "--file",
                "f",
                "--fragment",
                "GatorGrader",
                "--count",
                "2",
                "--exact",
            ]
        ),
        (
            [
                "--nowelcome",
                "--command",
                "ls",
                "--fragment",
                "GatorGrader",
                "--count",
                "2",
                "--exact",
            ]
        ),
    ],
)
def test_exact_count_check_valid(chosen_arguments):
    """Check that invalid argument combinations do verify correctly."""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_exact(parsed_arguments)
    assert verified_arguments is True


# }}}
