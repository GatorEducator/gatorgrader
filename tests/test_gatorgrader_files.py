""" test cases for the gatorgrader_files module """

import gatorgrader_files


def test_one_file_found_in_subdirectory(tmpdir):
    """ file_in_directory can file one file in a subdirectory """
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    print(tmpdir.basename)
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1
    was_file_found = gatorgrader_files.file_in_directory(
        "hello.txt", tmpdir.dirname + "/" + tmpdir.basename + "/" + "sub")
    assert was_file_found is True
