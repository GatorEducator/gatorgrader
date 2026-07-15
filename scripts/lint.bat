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

echo -- Running black
uv run black %CHECK% %FILES%
if ERRORLEVEL 1 (
    echo -- Failed
    set PASSED=false
) else (
    echo -- Passed
)

echo -- Running pylint
uv run pylint %FILES%
if ERRORLEVEL 1 (
    echo -- Failed
    set PASSED=false
) else (
    echo -- Passed
)

echo -- Running flake8
uv run flake8 %FILES%
if ERRORLEVEL 1 (
    echo -- Failed
    set PASSED=false
) else (
    echo -- Passed
)

echo -- Running pydocstyle
uv run pydocstyle %FILES%
if ERRORLEVEL 1 (
    echo -- Failed
    set PASSED=false
) else (
    echo -- Passed
)

echo -- Running radon cc
uv run radon cc %FILES%
if ERRORLEVEL 1 (
    echo -- Failed
    set PASSED=false
) else (
    echo -- Passed
)

echo -- Running radon mi
uv run radon mi %FILES%
if ERRORLEVEL 1 (
    echo -- Failed
    set PASSED=false
) else (
    echo -- Passed
)

echo -- Running xenon
uv run xenon --max-absolute D --max-modules B --max-average A gator
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
