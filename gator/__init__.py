"""
Gatorgrader is an automated grading tool that checks the work of writers and programmers.

The gator package exposes the following functions:

    - grader_cli: Executes GatorGrader's command line interface to perform the requested check.
    - grader: given a list[str] in the format of GatorGrader command line arguments, performs the requested check and returns data about its success.

"""

# expose main_api entry point as "grader" function
from gator.orchestrate import main_api as grader  # noqa: F401

# expose main_cli entry point as "grader_cli" function
from gator.orchestrate import main_cli as grader_cli  # noqa: F401

# expose possible exceptions
from gator.exceptions import InvalidCheckArgumentsError  # noqa: F401
from gator.exceptions import InvalidSystemArgumentsError  # noqa: F401
from gator.exceptions import InvalidCheckError  # noqa: F401
