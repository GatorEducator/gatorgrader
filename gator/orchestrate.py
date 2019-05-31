"""Orchestrate the checks performed on writing and source code"""

import sys

from gator import arguments
from gator import constants
from gator import display
from gator import leave
from gator import report

# pylint: disable=unused-import
from gator import invoke  # noqa: F401
from gator import run  # noqa: F401

# define the name of this module
ORCHESTRATE = sys.modules[__name__]

# define the modules that contain invokable functions
DISPLAY = sys.modules[constants.modules.Display]
INVOKE = sys.modules[constants.modules.Invoke]
RUN = sys.modules[constants.modules.Run]
REPORT = sys.modules[constants.modules.Report]

# define the formats for the output of the checks
OUTPUT_TYPE = getattr(REPORT, constants.outputs.Text)


def check_arguments(system_arguments):
    """Check the arguments return the desired actions to perform"""
    # parse and verify the arguments
    actions = []
    gg_arguments = arguments.parse(system_arguments)
    # Action: display the welcome message
    if gg_arguments.nowelcome is not True:
        actions.append([DISPLAY, "welcome_message", constants.arguments.Void])
    if gg_arguments.json is True:
        # pylint: disable=global-statement
        global OUTPUT_TYPE
        OUTPUT_TYPE = getattr(REPORT, constants.outputs.Json)
    did_verify_arguments = arguments.verify(gg_arguments)
    # arguments are incorrect
    if did_verify_arguments is False:
        # Action: display incorrect arguments message
        actions.append([DISPLAY, "incorrect_message", constants.arguments.Void])
        # Action: exit the program
        actions.append([RUN, "run_exit", [constants.arguments.Incorrect]])
    return gg_arguments, actions


def check_commits(system_arguments):
    """Check the commits to the git repository and return desired actions"""
    actions = []
    # the repository is the current directory contained work to check
    repository = constants.paths.Current_Directory
    if system_arguments.commits is not None:
        actions.append(
            [
                INVOKE,
                "invoke_commits_check",
                [repository, system_arguments.commits, system_arguments.exact],
            ]
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
                    constants.comments.Single_Line,
                    system_arguments.language,
                    system_arguments.exact,
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
                    constants.comments.Multiple_Line,
                    system_arguments.language,
                    system_arguments.exact,
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
                    system_arguments.exact,
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
                    system_arguments.exact,
                ],
            ]
        )
    return actions


def check_total_words(system_arguments):
    """Check the total word count in a file and return desired actions"""
    actions = []
    if system_arguments.total_words is not None:
        actions.append(
            [
                INVOKE,
                "invoke_all_total_word_count_checks",
                [
                    system_arguments.file,
                    system_arguments.directory,
                    system_arguments.total_words,
                    system_arguments.exact,
                ],
            ]
        )
    return actions


def check_fragment_file(system_arguments):
    """Check the existence of fragment in a file and return desired actions"""
    actions = []
    if system_arguments.fragment is not None and system_arguments.file is not None:
        actions.append(
            [
                INVOKE,
                "invoke_all_fragment_checks",
                [
                    system_arguments.fragment,
                    system_arguments.count,
                    system_arguments.file,
                    system_arguments.directory,
                    constants.markers.Nothing,
                    system_arguments.exact,
                ],
            ]
        )
    return actions


def check_regex_file(system_arguments):
    """Check the existence of regex in a file and return desired actions"""
    actions = []
    if system_arguments.regex is not None and system_arguments.file is not None:
        actions.append(
            [
                INVOKE,
                "invoke_all_regex_checks",
                [
                    system_arguments.regex,
                    system_arguments.count,
                    system_arguments.file,
                    system_arguments.directory,
                    constants.markers.Nothing,
                    system_arguments.exact,
                ],
            ]
        )
    return actions


def check_markdown_file(system_arguments):
    """Check the existence of markdown in a file and return desired actions"""
    actions = []
    if system_arguments.markdown is not None and system_arguments.file is not None:
        actions.append(
            [
                INVOKE,
                "invoke_all_markdown_checks",
                [
                    system_arguments.markdown,
                    system_arguments.count,
                    system_arguments.file,
                    system_arguments.directory,
                    system_arguments.exact,
                ],
            ]
        )
    return actions


def check_count_file(system_arguments):
    """Check the count of lines in a file and return desired actions"""
    actions = []
    # pylint: disable=bad-continuation
    if (
        system_arguments.count is not None
        and system_arguments.file is not None
        and system_arguments.fragment is None
        and system_arguments.regex is None
        and system_arguments.markdown is None
    ):
        actions.append(
            [
                INVOKE,
                "invoke_all_count_checks",
                [
                    system_arguments.count,
                    system_arguments.file,
                    system_arguments.directory,
                    constants.markers.Nothing,
                    system_arguments.exact,
                ],
            ]
        )
    return actions


def check_fragment_command(system_arguments):
    """Check the existence of fragment in a command's output and return desired actions"""
    actions = []
    if system_arguments.fragment is not None and system_arguments.command is not None:
        actions.append(
            [
                INVOKE,
                "invoke_all_command_fragment_checks",
                [
                    system_arguments.command,
                    system_arguments.fragment,
                    system_arguments.count,
                    system_arguments.exact,
                ],
            ]
        )
    return actions


def check_regex_command(system_arguments):
    """Check the existence of regex in a command's output and return desired actions"""
    actions = []
    if system_arguments.regex is not None and system_arguments.command is not None:
        actions.append(
            [
                INVOKE,
                "invoke_all_command_regex_checks",
                [
                    system_arguments.command,
                    system_arguments.regex,
                    system_arguments.count,
                    system_arguments.exact,
                ],
            ]
        )
    return actions


def check_count_command(system_arguments):
    """Check the count of lines in a command's output and return desired actions"""
    actions = []
    # pylint: disable=bad-continuation
    if (
        system_arguments.count is not None
        and system_arguments.command is not None
        and system_arguments.fragment is None
        and system_arguments.regex is None
    ):
        actions.append(
            [
                INVOKE,
                "invoke_all_command_count_checks",
                [
                    system_arguments.command,
                    system_arguments.count,
                    system_arguments.exact,
                ],
            ]
        )
    return actions


def check_executes_command(system_arguments):
    """Check whether or not a command executes without error and return desired actions"""
    actions = []
    # pylint: disable=bad-continuation
    if (
        system_arguments.command is not None
        and system_arguments.executes is not None
        and system_arguments.count is None
        and system_arguments.fragment is None
        and system_arguments.regex is None
    ):
        actions.append(
            [INVOKE, "invoke_all_command_executes_checks", [system_arguments.command]]
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
        "check_total_words",
        "check_markdown_file",
        "check_fragment_file",
        "check_fragment_command",
        "check_count_file",
        "check_count_command",
        "check_executes_command",
        "check_regex_file",
        "check_regex_command",
    ]
    # iterate through all of the possible checks
    for a_check in checks:
        # reflectively create the checking function
        check_to_invoke = getattr(ORCHESTRATE, a_check)
        # call the checking function and get actions
        actions = check_to_invoke(gg_arguments)
        # perform the actions and get results
        step_results = perform(actions)
        # store the results from these actions
        check_results.extend(step_results)
    # Section: Output the report
    # Only step: get the report's details, produce the output, and display it
    produced_output = report.output(report.get_result(), OUTPUT_TYPE)
    display.message(produced_output)
    # Section: Return control back to __main__ in gatorgrader
    # Only step: determine the correct exit code for the checks
    correct_exit_code = leave.get_code(check_results)
    return correct_exit_code
