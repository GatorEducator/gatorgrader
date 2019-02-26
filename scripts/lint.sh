#!/bin/bash

if [[ "$1" == "--check" ]]; then
    CHECK="--check"
else
    CHECK=""
fi

PASSED=true

OS="$(uname)"

if [[ "$OS" == "Darwin" ]]; then
    FILES=$(find -E . -type f -regex "\./(gator|tests)/.*.py")
else
    FILES=$(find . -type f -regextype posix-extended -regex "\./(gator|tests)/.*.py")
fi

FILES="$FILES *.py"

echo " -- Running black"
pipenv run black $CHECK $FILES

if [[ $? != 0 ]]; then
    echo " -- Failed"
    PASSED=false
else
    echo " -- Passed"
fi
echo ""
echo " -- Running pylint"
pipenv run pylint $FILES

if [[ $? != 0 ]]; then
    echo " -- Failed"
    PASSED=false
else
    echo " -- Passed"
fi
echo ""
echo " -- Running flake8"
pipenv run flake8 $FILES

if [[ $? != 0 ]]; then
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
