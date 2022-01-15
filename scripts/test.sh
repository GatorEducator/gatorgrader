#!/bin/sh

# Run the test suite so that:
# --> -x: Stops on first error or failure
# --> -s: Outputs all diagnostic information
poetry run pytest -x -s
