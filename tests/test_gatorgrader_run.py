""" test cases for the gatorgrader_exit module """

import gatorgrader_run


def test_run_command_returns_ls(tmpdir):
    """Checks that code fails"""
    output, error = gatorgrader_run.run_command("echo \"Hello!\"")
    assert error == b''
    assert output == b'Hello!\n'
