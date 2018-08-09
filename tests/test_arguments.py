"""Tests for the input and checking of command-line arguments"""

import pytest

from gator import arguments

EMPTY_STRING = ""
ERROR = "error:"

VERIFIED = True
NOT_VERIFIED = False

# Region: Simple fixture-based Tests {{{


@pytest.fixture
def no_gg_args():
    """Return no command-line arguments"""
    return []


@pytest.fixture
def verifiable_gg_args():
    """Return arguments that are verifiable"""
    return ["--directory", "D", "--file", "a", "--exists"]


# pylint: disable=redefined-outer-name
def test_default_argument_values_correct(no_gg_args):
    """The default command-line arguments are correct"""
    gg_arguments = arguments.parse(no_gg_args)
    arguments_args_verified = arguments.verify(gg_arguments)
    assert arguments_args_verified == NOT_VERIFIED


# pylint: disable=redefined-outer-name
def test_arguments_verified(verifiable_gg_args):
    """Run arguments with verifiable arguments and it is verified"""
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
        (["--directory", "D", "--file", "f", "--singlecomments", "2", "--language", "JavaScript"]),
        (["--directory", "D", "--file", "f", "--multicomments", "2", "--language", "JavaScript"]),
    ],
)
def test_module_argument_not_verifiable_syserror(chosen_arguments, capsys):
    """Check that not valid arguments will not verify correctly"""
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
        (["--file", "f", "--directory", "D", "--multicomments", "2", "--executes"]),
        (["--file", "f", "--directory", "D", "--singlecomments", "2", "--executes"]),
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
    ],
)
def test_invalid_argument_combinations_not_accepted(chosen_arguments):
    """Check that not valid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.verify(parsed_arguments)
    assert verified_arguments is False


# }}}

# Region: Verified Arguments Tests for verify {{{


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--file", "f", "--exists"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--singlecomments", "2"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--multicomments", "2"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--paragraphs", "2"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--words", "100"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--sentences", "100"]),
        (["--nowelcome", "--command", "run", "--executes"]),
        (
            [
                "--nowelcome",
                "--command",
                "run",
                "--fragment",
                "hi",
                "--fragmentcount",
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
                "--fragment",
                "hi",
                "--fragmentcount",
                "2",
            ]
        ),
    ],
)
def test_valid_argument_combinations_accepted(chosen_arguments):
    """Check that valid argument combinations do verify correctly"""
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
                "--multicomments",
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
                "--singlecomments",
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
    """Check that not valid argument combinations do not verify correctly"""
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
    """Check that invalid argument combinations do not verify correctly"""
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
    """Check that invalid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_file_or_directory(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome"]),
        (["--nowelcome", "--directory", "D", "--singlecomments", "2"]),
        (["--nowelcome", "--directory", "D", "--multicomments", "1"]),
        (["--directory", "D", "--singlecomments", "2"]),
        (["--directory", "D", "--multicomments", "3"]),
        (["--nowelcome", "--file", "F", "--singlecomments", "1"]),
        (["--nowelcome", "--file", "F", "--multicomments", "2"]),
        (["--file", "F", "--singlecomments", "1"]),
        (["--file", "F", "--multicomments", "1"]),
        (["--directory", "D", "--file", "F", "--paragraphs", "1"]),
        (["--directory", "D", "--file", "F", "--words", "1"]),
    ],
)
def test_is_not_valid_file_not_valid_comments_wrong(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly"""
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
        (["--directory", "D", "--file", "F", "--singlecomments", "1"]),
        (["--directory", "D", "--file", "F", "--multicomments", "1"]),
        (["--directory", "D", "--file", "F", "--words", "1"]),
    ],
)
def test_is_not_valid_file_not_valid_paragraphs_wrong(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly"""
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
        (["--directory", "D", "--file", "F", "--singlecomments", "1"]),
        (["--directory", "D", "--file", "F", "--multicomments", "1"]),
        (["--directory", "D", "--file", "F", "--paragraphs", "1"]),
    ],
)
def test_is_not_valid_file_not_valid_words_wrong(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly"""
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
        (["--directory", "D", "--file", "F", "--fragment", "it", "--fragmentcount", "2", "--language", "Java"]),
        (["--directory", "D", "--file", "F", "--fragment", "it", "--fragmentcount", "2", "--language", "Python"]),
    ],
)
def test_is_not_valid_language_combinations_wrong(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_language(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--fragment", "it"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--fragmentcount", "2"]),
        (["--nowelcome", "--command", "run", "--fragment", "it"]),
        (["--nowelcome", "--command", "run", "--fragmentcount", "2"]),
    ],
)
def test_is_invalid_fragment_with_file_or_command(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_fragment(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--command", "run", "--paragraphs", "3"]),
        (["--nowelcome", "--command", "run", "--words", "3"]),
        (["--nowelcome", "--command", "run", "--singlecomments", "3"]),
        (["--nowelcome", "--command", "run", "--multicomments", "3"]),
    ],
)
def test_is_not_command_ancillary(chosen_arguments):
    """Check that file ancillary detection verifies correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    # note that this function is only checking for the presence
    # of the ancillary arguments like fragment and fragmentcount
    verified_arguments = arguments.is_command_ancillary(parsed_arguments)
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
    """Check that valid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_file_and_directory(parsed_arguments)
    assert verified_arguments is True
    verified_arguments = arguments.is_valid_file_or_directory(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--file", "f", "--singlecomments", "2"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--multicomments", "2"]),
        (["--nowelcome", "--file", "f", "--directory", "D", "--singlecomments", "2"]),
        (["--nowelcome", "--file", "f", "--directory", "D", "--multicomments", "2"]),
        (["--file", "f", "--directory", "D", "--singlecomments", "2"]),
        (["--file", "f", "--directory", "D", "--multicomments", "2"]),
        (["--directory", "D", "--file", "F", "--singlecomments", "2"]),
        (["--directory", "D", "--file", "F", "--multicomments", "2"]),
    ],
)
def test_is_valid_comments_valid(chosen_arguments):
    """Check that valid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_comments(parsed_arguments)
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
                "--singlecomments",
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
                "--multicomments",
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
                "--singlecomments",
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
                "--multicomments",
                "2",
                "--language",
                "Java",
            ]
        ),
        (
            [
                "--file",
                "f",
                "--directory",
                "D",
                "--singlecomments",
                "2",
                "--language",
                "Java",
            ]
        ),
        (
            [
                "--file",
                "f",
                "--directory",
                "D",
                "--multicomments",
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
                "--singlecomments",
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
                "--multicomments",
                "2",
                "--language",
                "Java",
            ]
        ),
    ],
)
def test_is_valid_comments_and_language_valid(chosen_arguments):
    """Check that valid argument combinations do not verify correctly"""
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
    """Check that valid argument combinations do not verify correctly"""
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
    """Check that valid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_words(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--command", "run", "--paragraphs", "3"]),
        (["--nowelcome", "--command", "run", "--words", "3"]),
        (["--nowelcome", "--command", "run", "--singlecomments", "3"]),
        (["--nowelcome", "--command", "run", "--multicomments", "3"]),
    ],
)
def test_is_file_ancillary(chosen_arguments):
    """Check that file ancillary detection verifies correctly"""
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
    """Check that file ancillary detection verifies correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    # note that this function is only checking for the presence
    # of the ancillary arguments like fragment and fragmentcount
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
                "--fragmentcount",
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
                "--fragmentcount",
                "2",
                "--fragment",
                "it",
            ]
        ),
        (
            [
                "--nowelcome",
                "--command",
                "run",
                "--fragment",
                "it",
                "--fragmentcount",
                "2",
            ]
        ),
        (
            [
                "--nowelcome",
                "--command",
                "run",
                "--fragmentcount",
                "2",
                "--fragment",
                "it",
            ]
        ),
    ],
)
def test_is_valid_fragment_with_file_or_command(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_fragment(parsed_arguments)
    assert verified_arguments is True


# }}}
