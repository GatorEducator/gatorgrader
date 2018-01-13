""" test cases for the gatorgrader_run module """

import gatorgrader_run


def test_run_command_returns_ls():
    """Checks that a single line is returned from command """
    output, error = gatorgrader_run.run_command("echo \"Hello!\"")
    assert error == b''
    assert output == b'Hello!\n'
