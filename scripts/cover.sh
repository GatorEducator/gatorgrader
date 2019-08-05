#!/bin/bash

# Run the test suite so that:
# --> -s: Outputs all diagnostic information
# --> Other parameters: Track coverage and output report as XML file
pipenv run pytest -s --cov-config .coveragerc --cov-report term-missing --cov-report xml --cov --cov-branch
