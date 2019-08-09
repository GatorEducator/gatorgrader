#!/bin/bash

# Run the test suite so that:
# --> -s: Outputs all diagnostic information
# --> Other parameters: Track coverage and output report as XML file
# Note that this command tracks both branch and statement coverage:
# --> pytest-cov collects statement coverage by default
# --> --cov-branch additionally specifies the collection of branch coverage
pipenv run pytest -s --cov-config .coveragerc --cov-report term-missing --cov-report xml --cov --cov-branch
