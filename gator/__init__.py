"""Gator package initilization."""

# expose main_api entry point as "grader" function
from gator.orchestrate import main_api as grader  # noqa: F401
from gator.orchestrate import InvalidSystemArgumentsError  # noqa: F401
from gator.orchestrate import InvalidCheckError  # noqa: F401
