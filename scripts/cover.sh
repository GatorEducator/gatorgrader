#!/bin/bash

pipenv run pytest -s --cov-config pytest.cov --cov-report term-missing --cov
