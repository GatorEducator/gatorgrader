"""Display output for GatorGrader's command-line interface."""


def welcome_message():
    """Display a welcome message."""
    print()
    print("✔ GatorGrader: Automatically Check the Files of Programmers and Writers")
    print("https://github.com/GatorEducator/gatorgrader")
    print()


def checking_message():
    """Display the checking message."""
    print("Valid command-line arguments.")
    print("Running the specified checks!")
    print()


def incorrect_message():
    """Display a message for incorrect arguments."""
    print("Incorrect command-line arguments.")
    print()


def help_reminder():
    """Display a message to remind for the use of help."""
    print("Use --help to show details about GatorGrader's use.")
    print()


def message(requested_message):
    """Display any requested message and then a newline."""
    print(requested_message)
    print()


def line(message=""):
    """Display a newline."""
    print(message)
