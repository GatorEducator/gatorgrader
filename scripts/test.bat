@echo off
setlocal EnableDelayedExpansion

poetry run pytest -x -s
