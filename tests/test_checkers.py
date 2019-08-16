"""Tests for the loading, verification, and use of plugin-based checkers."""


from gator import arguments
from gator import checkers

import pytest


@pytest.fixture(scope="module", autouse=True)
def reset_checker_source():
    """Before running a test in this suite always reset the source of the checkers in pluginbase."""
    # note that performing this reset ensures test independence and
    # avoids test flakiness for single-test runs or different test orderings
    checkers.reset_source()


def test_check_transformation():
    """Ensure that check name transformation works correctly."""
    check_name_on_commandline = "CountCommits"
    transformed_check_name = checkers.transform_check(check_name_on_commandline)
    assert transformed_check_name == "check_CountCommits"


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--json", "ListChecks"]),
        (["--json", "--nowelcome", "ListChecks"]),
        (["--nowelcome", "ListChecks"]),
        (["--checkerdir", "./gator/checks", "ListChecks"]),
        (["--checkerdir", "./gator/checks", "ListChecks", "--namecontains", "Com"]),
    ],
)
def test_check_function_verification_separate(commandline_arguments):
    """Ensure that check verification works for standard functions."""
    parsed_arguments, remaining_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(parsed_arguments)
    assert args_verified is True
    external_checker_directory = checkers.get_checker_dir(parsed_arguments)
    checker_source = checkers.get_source([external_checker_directory])
    check_name = checkers.get_chosen_check(parsed_arguments)
    check_file = checkers.transform_check(check_name)
    check_exists = checkers.verify_check_existence(check_file, checker_source)
    assert check_exists is True
    check = checker_source.load_plugin(check_file)
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
        (["--checkerdir", "./gator/checks", "ListChecks", "--namecontains", "Com"]),
    ],
)
def test_check_function_verification_list(commandline_arguments):
    """Ensure that check verification works for standard functions."""
    parsed_arguments, remaining_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(parsed_arguments)
    assert args_verified is True
    external_checker_directory = checkers.get_checker_dir(parsed_arguments)
    checker_source = checkers.get_source([external_checker_directory])
    check_name = checkers.get_chosen_check(parsed_arguments)
    check_file = checkers.transform_check(check_name)
    check_exists = checkers.verify_check_existence(check_file, checker_source)
    assert check_exists is True
    # create the check
    check = checker_source.load_plugin(check_file)
    # verify that the check has the functions, specified separately
    assert (
        checkers.verify_check_functions(check, ["act", "get_parser", "parse"]) is True
    )
    # verify that the check has the functions, specified according to defaults
    assert checkers.verify_check_functions(check) is True
    # verify that the check does not have the provided functions, specified separately
    assert (
        checkers.verify_check_functions(check, ["actWRONG", "get_parser", "parse"])
        is False
    )
    assert (
        checkers.verify_check_functions(check, ["act", "get_parserWRONG", "parse"])
        is False
    )
    assert (
        checkers.verify_check_functions(check, ["actWRONG", "get_parser", "parseWRONG"])
        is False
    )


def test_argument_not_none_verification():
    """Ensure that checking of the arguments is not None is working correctly."""
    assert checkers.verify_arguments_not_none(["act", "get_parser", "parse"]) is True
    assert checkers.verify_arguments_not_none([5, "get_parser", "parse"]) is True
    assert checkers.verify_arguments_not_none([5, False, "parse"]) is True
    assert checkers.verify_arguments_not_none([5, None, "parse"]) is False
    assert checkers.verify_arguments_not_none([None]) is False
    assert checkers.verify_arguments_not_none([]) is True


def test_checkerdir_extraction_from_commandline_arguments(tmpdir):
    """Ensure that command-line argument extraction works in checker function if specified checkerdir."""
    _ = tmpdir.mkdir("checks").join("check_messages.py")
    assert len(tmpdir.listdir()) == 1
    checker_directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "checks"
    commandline_arguments = ["--checkerdir", checker_directory, "check_messages"]
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
    for checker in checker_source.list_plugins():
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
    for checker in checker_source.list_plugins():
        assert "check_" in checker


def test_load_checkers_list_is_not_empty_provided_input(tmpdir):
    """Ensure that checker loading results in non-empty list with provided list."""
    checker_file = tmpdir.mkdir("internal_checkers").join("check_testing.py")
    # this must be valid Python code because it will be loaded by pluginbase
    checker_file.write('"' 'a checker"' "")
    checker_directory = (
        tmpdir.dirname + "/" + tmpdir.basename + "/" + "internal_checkers"
    )
    list_of_checker_directories = [checker_directory]
    checker_source = checkers.get_source(list_of_checker_directories)
    assert checker_source is not None
    checker_source_list = checker_source.list_plugins()
    assert len(checker_source_list) >= 1


def test_load_checkers_list_is_not_empty_check_exists_with_provided_input(tmpdir):
    """Ensure that checker loading results in non-empty list containing check with provided list."""
    checkers.reset_source()
    checker_file = tmpdir.mkdir("internal_checkers").join("check_testing.py")
    # this must be valid Python code because it will be loaded by pluginbase
    checker_file.write('"' 'a checker"' "")
    checker_directory = (
        tmpdir.dirname + "/" + tmpdir.basename + "/" + "internal_checkers"
    )
    list_of_checker_directories = [checker_directory]
    checker_source = checkers.get_source(list_of_checker_directories)
    assert checker_source is not None
    checker_source_list = checker_source.list_plugins()
    assert len(checker_source_list) >= 1
    assert checkers.verify_check_existence("check_testing", checker_source) is True
    assert (
        checkers.verify_check_existence("check_testing_WRONG", checker_source) is False
    )


def test_check_extraction_from_commandline_arguments_has_overall_help_when_no_checker():
    """Ensure that checker finding and help extraction works for a provided checker."""
    checker = "check_CountCommits_Invalid"
    commandline_arguments = [checker]
    gg_arguments, remaining_arguments = arguments.parse(commandline_arguments)
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
    checker = "check_CountCommits"
    commandline_arguments = [checker]
    gg_arguments, remaining_arguments = arguments.parse(commandline_arguments)
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
    tmpdir
):
    """Ensure that checker finding and help extraction works for a provided checker."""
    invalid_checker = "check_IncorrectChecker"
    checker = "check_CountCommits"
    _ = tmpdir.mkdir("checks").join(invalid_checker + ".py")
    assert len(tmpdir.listdir()) == 1
    checker_directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "checks"
    commandline_arguments = ["--checkerdir", checker_directory, checker]
    gg_arguments, remaining_arguments = arguments.parse(commandline_arguments)
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
