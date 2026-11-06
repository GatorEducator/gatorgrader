"""Test cases for the run module."""

import platform

import pytest

from gator import run

# define the operating systems on which to run processes
LINUX = "Linux"
MAC = "Darwin"
WINDOWS = "Windows"


class DistinctStr(str):
    """Equal to a str but never the same object."""


def expected_echo_output(system_name):
    """Return the output that echo makes on the given operating system."""
    # running an "echo" will have a trailing newline
    if system_name in (LINUX, MAC):
        return b"Hello!\n"
    # running an "echo" will have a carriage return and then trailing newline
    if system_name == WINDOWS:
        return b'"Hello!"\r\n'
    return None


def test_run_working_command_returns_message():
    """Check that a single line is returned from command ."""
    output, error, code = run.run_command('echo "Hello!"')
    assert error == b""
    assert output == expected_echo_output(platform.system())
    assert code == 0


@pytest.mark.parametrize(
    ("system_name", "output"),
    [
        (LINUX, b"Hello!\n"),
        (MAC, b"Hello!\n"),
        (WINDOWS, b'"Hello!"\r\n'),
    ],
)
def test_run_output_assertion_uses_value_comparison(
    monkeypatch, system_name, output
):
    """Check command output for equal but distinct operating system names."""
    distinct = DistinctStr(system_name)
    assert distinct == system_name
    assert distinct is not system_name
    monkeypatch.setattr(platform, "system", lambda: distinct)
    monkeypatch.setattr(run, "run_command", lambda command: (output, b"", 0))
    test_run_working_command_returns_message()

    # Incorrect output must fail rather than skip the operating system check.
    monkeypatch.setattr(
        run, "run_command", lambda command: (b"incorrect output", b"", 0)
    )
    with pytest.raises(AssertionError):
        test_run_working_command_returns_message()


def test_run_broken_command_returns_nonzero():
    """Check that a single line is returned from command ."""
    output, error, code = run.run_command("willnotwork")
    assert output == b""
    assert error != b""
    assert code != 0


def test_run_command_grab_output_as_string_correct_command(tmpdir):
    """Check that invocation of command produces correct captured output."""
    tmpdir.mkdir("Hello1")
    tmpdir.mkdir("Hello2")
    tmpdir.mkdir("Hello3")
    assert len(tmpdir.listdir()) == 3
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/"
    # note that this test case passes even when run in AppVeyor CI
    # thus suggesting that the ls command is supported on Windows
    output = run.specified_command_get_output("ls " + directory)
    assert "Hello1" in output
    assert "Hello2" in output
    assert "Hello3" in output


def test_run_command_grab_output_as_string_incorrect_command(tmpdir):
    """Check that invocation of command produces correct captured output."""
    tmpdir.mkdir("Hello1")
    tmpdir.mkdir("Hello2")
    tmpdir.mkdir("Hello3")
    assert len(tmpdir.listdir()) == 3
    directory = tmpdir.dirname + "/" + tmpdir.basename + "/"
    # this command will not work correctly because it does not exist
    # this means that it should not produce any output
    output = run.specified_command_get_output("gus " + directory)
    assert output == ""


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
