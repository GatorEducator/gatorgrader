"""Display output for GatorGrader's command-line interface."""

from gator.exceptions import (
    InvalidCheckError,
    InvalidSystemArgumentsError,
    InvalidCheckArgumentsError,
)


def welcome_message():
    """Display a welcome message."""
    print()
    print("✔ GatorGrader: Automatically Check the Files of Programmers and Writers")
    print("https://github.com/GatorEducator/gatorgrader")
    print()


def incorrect_system_arguments_message(error: InvalidSystemArgumentsError = None):
    """Display a message for incorrect arguments."""
    print("Incorrect command-line arguments.")
    if error and isinstance(error, InvalidCheckError):
        print(error.check_name + " is not a valid check.")
    print()


def incorrect_check_arguments_message(error: InvalidCheckArgumentsError = None):
    """Display a message for invalid check arguments."""
    print("Incorrect check arguments.")
    print()
    if error:
        print(error.message)
        print(error.usage)
        print()


def help_reminder():
    """Display a message to remind for the use of help."""
    print(f"Use gatorgrader --help to show details about GatorGrader's use.")
    print()


def message(requested_message):
    """Display any requested message and then a newline."""
    print(requested_message)
    print()


def line(message=""):
    """Display a newline."""
    print(message)
