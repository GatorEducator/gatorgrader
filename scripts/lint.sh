#!/bin/bash

if [[ "$1" = "--check" ]]; then
    CHECK="--check"
else
    CHECK=""
fi

PASSED=true

FILES=$(find . -type f -name "*.py")

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
