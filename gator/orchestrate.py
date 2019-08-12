"""Orchestrate the preliminary actions and checks performed on writing and source code."""

import sys

from gator import arguments
from gator import checkers
from gator import constants

# from gator import leave
# from gator import report

# pylint: disable=unused-import
from gator import display  # noqa: F401
from gator import invoke  # noqa: F401
from gator import run  # noqa: F401

import snoop

snoop.install(color="rrt")

# define the name of this module
ORCHESTRATE = sys.modules[__name__]

# define the modules that contain invokable functions
DISPLAY = sys.modules[constants.modules.Display]
INVOKE = sys.modules[constants.modules.Invoke]
RUN = sys.modules[constants.modules.Run]
REPORT = sys.modules[constants.modules.Report]

# define the format for the output of the checks
OUTPUT_TYPE = getattr(REPORT, constants.outputs.Text)


def parse_verify_arguments(system_arguments):
    """Parse, verify and then return the parsed command-line arguments."""
    # parse the command-line arguments
    parsed_arguments = arguments.parse(system_arguments)
    # verify the command-line arguments
    did_verify_arguments = arguments.verify(parsed_arguments)
    return parsed_arguments, did_verify_arguments


def get_actions(parsed_arguments, verification_status):
    """Get the actions to perform before running any specified checker."""
    needed_actions = []
    # Needed Action: display the welcome message
    if parsed_arguments.nowelcome is not True:
        needed_actions.append([DISPLAY, "welcome_message", constants.arguments.Void])
    # Needed Action: configure to produce JSON output for external interface
    if parsed_arguments.json is True:
        # pylint: disable=global-statement
        global OUTPUT_TYPE
        OUTPUT_TYPE = getattr(REPORT, constants.outputs.Json)
    # arguments were not verified, create actions for error message display and an exit
    if verification_status is False:
        # Needed Action: display incorrect arguments message
        needed_actions.append([DISPLAY, "incorrect_message", constants.arguments.Void])
        # Needed Action: exit the program
        needed_actions.append([RUN, "run_exit", [constants.arguments.Incorrect]])
    return needed_actions


def perform_actions(actions):
    """Perform the specified actions."""
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


def check_commits(system_arguments):
    """Check the commits to the git repository and return desired actions."""
    actions = []
    # the repository is the current directory containing work to check
    if system_arguments.commits is not None:
        actions.append(
            [
                INVOKE,
                "invoke_commits_check",
                [
                    constants.paths.Current_Directory,
                    system_arguments.commits,
                    system_arguments.exact,
                ],
            ]
        )
    return actions


def check_exists(system_arguments):
    """Check the existence of a file in directory and return desired actions."""
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
    """Check the existence of single-line comments in a file and return desired actions."""
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
    """Check the existence of multiple-line comments in a file and return desired actions."""
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
    """Check the existence of paragraphs in a file and return desired actions."""
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
    """Check the existence of minimum words across a file and return desired actions."""
    actions = []
    if system_arguments.words is not None:
        actions.append(
            [
                INVOKE,
                "invoke_all_minimum_word_count_checks",
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
    """Check the total word count in a file and return desired actions."""
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
    """Check the existence of fragment in a file and return desired actions."""
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
    """Check the existence of regex in a file and return desired actions."""
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
    """Check the existence of markdown in a file and return desired actions."""
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
    """Check the count of lines in a file and return desired actions."""
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
    """Check the existence of fragment in a command's output and return desired actions."""
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
    """Check the existence of regex in a command's output and return desired actions."""
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
    """Check the count of lines in a command's output and return desired actions."""
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
    """Check whether or not a command executes without error and return desired actions."""
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


@snoop
def check(system_arguments):
    """Orchestrate a full check of the specified deliverables."""
    # Section: Initialize
    # step_results = []
    # check_results = []
    # Step: Parse and then verify the arguments
    parsed_arguments, verification_status = parse_verify_arguments(system_arguments)
    # Step: Get and perform the preliminary actions before running a checker
    # if the arguments did not parse or verify correctly, then:
    # --> argparse will cause the program to crash with an error OR
    # --> one of the actions will be to print the help message and exist
    actions = get_actions(parsed_arguments, verification_status)
    perform_actions(actions)
    # Step: Get the source of all the checkers available from either:
    # --> the internal directory of checkers (e.g., "./gator/checks")
    # --> the directory specified on the command-line
    external_checker_directory = checkers.get_checker_dir(parsed_arguments)
    checker_source = checkers.get_source([external_checker_directory])
    # Step: Get and transform the name of the chosen checker and
    # then prepare for running it by ensuring that it is:
    # --> available for use (i.e., pluginbase found and loaded it)
    check = checkers.get_chosen_check(parsed_arguments)
    check_file = checkers.transform_check(check)
    checker_exists = checkers.verify_check_existence(check_file, checker_source)

    # check_results.extend(step_results)
    # # Section: Perform one of these checks
    # # Note that GatorGrader only performs a single check
    # # The Gradle plugin can run multiple GatorGrader checks in parallel
    # # Make new checks available by adding them to this list of check names
    # checks = [
    #     "check_commits",
    #     "check_exists",
    #     "check_single",
    #     "check_multiple",
    #     "check_paragraphs",
    #     "check_words",
    #     "check_total_words",
    #     "check_markdown_file",
    #     "check_fragment_file",
    #     "check_fragment_command",
    #     "check_count_file",
    #     "check_count_command",
    #     "check_executes_command",
    #     "check_regex_file",
    #     "check_regex_command",
    # ]
    # # iterate through all of the possible checks
    # # each check:
    # # --> is a string of a name of a check function
    # # --> is called reflectively through the getattr function
    # # --> will only result in actions if the arguments signal to call it
    # for a_check in checks:
    #     # reflectively create the checking function
    #     check_to_invoke = getattr(ORCHESTRATE, a_check)
    #     # call the checking function and get actions
    #     actions = check_to_invoke(gg_arguments)
    #     # perform the actions and get results
    #     step_results = perform(actions)
    #     # store the results from these actions
    #     check_results.extend(step_results)
    # # Section: Output the report
    # # Only step: get the report's details, produce the output, and display it
    # produced_output = report.output(report.get_result(), OUTPUT_TYPE)
    # display.message(produced_output)
    # # Section: Return control back to __main__ in gatorgrader
    # # Only step: determine the correct exit code for the checks
    # correct_exit_code = leave.get_code(check_results)
    # return correct_exit_code
