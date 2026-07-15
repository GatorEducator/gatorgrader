"""Display output for GatorGrader's command-line interface."""

from rich.console import Console

from gator.exceptions import (
    InvalidCheckArgumentsError,
    InvalidCheckError,
    InvalidSystemArgumentsError,
)

console = Console()


def welcome_message():
    """Display a welcome message."""
    console.print()
    console.print("✔ GatorGrader: Automatically Check the Files of Programmers and Writers")
    console.print("https://github.com/GatorEducator/gatorgrader")
    console.print()


def incorrect_system_arguments_message(error: InvalidSystemArgumentsError = None):
    """Display a message for incorrect arguments."""
    console.print("Incorrect command-line arguments.")
    if error and isinstance(error, InvalidCheckError):
        console.print(error.check_name + " is not a valid check.")
    console.print()


def incorrect_check_arguments_message(error: InvalidCheckArgumentsError = None):
    """Display a message for invalid check arguments."""
    console.print("Incorrect check arguments.")
    console.print()
    if error:
        console.print(error.error)
        console.print(error.usage)
        console.print()


def help_reminder():
    """Display a message to remind for the use of help."""
    console.print("Use gatorgrader --help to show details about GatorGrader's use.")
    console.print()


def message(requested_message):
    """Display any requested message and then a newline."""
    console.print(requested_message)
    console.print()


def line(message=""):
    """Display a newline."""
    console.print(message)
