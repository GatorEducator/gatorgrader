"""Configuration file for the test suite."""

import os
import sys

from contextlib import contextmanager

GO_BACK_A_DIRECTORY = "/../"

# set the system path to contain the previous directory
PREVIOUS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PREVIOUS_DIRECTORY + GO_BACK_A_DIRECTORY)


@contextmanager
def not_raises(ExpectedException):
    """Ensure that a function is not raised during test execution."""
    try:
        yield
    except ExpectedException as error:
        raise AssertionError(f"Raised exception {error} when it should not!")
    except Exception as error:
        raise AssertionError(f"An unexpected exception {error} raised.")
