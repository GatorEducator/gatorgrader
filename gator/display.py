"""Display output for GatorGrader"""


def welcome_message():
    """Display a welcome message"""
    print()
    print("✔ GatorGrader: Automatically Check the Files of Programmers and Writers")
    print("https://github.com/GatorEducator/gatorgrader")
    print()


def checking_message():
    """Display the checking message"""
    print("Valid command-line arguments.")
    print("Running the specified checks!")
    print()


def incorrect_message():
    """Display a message for incorrect arguments"""
    print("Incorrect command-line arguments.")
    print()


def message(requested_message):
    """Display any requested message and then a newline"""
    print(requested_message)
    print()
