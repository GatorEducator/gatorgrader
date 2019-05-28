"""Utility functions that check the contents of the file system"""

from pathlib import Path


def create_path(*args, file, home):
    """Create a Path object for a file with varying sub-path count"""
    # create the Path for the home
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


def case_native_check_file_in_directory(*args, file, home):
    """Returns true if the case-insensitive specified file is in the directory"""
    # create the path so that it has this structure:
    # <home> + <any paths in *args, without their anchor> + <file>
    file_for_checking_path = create_path(*args, file=file, home=home)
    # return true if the specified file exists
    return file_for_checking_path.is_file()


def case_sensitive_check_file_in_directory(*args, file, home):
    """Returns true if the case-sensitive specified file is in the directory"""
    # create the path so that it has this structure:
    # <home> + <any paths in *args, without their anchor> + <file>
    file_for_checking_path = create_path(*args, file=file, home=home)
    # get parent, i.e., the containing directory for the specified file
    file_parent = file_for_checking_path.parent
    # create a generator of all of the files in the parent directory
    file_parent_glob = file_parent.glob("**/*")
    # assume that the file with the correct name has not been found
    # and prove otherwise by iterating through the generator of files
    file_found = False
    for current_file in file_parent_glob:
        # the case-sensitive file name has been found
        if str(current_file.name) == file:
            file_found = True
    return file_found


def check_file_in_directory(*args, file, home):
    """Returns true if the specified file is in the directory"""
    # perform the standard check that relies on the operating system
    # to determine whether or not the file exists on the file system
    no_case_file_exists = case_native_check_file_in_directory(
        *args, file=file, home=home
    )
    # perform a case-sensitive check that lists all of the files in
    # the provided directory and then checks for exactly the file name
    case_file_exists = case_sensitive_check_file_in_directory(
        *args, file=file, home=home
    )
    # both of the checks have passed and thus the file does exist
    return no_case_file_exists and case_file_exists
