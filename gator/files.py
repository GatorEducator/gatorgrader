"""Utility functions that check the contents of the file system"""

from pathlib import Path


def create_path(*args, file, home):
    """Create a Path object for a file with varying sub-path count"""
    # create the Path for the file_home
    home_path = Path(home)
    # create the Path for the given file
    given_file_path = Path(file)
    final_path = home_path
    # create a containing directory of sub-directories for the file
    # pylint: disable=old-division
    for containing_path in args:
        print("This is the containing_path: " + containing_path)
        nested_path = Path(containing_path)
        final_path = final_path / nested_path.relative_to(nested_path.anchor)
    final_path = final_path / given_file_path
    print("This is the final path" + str(final_path.absolute))
    return final_path


def check_file_in_directory(*args, file, home):
    """Returns true if the specified file is in the directory"""
    # always use a Path from pathlib to ensure platform independence
    # create the Path for the home_prefix
    # home_prefix_path = Path(home_prefix)
    # create the Path for the containing directory
    # containing_directory_path = Path(containing_dir)
    # create the Path for the given file
    # given_file_path = Path(given_file)
    # create the Path file for checking
    # Since home_prefix_path and containing_directory_path are both absolute,
    # the code must make the containing_directory_path relative by stripping
    # off its anchor, allowing paths to be joined on all operating systems
    # pylint: disable=old-division
    file_for_checking_path = create_path(*args, file=file, home=home)
    # file_for_checking_path = (
    #     home_prefix_path
    #     / containing_directory_path.relative_to(containing_directory_path.anchor)
    #     / given_file_path
    # )
    print("new:" + str(file_for_checking_path))
    return file_for_checking_path.is_file()
