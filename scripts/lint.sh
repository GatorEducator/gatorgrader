#!/bin/bash

if [[ "$1" == "--check" ]]; then
    CHECK="--check"
else
    CHECK=""
fi

PASSED=true

OS="$(uname)"

if [[ "$OS" == "Darwin" ]]; then
    FILES=$(find -E . -type f -regex "\./(gator/|tests/)?.*.py")
else
    FILES=$(find . -type f -regextype posix-extended -regex "\./(gator/|tests/)?.*.py")
fi

echo " -- Running black"
# shellcheck disable=SC2086
if ! pipenv run black $CHECK $FILES; then
    echo " -- Failed"
    PASSED=false
else
    echo " -- Passed"
fi
echo ""
echo " -- Running pylint"
# shellcheck disable=SC2086
if ! pipenv run pylint $FILES; then
    echo " -- Failed"
    PASSED=false
else
    echo " -- Passed"
fi
echo ""
echo " -- Running flake8"
# shellcheck disable=SC2086
if ! pipenv run flake8 $FILES; then
    echo " -- Failed"
    PASSED=false
else
    echo " -- Passed"
fi
echo ""
echo " -- Running bandit"
# shellcheck disable=SC2086
if ! pipenv run bandit -c ".bandit" $FILES; then
    echo " -- Failed"
    PASSED=false
else
    echo " -- Passed"
fi

if [[ "$PASSED" != "true" ]]; then
    exit 1
else
    exit 0
fi
