"""Configuration file for the test_gatorgrader_submit_files test suite"""

DIRECTORY = "directory"
CHECKFILE = "checkfile"


def pytest_addoption(parser):
    """ Add command-line options for running test_gatorgrader_submit_files"""
    parser.addoption(
        "--directory",
        action="append",
        default=[],
        help="directory for GatorGrader to check")
    parser.addoption(
        "--checkfile",
        action="append",
        default=[],
        help="file for GatorGrader to check")


def pytest_generate_tests(metafunc):
    """ Generate the test cases from the command-line arguments """
    if DIRECTORY in metafunc.fixturenames:
        metafunc.parametrize(DIRECTORY,
                             metafunc.config.getoption(DIRECTORY))
    if CHECKFILE in metafunc.fixturenames:
        metafunc.parametrize(CHECKFILE,
                             metafunc.config.getoption(CHECKFILE))
