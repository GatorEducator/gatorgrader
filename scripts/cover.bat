@echo off
setlocal EnableDelayedExpansion

poetry run pytest -s --cov-config .coveragerc --cov-report term-missing --cov-report xml --cov --cov-branch
