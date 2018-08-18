"""Orchestrate the checks performed on writing and source code"""

import sys

from gator import arguments
from gator import display
from gator import leave
from gator import report

# pylint: disable=unused-import
from gator import invoke
from gator import run

DISPLAY = sys.modules["gator.display"]
INVOKE = sys.modules["gator.invoke"]
ORCHESTRATE = sys.modules[__name__]
RUN = sys.modules["gator.run"]

VOID = []

INCORRECT_ARGUMENTS = 2

SINGLE = "single-line"
MULTIPLE = "multiple-line"
REPOSITORY = "."


def check_arguments(system_arguments):
    """Check the arguments return the desired actions to perform"""
    # parse and verify the arguments
    actions = []
    gg_arguments = arguments.parse(system_arguments)
    # Action: display the welcome message
    if gg_arguments.nowelcome is not True:
        actions.append([DISPLAY, "welcome_message", VOID])
    did_verify_arguments = arguments.verify(gg_arguments)
    # arguments are incorrect
    if did_verify_arguments is False:
        # Action: display incorrect arguments message
        actions.append([DISPLAY, "incorrect_message", VOID])
        # Action: exit the program
        actions.append([RUN, "run_exit", [INCORRECT_ARGUMENTS]])
    return gg_arguments, actions


def check_commits(system_arguments):
    """Check the commits to the git repository and return desired actions"""
    actions = []
    if system_arguments.commits is not None:
        actions.append(
            [INVOKE, "invoke_commits_check", [REPOSITORY, system_arguments.commits]]
        )
    return actions


def check_exists(system_arguments):
    """Check the existence of a file in directory and return desired actions"""
    actions = []
    if system_arguments.exists is True:
        actions.append(
            [
                INVOKE,
                "invoke_file_in_directory_check",
                [system_arguments.file, system_arguments.directory],
            ]
        )
    return actions


def check_single(system_arguments):
    """Check the existence of single-line comments in a file and return desired actions"""
    actions = []
    if system_arguments.single is not None:
        actions.append(
            [
                INVOKE,
                "invoke_all_comment_checks",
                [
                    system_arguments.file,
                    system_arguments.directory,
                    system_arguments.single,
                    SINGLE,
                    system_arguments.language,
                ],
            ]
        )
    return actions


def check_multiple(system_arguments):
    """Check the existence of multiple-line comments in a file and return desired actions"""
    actions = []
    if system_arguments.multiple is not None:
        actions.append(
            [
                INVOKE,
                "invoke_all_comment_checks",
                [
                    system_arguments.file,
                    system_arguments.directory,
                    system_arguments.multiple,
                    MULTIPLE,
                    system_arguments.language,
                ],
            ]
        )
    return actions


def check_paragraphs(system_arguments):
    """Check the existence of paragraphs in a file and return desired actions"""
    actions = []
    if system_arguments.paragraphs is not None:
        actions.append(
            [
                INVOKE,
                "invoke_all_paragraph_checks",
                [
                    system_arguments.file,
                    system_arguments.directory,
                    system_arguments.paragraphs,
                ],
            ]
        )
    return actions


def check_words(system_arguments):
    """Check the existence of words in a file and return desired actions"""
    actions = []
    if system_arguments.words is not None:
        actions.append(
            [
                INVOKE,
                "invoke_all_word_count_checks",
                [
                    system_arguments.file,
                    system_arguments.directory,
                    system_arguments.words,
                ],
            ]
        )
    return actions


def perform(actions):
    """Perform the specified actions"""
    results = []
    # iteratively run all of the actions in the list
    for module, function, parameters in actions:
        function_to_invoke = getattr(module, function)
        # no parameters were specified, do not pass
        if parameters == []:
            function_result = function_to_invoke()
        # parameters were specified, do pass
        else:
            function_result = function_to_invoke(*parameters)
        results.append(function_result)
    return results


def check(system_arguments):
    """Orchestrate a full check of the specified deliverables"""
    # Section: Initialize
    # Only step: check the arguments
    step_results = []
    check_results = []
    gg_arguments, arguments_actions = check_arguments(system_arguments)
    step_results = perform(arguments_actions)
    check_results.extend(step_results)
    # Section: Perform one of these checks
    checks = [
        "check_commits",
        "check_exists",
        "check_single",
        "check_multiple",
        "check_paragraphs",
        "check_words",
    ]
    for a_check in checks:
        # create the checking function
        check_to_invoke = getattr(ORCHESTRATE, a_check)
        # call the checking function and get actions
        actions = check_to_invoke(gg_arguments)
        # perform the actions and get results
        step_results = perform(actions)
        # store the results from these actions
        check_results.extend(step_results)
    # Section: Output the report
    # Only step: get the report's details, produce the output, and display it
    output_list = report.output_list(report.get_details(), report.TEXT)
    produced_output = report.output(output_list)
    display.message(produced_output)
    # Section: Return control back to __main__ in gatorgrader
    # Only step: determine the correct exit code for the checks
    correct_exit_code = leave.get_code(check_results)
    return correct_exit_code
