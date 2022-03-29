"""
**GatorGrader** CLI.

Call ``main`` to run the command-line interface.
The arguments will be retrieved from ``sys.argv``.
The results of the check will be formatted and printed.

If more control is needed, import the ``gator`` package and use ``gator.grader`` or ``gator.grader_cli``.
"""

import sys

from gator import *


def main():
    """Run GatorGrader."""
    # orchestrate check given by the command line arguments
    exit_code = grader_cli(sys.argv[1:])
    # exit the program with the returned code
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
