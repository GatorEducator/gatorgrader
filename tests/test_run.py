"""Test cases for the run module"""

from gator import run


def test_run_command_returns_message():
    """Checks that a single line is returned from command """
    output, error = run.run_command('echo "Hello!"')
    assert error == b""
    assert output == b"Hello!\n"
