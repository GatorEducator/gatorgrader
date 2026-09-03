"""Tests for the loading, verification, and use of plugin-based checkers."""

import os
import sys
from unittest.mock import patch

import pytest

from gator import arguments, checkers, plugin


@pytest.fixture(autouse=True)
def reset_checker_source():
    """Before running any test in this suite always reset the source of the checkers in pluginbase."""
    # note that performing this reset ensures test independence and
    # avoids test flakiness for single-test runs or different test orderings
    checkers.reset_source()


def test_reset_checker_source(load_checker):
    """Ensure that reset of the checker source works correctly."""
    assert checkers.CHECKER_SOURCE is None
    testargs = [os.getcwd()]
    commandline_arguments = [
        "CountCommandOutput",
        "--command",
        'echo "CorrectCommand"',
        "--count",
        "100",
    ]
    with patch.object(sys, "argv", testargs):
        parsed_arguments, remaining_arguments = arguments.parse(
            commandline_arguments
        )
        args_verified = arguments.verify(parsed_arguments)
        assert args_verified is True
        check_exists, checker_source, check_file = load_checker(
            parsed_arguments
        )
        assert check_exists is True
    checkers.reset_source()
    assert checkers.CHECKER_SOURCE is None


def test_check_transformation():
    """Ensure that check name transformation works correctly."""
    check_name_on_commandline = "CountCommits"
    transformed_check_name = checkers.transform_check(
        check_name_on_commandline
    )
    assert transformed_check_name == "check_CountCommits"


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--json", "ListChecks"]),
        (["--json", "--nowelcome", "ListChecks"]),
        (["--nowelcome", "ListChecks"]),
        (["--checkerdir", "./gator/checks", "ListChecks"]),
        (
            [
                "--checkerdir",
                "./gator/checks",
                "ListChecks",
                "--namecontains",
                "Com",
            ]
        ),
    ],
)
def test_check_function_verification_separate(
    commandline_arguments, load_check
):
    """Ensure that check verification works for standard functions."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        parsed_arguments, remaining_arguments = arguments.parse(
            commandline_arguments
        )
        args_verified = arguments.verify(parsed_arguments)
        assert args_verified is True
        check = load_check(parsed_arguments)
        assert checkers.verify_check_function(check, "act") is True
        assert checkers.verify_check_function(check, "get_parser") is True
        assert checkers.verify_check_function(check, "parse") is True


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--json", "ListChecks"]),
        (["--json", "--nowelcome", "ListChecks"]),
        (["--nowelcome", "ListChecks"]),
        (["--checkerdir", "./gator/checks", "ListChecks"]),
        (
            [
                "--checkerdir",
                "./gator/checks",
                "ListChecks",
                "--namecontains",
                "Com",
            ]
        ),
        (
            [
                "--checkerdir",
                "./gator/checks",
                "ListChecks",
                "--namecontains",
                "Exec",
            ]
        ),
    ],
)
def test_check_function_verification_list(commandline_arguments, load_check):
    """Ensure that check verification works for standard functions."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        parsed_arguments, remaining_arguments = arguments.parse(
            commandline_arguments
        )
        args_verified = arguments.verify(parsed_arguments)
        assert args_verified is True
        check = load_check(parsed_arguments)
        # verify that the check has the functions, specified separately
        assert (
            checkers.verify_check_functions(
                check, ["act", "get_parser", "parse"]
            )
            is True
        )
        # verify that the check has the functions, specified according to defaults
        assert checkers.verify_check_functions(check) is True
        # verify that the check does not have the provided functions, specified separately
        assert (
            checkers.verify_check_functions(
                check, ["actWRONG", "get_parser", "parse"]
            )
            is False
        )
        assert (
            checkers.verify_check_functions(
                check, ["act", "get_parserWRONG", "parse"]
            )
            is False
        )
        assert (
            checkers.verify_check_functions(
                check, ["actWRONG", "get_parser", "parseWRONG"]
            )
            is False
        )


def test_argument_not_none_verification():
    """Ensure that checking of the arguments is not None is working correctly."""
    assert (
        checkers.verify_arguments_not_none(["act", "get_parser", "parse"])
        is True
    )
    assert (
        checkers.verify_arguments_not_none([5, "get_parser", "parse"]) is True
    )
    assert checkers.verify_arguments_not_none([5, False, "parse"]) is True
    assert checkers.verify_arguments_not_none([5, None, "parse"]) is False
    assert checkers.verify_arguments_not_none([None]) is False
    assert checkers.verify_arguments_not_none([]) is True


def test_checkerdir_extraction_from_commandline_arguments(tmpdir):
    """Ensure that command-line argument extraction works in checker function if specified checkerdir."""
    _ = tmpdir.mkdir("checks").join("check_messages.py")
    assert len(tmpdir.listdir()) == 1
    checker_directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "checks"
    commandline_arguments = [
        "--checkerdir",
        checker_directory,
        "check_messages",
    ]
    gg_arguments, remaining_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(gg_arguments)
    assert args_verified is True
    found_checker_directory = checkers.get_checker_dir(gg_arguments)
    assert found_checker_directory == checker_directory


def test_empty_checkerdir_extraction_from_commandline_arguments(tmpdir):
    """Ensure that command-line argument extraction works in checker function if empty checkerdir."""
    _ = tmpdir.mkdir("checks").join("check_messages.py")
    assert len(tmpdir.listdir()) == 1
    commandline_arguments = ["check_messages"]
    gg_arguments, remaining_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(gg_arguments)
    assert args_verified is True
    found_checker_directory = checkers.get_checker_dir(gg_arguments)
    assert found_checker_directory == ""


def test_check_extraction_from_commandline_arguments(tmpdir):
    """Ensure that command-line argument extraction works in checker function."""
    checker = "check_CountCommits"
    _ = tmpdir.mkdir("checks").join(checker + ".py")
    assert len(tmpdir.listdir()) == 1
    checker_directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "checks"
    commandline_arguments = ["--checkerdir", checker_directory, checker]
    gg_arguments, remaining_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(gg_arguments)
    assert args_verified is True
    found_check = checkers.get_chosen_check(gg_arguments)
    assert found_check == checker


def test_load_checkers_list_is_not_empty_default_input():
    """Ensure that checker loading results in non-empty list with defaults."""
    checker_source = checkers.get_source()
    # the source for the plugins is not empty
    assert checker_source is not None
    # the source for the plugins contains plugins
    # that adhere to the naming scheme "check_<ACTION><ENTITY>"
    # for instance "check_commits"
    # we know that this should be true because all
    # internal GatorGrader plugins adhere to this convention
    for checker in checkers.list_checks(checker_source):
        assert "check_" in checker


def test_load_checkers_list_is_not_empt_blank_input():
    """Ensure that checker loading results in non-empty list with defaults."""
    # this case would occur on the command-line when
    # the checkerdir is not specified as an argument
    checker_source = checkers.get_source([""])
    # the source for the plugins is not empty
    assert checker_source is not None
    # the source for the plugins contains plugins
    # that adhere to the naming scheme "check_<ACTION><ENTITY>"
    # for instance "check_commits"
    # we know that this should be true because all
    # internal GatorGrader plugins adhere to this convention
    for checker in checkers.list_checks(checker_source):
        assert "check_" in checker


def test_load_checkers_list_is_not_empty_provided_input(tmpdir):
    """Ensure that checker loading results in non-empty list with provided list."""
    checker_file = tmpdir.mkdir("internal_checkers").join("check_testing.py")
    # this must be valid Python code because it will be loaded by pluginbase
    checker_file.write('"a checker"')
    checker_directory = (
        tmpdir.dirname + "/" + tmpdir.basename + "/" + "internal_checkers"
    )
    list_of_checker_directories = [checker_directory]
    checker_source = checkers.get_source(list_of_checker_directories)
    assert checker_source is not None
    checker_source_list = checkers.list_checks(checker_source)
    assert "check_testing" in checker_source_list


def test_load_checkers_list_is_not_empty_check_exists_with_provided_input(
    tmpdir,
):
    """Ensure that checker loading results in non-empty list containing check with provided list."""
    checker_file = tmpdir.mkdir("internal_checkers").join("check_testing.py")
    # this must be valid Python code because it will be loaded by pluginbase
    checker_file.write('"a checker"')
    checker_directory = (
        tmpdir.dirname + "/" + tmpdir.basename + "/" + "internal_checkers"
    )
    list_of_checker_directories = [checker_directory]
    checker_source = checkers.get_source(list_of_checker_directories)
    assert checker_source is not None
    checker_source_list = checkers.list_checks(checker_source)
    assert "check_testing" in checker_source_list
    assert (
        checkers.verify_check_existence("check_testing", checker_source)
        is True
    )
    assert (
        checkers.verify_check_existence("check_testing_WRONG", checker_source)
        is False
    )


def test_check_extraction_from_commandline_arguments_has_overall_help_when_no_checker():
    """Ensure that checker finding and help extraction works for a provided checker."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        checker = "check_CountCommits_Invalid"
        commandline_arguments = [checker]
        gg_arguments, remaining_arguments = arguments.parse(
            commandline_arguments
        )
        args_verified = arguments.verify(gg_arguments)
        assert args_verified is True
        found_check = checkers.get_chosen_check(gg_arguments)
        assert found_check == checker
        checker_source = checkers.get_source()
        check_helps = checkers.get_checks_help(checker_source)
        assert check_helps != ""
        assert "CountCommits" in check_helps
        counted_newlines = check_helps.count("\n")
        assert counted_newlines > 0


def test_check_extraction_from_commandline_arguments_has_help_single_checker():
    """Ensure that checker finding and help extraction works for a provided checker."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        checker = "check_CountCommits"
        commandline_arguments = [checker]
        gg_arguments, remaining_arguments = arguments.parse(
            commandline_arguments
        )
        args_verified = arguments.verify(gg_arguments)
        assert args_verified is True
        found_check = checkers.get_chosen_check(gg_arguments)
        assert found_check == checker
        checker_source = checkers.get_source()
        check_helps = checkers.get_checks_help(checker_source)
        assert check_helps != ""
        assert "CountCommits" in check_helps
        counted_newlines = check_helps.count("\n")
        assert counted_newlines > 0


def test_check_extraction_from_commandline_arguments_has_help_two_checkers_one_invalid(
    tmpdir,
):
    """Ensure that checker finding and help extraction works for a provided checker."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        checker_file = tmpdir.mkdir("internal_checkers").join(
            "check_testing.py"
        )
        # this must be valid Python code because it will be loaded by pluginbase
        checker_file.write('"a checker"')
        checker_directory = (
            tmpdir.dirname + "/" + tmpdir.basename + "/" + "internal_checkers"
        )
        checker = "check_CountCommits"
        assert len(tmpdir.listdir()) == 1
        commandline_arguments = ["--checkerdir", checker_directory, checker]
        gg_arguments, remaining_arguments = arguments.parse(
            commandline_arguments
        )
        args_verified = arguments.verify(gg_arguments)
        assert args_verified is True
        found_check = checkers.get_chosen_check(gg_arguments)
        assert found_check == checker
        # ensure that get_checks_help does not try to create a help
        # message for an invalid check that does not have a get_parser function
        checker_source = checkers.get_source([checker_directory])
        check_helps = checkers.get_checks_help(checker_source)
        assert check_helps != ""
        assert "CountCommits" in check_helps
        counted_newlines = check_helps.count("\n")
        assert counted_newlines > 0


def test_check_extraction_from_commandline_arguments_has_help_single_checker_filtered():
    """Ensure that checker finding and help extraction works for a single filtered check."""
    testargs = [os.getcwd()]
    with patch.object(sys, "argv", testargs):
        checker = "ListChecks"
        commandline_arguments = [
            "--checkerdir",
            "./gator/checks",
            "ListChecks",
            "--namecontains",
            "Exec",
        ]
        gg_arguments, remaining_arguments = arguments.parse(
            commandline_arguments
        )
        args_verified = arguments.verify(gg_arguments)
        assert args_verified is True
        found_check = checkers.get_chosen_check(gg_arguments)
        assert found_check == checker
        checker_source = checkers.get_source()
        check_helps = checkers.get_checks_help(
            checker_source, namecontains="Exec"
        )
        assert check_helps != ""
        assert "Exec" in check_helps
        counted_newlines = check_helps.count("\n")
        assert counted_newlines > 0


def test_list_checks_returns_all_internal_checks():
    """Ensure that list_checks returns all internal checks."""
    check_files = filter(
        lambda f: f.startswith("check_"), os.listdir("./gator/checks")
    )
    checker_source = checkers.get_source()
    available_checks = checkers.list_checks(checker_source)
    for check_file in check_files:
        check_name = check_file.replace(".py", "")
        assert check_name in available_checks


def test_load_check_can_load_internal_check():
    """Ensure that load_check can load internal checks."""
    check = checkers.load_check(None, "check_CountCommits")
    assert check is not None
    assert hasattr(check, "act")


def test_example_external_checker_appears_in_listing():
    """Ensure that the example external checker is listed via --checkerdir."""
    example_directory = os.path.join(os.getcwd(), "examples", "plugin")
    checker_source = checkers.get_source([example_directory])
    assert "check_WordCountExample" in checkers.list_checks(checker_source)
    check_helps = checkers.get_checks_help(checker_source)
    assert "WordCountExample" in check_helps


def test_example_external_checker_runs_end_to_end(tmpdir):
    """Ensure that the example external checker passes and fails correctly."""
    sample_file = tmpdir.join("essay.txt")
    sample_file.write("one two three four five six seven")
    example_directory = os.path.join(os.getcwd(), "examples", "plugin")
    checker_source = checkers.get_source([example_directory])
    example_check = checkers.load_check(
        checker_source, "check_WordCountExample"
    )
    passing_args = [
        "--file",
        "essay.txt",
        "--directory",
        str(tmpdir),
        "--count",
        "7",
    ]
    failing_args = [
        "--file",
        "essay.txt",
        "--directory",
        str(tmpdir),
        "--count",
        "8",
    ]
    assert example_check.act(None, passing_args) is True
    assert example_check.act(None, failing_args) is False


def test_invalid_external_checker_does_not_crash_help(tmpdir):
    """Ensure that listing checks survives a malformed external checker."""
    checker_directory = tmpdir.mkdir("external_checkers")
    checker_file = checker_directory.join("check_testing.py")
    # this must be valid Python code because it will be loaded by pluginbase
    checker_file.write('"a checker"')
    checker_source = checkers.get_source([str(checker_directory)])
    assert "check_testing" in checkers.list_checks(checker_source)
    # no get_parser function means no help text, but no crash either
    assert checkers.get_checks_help(checker_source) != ""


def test_plugin_verification_helpers():
    """Ensure that the documented contract helpers classify modules."""

    class WellFormedChecker:
        """Checker module with the documented shape."""

        def get_parser():
            """Return a parser."""

        def parse(args):
            """Parse the arguments."""

        def act(main_parsed_arguments, check_remaining_arguments) -> bool:
            """Run the check."""

    class UnannotatedActChecker(WellFormedChecker):
        """Checker whose act does not declare its bool return."""

        def act(main_parsed_arguments, check_remaining_arguments):
            """Run the check."""

    class MissingActChecker:
        """Checker module without the required act function."""

        def get_parser():
            """Return a parser."""

        def parse(args):
            """Parse the arguments."""

    assert plugin.verify_check_functions(WellFormedChecker) is True
    assert plugin.verify_act_returns_bool(WellFormedChecker) is True
    assert plugin.verify_act_returns_bool(UnannotatedActChecker) is False
    assert plugin.verify_check_functions(MissingActChecker) is False
    assert plugin.verify_act_returns_bool(MissingActChecker) is False
