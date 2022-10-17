"""Configuration file for the test suite."""

import os
import sys

import pytest

from contextlib import contextmanager

from gator import checkers
from gator import report


GO_BACK_A_DIRECTORY = "/../"

# set the system path to contain the previous directory
PREVIOUS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PREVIOUS_DIRECTORY + GO_BACK_A_DIRECTORY)

# define four fixtures for use in the test suites
# --> load_checker
# --> load_check
# --> reset_results_dictionary
# --> not_raises


@pytest.fixture(scope="session")
def load_checker():  # noqa: D202
    """Load a checker using pluginbase."""

    def _load_checker(parsed_arguments):
        """Define internal function to load a checker using pluginbase."""
        external_checker_directory = checkers.get_checker_dir(parsed_arguments)
        checker_source = checkers.get_source([external_checker_directory])
        check_name = checkers.get_chosen_check(parsed_arguments)
        check_file = checkers.transform_check(check_name)
        check_exists = checkers.verify_check_existence(check_file, checker_source)
        return (check_exists, checker_source, check_file)

    return _load_checker


@pytest.fixture(scope="session")
def load_check():  # noqa: D202
    """Load a check using pluginbase."""

    def _load_check(parsed_arguments):
        """Define internal function to load a check using pluginbase."""
        external_checker_directory = checkers.get_checker_dir(parsed_arguments)
        checker_source = checkers.get_source([external_checker_directory])
        check_name = checkers.get_chosen_check(parsed_arguments)
        check_file = checkers.transform_check(check_name)
        assert checkers.verify_check_existence(check_file, checker_source) is True
        return checkers.load_check(checker_source, check_file)

    return _load_check


@pytest.fixture
def reset_results_dictionary():
    """Reset the state of the results dictionary."""
    report.reset()


@pytest.fixture(scope="session")
def not_raises():  # noqa: D202
    """Delete the check that an exception is not raised during test execution."""

    @contextmanager
    def _not_raises(ExpectedException):
        """Define internal function to ensure that ExpectedException is not raised."""
        try:
            yield
        except ExpectedException as error:
            raise AssertionError(
                f"Raised exception {error} when it should not!"
            ) from error
        except Exception as error:
            raise AssertionError(f"An unexpected exception {error} raised.") from error

    return _not_raises
