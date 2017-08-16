import os
import sys

# set the system path to contain the previous directory
mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, mypath + '/../')


def pytest_addoption(parser):
    """define the viable command-line arguments when running tests"""
    # define command-line argument for including slow tests
    parser.addoption(
        "--runslow", action="store_true", help="Run the slow test cases")
    # define command-line argument for including tests that securely download files
    parser.addoption(
        "--rundownload", action="store_true", help="Run the downloading test cases")
