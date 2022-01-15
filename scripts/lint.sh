#!/bin/bash

# determine whether or not black code formatting
# will fail if code is not correctly formatted
# "--check" returns non-zero exit code if formatting needed
# otherwise, the black check is run for diagnostic purposes
if [[ "$1" == "--check" ]]; then
    CHECK="--check"
else
    CHECK=""
fi

# assume that all of the linters passed and prove otherwise
PASSED=true

OS="$(uname)"

# collect the files on MacOS
if [[ "$OS" == "Darwin" ]]; then
    FILES=$(find -E . -type f -regex '\./(gator|tests)/.*.py')
else
    FILES=$(find . -type f -regextype posix-extended -regex '\./(gator|tests)/.*.py')
fi

# lint all of the Python source code files
FILES="$FILES *.py"

# xenon cannot accept a lists of files or directories,
# so give the directory of the main module instead
MODULE="gator"

# Notes about the linters run on Linux and MacOS:
# - black checks and fixes Python code formatting
# - pylint and flake8 check Python code
# - bandit finds security problems in Python code
# - radon checks code quality for diagnostic purposes
#   --> cc is for calculating cyclomatic complexity
#   --> mi is for calculating maintainability index
# - xenon returns an error code for code quality thresholds
#   --> absolute: worst tolerable score for a function or block
#   --> modules: worst tolerable score for a module
#   --> average: worst tolerable average score across a module

# define all of the linters to iteratively run
declare -A LINTERS
LINTERS=( ["black"]="poetry run black $CHECK $FILES" ["pylint"]="poetry run pylint $FILES" ["flake8"]="poetry run flake8 $FILES" ["bandit"]="poetry run bandit -c bandit.yml $FILES" ["radon-cc"]="poetry run radon cc $FILES" ["radon-mi"]="poetry run radon mi $FILES" ["xenon"]="poetry run xenon --max-absolute D --max-modules B --max-average A $MODULE" ["pydocstyle"]="poetry run pydocstyle $FILES" )

# run each of the already configured linters
for tool in "${!LINTERS[@]}"; do
    echo " -- Running $tool"
    # shellcheck disable=SC2086
    if ! ${LINTERS[$tool]}; then
        echo " -- Failed"
        PASSED=false
    else
        echo " -- Passed"
    fi
    echo ""
done

# display the final diagnostic information
if [[ "$PASSED" != "true" ]]; then
    echo "Not all linters passed!"
    exit 1
else
    echo "All is good!"
    exit 0
fi
