"""Configuration file for the test suite."""

import os
import sys

GO_BACK_A_DIRECTORY = "/../"

# set the system path to contain the previous directory
PREVIOUS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PREVIOUS_DIRECTORY + GO_BACK_A_DIRECTORY)
