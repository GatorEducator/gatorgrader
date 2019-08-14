"""Configuration file for the test suite."""

import os
import sys

import pytest

from contextlib import contextmanager

GO_BACK_A_DIRECTORY = "/../"

# set the system path to contain the previous directory
PREVIOUS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PREVIOUS_DIRECTORY + GO_BACK_A_DIRECTORY)


@pytest.fixture(scope="session")
def not_raises():
    """Delete the check that an exception is not raised during test execution."""

    @contextmanager
    def _not_raises(ExpectedException):
        """Define internal function to ensure that ExpectedException is not raised."""
        try:
            yield
        except ExpectedException as error:
            raise AssertionError(f"Raised exception {error} when it should not!")
        except Exception as error:
            raise AssertionError(f"An unexpected exception {error} raised.")

    return _not_raises
