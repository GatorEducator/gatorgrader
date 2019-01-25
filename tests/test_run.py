"""Test cases for the run module"""

from gator import run


def test_run_working_command_returns_message():
    """Checks that a single line is returned from command """
    output, error, code = run.run_command('echo "Hello!"')
    assert error == b""
    assert output == b"Hello!\n"
    assert code == 0


def test_run_broken_command_returns_nonzero():
    """Checks that a single line is returned from command """
    output, error, code = run.run_command("willnotwork")
    assert output == b""
    assert error != b""
    assert code != 0


# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
def test_run_command_grab_output_as_string(tmpdir):
    """Checks that invocation of command produces correct captured output"""
    tmpdir.mkdir("Hello1")
    tmpdir.mkdir("Hello2")
    tmpdir.mkdir("Hello3")
    assert len(tmpdir.listdir()) == 3
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/"
    output = run.specified_command_get_output("ls " + directory)
    assert "Hello1" in output
    assert "Hello2" in output
    assert "Hello3" in output

def test_run_invalid_output():
    """ Checks that is handles invalid ouput"""
    invalid_byte_sequence=b'\x80\x81'
    output = run.get_actual_output(invalid_byte_sequence)
    print(output)
    assert invalid_byte_sequence in output
