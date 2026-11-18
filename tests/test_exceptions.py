"""Tests for the exception classes provided by GatorGrader."""


from gator.exceptions import InvalidCheckArgumentsError


def test_invalid_check_arguments_error_with_message():
    """Ensure that the error stores a provided message."""
    error = InvalidCheckArgumentsError(
        ["--file", "hello.py"],
        "usage: CountFileLines",
        "the following arguments are required: --count",
        "CountFileLines",
    )
    assert error.error == "the following arguments are required: --count"
    assert error.check_name == "CountFileLines"


def test_invalid_check_arguments_error_without_message():
    """Ensure that the error can be created without a message."""
    error = InvalidCheckArgumentsError(
        ["--file", "hello.py"],
        "usage: CountFileLines",
        None,
        "CountFileLines",
    )
    assert error.error is None
    assert error.check_name == "CountFileLines"
