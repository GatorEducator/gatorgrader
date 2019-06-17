"""Test cases for the run module."""

import platform

from gator import run

# define the operating systems on which to run processes
LINUX = "Linux"
MAC = "Darwin"
WINDOWS = "Windows"


def test_run_working_command_returns_message():
    """Check that a single line is returned from command ."""
    output, error, code = run.run_command('echo "Hello!"')
    assert error == b""
    system_name = platform.system()
    # running an "echo" will have a trailing newline
    if system_name is LINUX or system_name is MAC:
        assert output == b"Hello!\n"
    # running an "echo" will have a carriage return and then trailing newline
    elif system_name is WINDOWS:
        assert output == b'"Hello!"\r\n'
    assert code == 0


def test_run_broken_command_returns_nonzero():
    """Check that a single line is returned from command ."""
    output, error, code = run.run_command("willnotwork")
    assert output == b""
    assert error != b""
    assert code != 0


def test_run_command_grab_output_as_string(tmpdir):
    """Check that invocation of command produces correct captured output."""
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
    """Check that invalid unicode bytestrings are handled correctly."""
    invalid_byte_sequence = b"\x80\x81"
    output = run.get_actual_output(invalid_byte_sequence)
    assert invalid_byte_sequence in output


def test_run_invalid_output_str():
    """Check that ouputs that are already strings are handled correctly."""
    randomString = "Hello"
    output = run.get_actual_output(randomString)
    assert randomString in output
