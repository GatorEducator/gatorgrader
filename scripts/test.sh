#!/usr/bin/env sh

# Run the test suite so that:
# --> -x: Stops on first error or failure
# --> -s: Outputs all diagnostic information
uv run pytest -x -s
