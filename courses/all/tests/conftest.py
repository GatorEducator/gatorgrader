"""Configuration file for the test_gatorgrader_submit_files test suite"""

DIRECTORY = "directory"


def pytest_addoption(parser):
    """ Add command-line options for running test_gatorgrader_submit_files"""
    parser.addoption(
        "--directory",
        action="append",
        default=[],
        help="list of directories for GatorGrader to check")


def pytest_generate_tests(metafunc):
    """ Generate the test cases from the command-line arguments """
    if DIRECTORY in metafunc.fixturenames:
        print(metafunc.config.getoption(DIRECTORY))
        metafunc.parametrize(DIRECTORY,
                             metafunc.config.getoption(DIRECTORY))
