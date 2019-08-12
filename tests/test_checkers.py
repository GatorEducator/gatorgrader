"""Tests for the loading, verification, and use of plugin-based checkers."""


from gator import arguments
from gator import checkers


def test_check_transformation():
    """Ensure that check name transformation works correctly."""
    check_name_on_commandline = "CountCommits"
    transformed_check_name = checkers.transform_check(check_name_on_commandline)
    assert transformed_check_name == "check_CountCommits"


def test_checkerdir_extraction_from_commandline_arguments(tmpdir):
    """Ensure that command-line argument extraction works in checker function if specified checkerdir."""
    _ = tmpdir.mkdir("checks").join("check_messages.py")
    assert len(tmpdir.listdir()) == 1
    checker_directory = tmpdir.dirname + "/" + tmpdir.basename + "/" + "checks"
    commandline_arguments = ["--checkerdir", checker_directory, "check_messages"]
    gg_arguments = arguments.parse(commandline_arguments)
    args_verified = arguments.verify(gg_arguments)
    assert args_verified is True
    found_checker_directory = checkers.get_checker_dir(gg_arguments)
    assert found_checker_directory == checker_directory


def test_empty_checkerdir_extraction_from_commandline_arguments(tmpdir):
    """Ensure that command-line argument extraction works in checker function if empty checkerdir."""
    _ = tmpdir.mkdir("checks").join("check_messages.py")
    assert len(tmpdir.listdir()) == 1
    commandline_arguments = ["check_messages"]
    gg_arguments = arguments.parse(commandline_arguments)
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
    gg_arguments = arguments.parse(commandline_arguments)
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
    checker_file.write("a checker")
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
    checker_file = tmpdir.mkdir("internal_checkers").join("check_testing.py")
    checker_file.write("a checker")
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
