@echo off
setlocal EnableDelayedExpansion

if '%1'=='--check' (
    set CHECK=--check
) else (
    set CHECK=
)

set PASSED=true

dir /b /s | findstr "\\*.py$" | findstr /v "\\\.venv\\" > .xyzfiles
for /f "Tokens=* Delims=" %%x in (.xyzfiles) do set FILES=!FILES! %%x
del .xyzfiles

set PATHS="gator tests"

echo -- Running black
pipenv run black %CHECK% %FILES%
if ERRORLEVEL 1 (
    echo -- Failed
    set PASSED=false
) else (
    echo -- Passed
)

echo -- Running pylint
pipenv run pylint %FILES%
if ERRORLEVEL 1 (
    echo -- Failed
    set PASSED=false
) else (
    echo -- Passed
)

echo -- Running flake8
pipenv run flake8 %FILES%
if ERRORLEVEL 1 (
    echo -- Failed
    set PASSED=false
) else (
    echo -- Passed
)

echo -- Running bandit
pipenv run bandit -c bandit.yml %FILES%
if ERRORLEVEL 1 (
    echo -- Failed
    set PASSED=false
) else (
    echo -- Passed
)

echo -- Running pydocstyle
pipenv run pydocstyle %FILES%
if ERRORLEVEL 1 (
    echo -- Failed
    set PASSED=false
) else (
    echo -- Passed
)

echo -- Running radon
pipenv run radon mi %FILES%
if ERRORLEVEL 1 (
    echo -- Failed
    set PASSED=false
) else (
    echo -- Passed
)

echo -- Running xenon
pipenv run xenon --max-absolute D --max-modules B --max-average B -c %PATHS%
if ERRORLEVEL 1 (
    echo -- Failed
    set PASSED=false
) else (
    echo -- Passed
)

if "%PASSED%"=="true" (
    exit /b 0
) else (
    exit /b 1
)
