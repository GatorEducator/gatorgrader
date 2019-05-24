"""Utility functions that check the contents of the file system"""

from pathlib import Path


def create_path(*args, file, home):
    """Create a Path object for a file with varying sub-path count"""
    # create the Path for the file_home
    home_path = Path(home)
    # create the Path for the given file
    given_file_path = Path(file)
    final_path = home_path
    # Create a containing directory of sub-directories for the file.
    # each of these paths will be a path between the home and the
    # specified file. None of these paths need their anchor, though,
    # which is given like "C:\" on Windows and "/" otherwise.
    # pylint: disable=old-division
    for containing_path in args:
        nested_path = Path(containing_path)
        final_path = final_path / nested_path.relative_to(nested_path.anchor)
    # add the file at the end of the constructed file path
    final_path = final_path / given_file_path
    return final_path


def check_file_in_directory(*args, file, home):
    """Returns true if the specified file is in the directory"""
    # create the path so that it has this structure:
    # <home> + <any paths in *args, without their anchor> + <file>
    file_for_checking_path = create_path(*args, file=file, home=home)
    # return true if the specified file exists
    return file_for_checking_path.is_file()
