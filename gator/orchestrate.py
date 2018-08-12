"""Orchestrate the checks performed on writing and source code"""

import sys

from gator import arguments
from gator import display

DISPLAY = sys.modules["gator.display"]
ORCHESTRATE = sys.modules[__name__]

VOID = []

INCORRECT_ARGUMENTS = 2


def check_arguments(system_arguments):
    """Check the arguments returning the desired actions to perform"""
    # parse and verify the arguments
    actions = []
    gg_arguments = arguments.parse(system_arguments)
    did_verify_arguments = arguments.verify(gg_arguments)
    # incorrect arguments
    if did_verify_arguments is False:
        # still permitted to display messages
        if gg_arguments.nowelcome is not True:
            actions.append([DISPLAY, "welcome_message", VOID])
        # display incorrect arguments message
        actions.append([DISPLAY, "incorrect_message", VOID])
        actions.append([ORCHESTRATE, "exit", [INCORRECT_ARGUMENTS]])
    return actions


def perform(actions):
    """Perform the specified actions"""
    results = []
    for module, function, parameters in actions:
        function_to_invoke = getattr(module, function)
        # no parameters were specified, do not pass
        if parameters == []:
            function_result = function_to_invoke()
        # parameters were specified, do pass
        else:
            function_result = function_to_invoke(parameters)
        results.append(function_result)
    return results


def exit(exit_value):
    """Exit from the program using the provided exit value"""
    sys.exit(exit_value)


def check(system_arguments):
    """Orchestrate a full check of the specified deliverables"""
