@echo off
setlocal EnableDelayedExpansion

uv run pytest -s --cov-config .coveragerc --cov-report term-missing --cov-report xml --cov --cov-branch
