"""Test cases for the run module"""

from gator import run


def test_run_command_returns_message():
    """Checks that a single line is returned from command """
    output, error = run.run_command('echo "Hello!"')
    assert error == b""
    assert output == b"Hello!\n"


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_run_command_grab_output_as_string(tmpdir):
    """Checks that invocation of comment counting check works correctly"""
    tmpdir.mkdir("Hello1")
    tmpdir.mkdir("Hello2")
    tmpdir.mkdir("Hello3")
    assert len(tmpdir.listdir()) == 3
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/"
    output = run.specified_command_get_output("ls " + directory)
    assert "Hello1" in output
    assert "Hello2" in output
    assert "Hello3" in output
