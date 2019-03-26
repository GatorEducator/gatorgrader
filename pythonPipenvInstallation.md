# Python and Pipenv Installation Instructions
Below are the instructions for installing Python and Pipenv.

## Python Installation
Python comes pre-installed on many different distributions, and is available as
a package on all linux distributions. However there are certain features you
might want to use that are not available on your distro’s package. Simply google `python download` for your OS, and follow 
the download and installation instructions on (the Python website)[python.org].

## Pipenv Installation
[Pipenv](https://github.com/pypa/pipenv) is used by gatorGrader to: create a
virtual testing environment, install and manage development packages, and to run
Python commands. Pipenv relies on Pip for installation. After installing Python,
ensure Pip is installed on your device and you can simply install Pipenv
through the terminal.

### Ubuntu:
- Install and upgrade the `pipenv` command: `pip install pipenv --user`
- Install the development dependencies `pipenv` command: `pipenv install --dev`

### MacOS:
- `brew install pipenv`

### Windows:
- Install and upgrade the `pipenv` command: `pip install pipenv --user`
- Install the development dependencies `pipenv` command: `pipenv install --dev`
