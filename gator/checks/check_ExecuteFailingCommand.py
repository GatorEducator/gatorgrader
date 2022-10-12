"""Check that a command executes with an expected error."""

import argparse

from gator import checkers
from gator import invoke

# import subprocess

def get_parser():
    """Get a parser for the arguments provided on the command-line."""
    # create the parser with the default help formatter
    # use a new description since this is a stand-alone check
    parser = argparse.ArgumentParser(
        prog="ExecuteFailingCommand",
        description="Check Provided by GatorGrader: ExecuteFailingCommand",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Required Named Checker Arguments {{{

    required_group = parser.add_argument_group("required checker arguments")

    # COMMAND: the command to execute
    # REQUIRED? Yes
    required_group.add_argument(
        "--command", type=str, help="command to execute", required=True
    )

    # }}}

    # Optional Named Checker Arguments {{{

    # None required for this checker

    # }}}
    return parser


def parse(args, parser=None):
    """Use the parser on the provided arguments."""
    return checkers.parse(get_parser, args, parser)


# pylint: disable=unused-argument
def act(main_parsed_arguments, check_remaining_arguments):
    """Perform the action for this check."""
    # extract the two arguments for this check:
    # --> command is required to specify the commit count threshold
    check_parsed_arguments = parse(check_remaining_arguments)
    # Directly run the check since at least one of the argument's for it is mandatory.
    # This means that the use of check_ExecuteCommand would have already failed by this
    # point since argparse will exit the program if a command-line argument is not provided
    command = check_parsed_arguments.command

    # # Run a command and return the output and error code.
    # process = subprocess.Popen(
    #     command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    # )
    # # run the command and return the results
    # output, error = process.communicate()
    # return_code = process.returncode

    # if process.returncode == 0:
    #     command = "commandWrong"
    # else:
    #     command = 'echo "CorrectCommand"'
    invocations = [invoke.invoke_all_command_executes_checks(command, inverse_check=True)]
    return invocations
