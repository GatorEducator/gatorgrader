#!/bin/bash

if [[ "$1" == "--check" ]]; then
    CHECK="--check"
else
    CHECK=""
fi

PASSED=true

OS="$(uname)"

if [[ "$OS" == "Darwin" ]]; then
    FILES=$(find -E . -type f -regex '\./(gator|tests)/.*.py')
else
    FILES=$(find . -type f -regextype posix-extended -regex '\./(gator|tests)/.*.py')
fi

# lint all of the Python source code files
FILES="$FILES *.py"

declare -A LINTERS

# define all of the linters to iteratively run
LINTERS=( ["black"]="pipenv run black $CHECK $FILES" ["pylint"]="pipenv run pylint $FILES" ["flake8"]="pipenv run flake8 $FILES" ["bandit"]="pipenv run bandit -c bandit.yml $FILES" ["radon"]="pipenv run radon mi $FILES" ["pydocstyle"]="pipenv run pydocstyle $FILES" )

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

if [[ "$PASSED" != "true" ]]; then
    echo "Not all linters passed!"
    exit 1
else
    echo "All is good!"
    exit 0
fi
