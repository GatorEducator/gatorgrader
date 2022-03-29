"""Orchestrate the preliminary actions and checks performed on writing and source code."""

import sys
from typing import List

from gator import arguments
from gator import checkers
from gator import constants
from gator import description
from gator import leave
from gator import report
from gator import display
from gator import run

from gator.exceptions import (
    InvalidSystemArgumentsError,
    InvalidCheckArgumentsError,
    InvalidCheckError,
)

# define the name of this module
ORCHESTRATE = sys.modules[__name__]

# define the modules that contain invokable functions
REPORT = sys.modules[constants.modules.Report]

# define the format for the output of the checks
OUTPUT_TYPE = getattr(REPORT, constants.outputs.Text)


def main_cli(system_arguments):
    """Orchestrate a full execution of the specified check."""
    passed = False
    try:
        # Execute the pipeline
        passed = perform_check(*perform_system_configuration(system_arguments))
        # Produce the output
        produced_output = report.output(report.get_result(), OUTPUT_TYPE)
        # Display the output
        display.message(produced_output)
    except InvalidSystemArgumentsError as error:
        # Display the incorrect arguments message
        display.incorrect_system_arguments_message(error)
        display.help_reminder()
        run.run_exit(constants.arguments.Incorrect)
    except InvalidCheckArgumentsError as error:
        # Display the invalid check message
        display.incorrect_check_arguments_message(error)
        display.help_reminder(error.check_name)
        run.run_exit(constants.arguments.Incorrect)
    # Section: Return control back to __main__ in gatorgrader
    # Only step: determine the correct exit code for the checks
    correct_exit_code = leave.get_code(passed)
    return correct_exit_code


def main_api(system_arguments: List[str]):
    """Execute the specified check.

    Args:
        system_arguments: The command-line arguments to be used.

    Returns:
        (description, passed, diagnostic): The description of the check, whether the check passed, and the diagnostic of the check.
    """
    perform_check(*perform_system_configuration(["--nowelcome"] + system_arguments))
    return report.decompose_result(report.get_result())


def perform_system_configuration(system_arguments):
    """Parse the specified command-line arguments and perform system configuration, validation, and welcoming."""
    parsed_arguments, remaining_arguments = arguments.parse(system_arguments)
    # Display the welcome message if the user did not specify the --nowelcome flag
    if parsed_arguments.nowelcome is not True:
        display.welcome_message()
    # Report if the system arguments are not valid
    if arguments.verify(parsed_arguments) is False:
        raise InvalidSystemArgumentsError(parsed_arguments)

    # Configure the output type to be JSON if the user specified the --json flag
    if parsed_arguments.json is True:
        # pylint: disable=global-statement
        global OUTPUT_TYPE
        OUTPUT_TYPE = getattr(REPORT, constants.outputs.Json)
    return parsed_arguments, remaining_arguments


def perform_check(parsed_arguments, remaining_arguments):
    """Perform the check specified in the given parsed arguments."""
    # Get the source of all the checkers available from either:
    # - the internal directory of checkers (e.g., "./gator/checks")
    # - the directory specified on the command-line
    external_checker_directory = checkers.get_checker_dir(parsed_arguments)
    checker_source = checkers.get_source([external_checker_directory])
    # Get and transform the name of the chosen checker and
    # then prepare for running it by ensuring that it is available for use
    # (i.e., pluginbase found and loaded it)
    check_name = checkers.get_chosen_check(parsed_arguments)
    check_file = checkers.transform_check(check_name)
    check_exists = checkers.verify_check_existence(check_file, checker_source)
    # Load the check and verify that it is valid:
    check_verified = False
    check = None
    if check_exists:
        check = checkers.load_check(checker_source, check_file)
        check_verified = checkers.verify_check_functions(check)
    # Report if the check is not valid
    if not check_exists or not check_verified:
        raise InvalidCheckError(parsed_arguments, check_name)
    # Perform the check
    passed = check.act(parsed_arguments, remaining_arguments)
    # parse a list of the check's output to
    # Override the result's description if needed
    # TODO: this line uses pass-by-reference, and should be refactored at some point for clarity
    description.transform_result_dictionary(parsed_arguments, report.get_result())
    return passed
