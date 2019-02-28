# Python and Pipenv Installation Instructions
Below are the instructions for installing Python and Pipenv.

## Python Installation
Python comes pre-installed on many different distributions, and is available as
a package on all linux distributions. However there are certain features you
might want to use that are not available on your distro’s package. You can
easily compile the latest version of Python from source. Below are the links to the most recent Python download, and Python installation help.

### Ubuntu:

  - [Link to download.](https://www.python.org/downloads/source/)

  - [Link to installation instructions.](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
### MacOS:
  - [Link to download.](https://www.python.org/downloads/mac-osx/)

  - [Link to installation instructions.](https://docs.python.org/3/using/mac.html)
### Windows:
  - [Link to download.](https://www.python.org/downloads/windows/)

  - [Link to installation instructions.](https://docs.python.org/3/using/windows.html)
## Pipenv Installation
[Pipenv](https://github.com/pypa/pipenv) is used by gatorGrader to: create a
virtual testing environment, install and manage development packages, and to run
Python commands. Pipenv relies on Pip for installation. After installing Python,
ensure Pip is installed on your device and you can simply install Pipenv
through the terminal.

### Pip installation:
- If you think you have Pip installed on Windows, verify it with the command
  `python -m pip install --upgrade pip`
- If you think you have Pip installed on other OS's, verify it with the command
  `pip install --upgrade pip`
- Otherwise
  Download get-pip.py at [download](https://pip.pypa.io/en/stable/installing/).
  Or on Ubuntu, you can download by opening a terminal and entering: `curl
  https://bootstrap.pypa.io/get-pip.py -o get-pip.py`

  Then run `python get-pip.py`



### Ubuntu:
- Install and upgrade the `pipenv` command: `pip install pipenv --user`
- Install the development dependencies `pipenv` command: `pipenv install --dev`

### MacOS:
- `brew install pipenv`
<!--TODO: Add more mac commands -->

### Windows:
- Install and upgrade the `pipenv` command: `pip install pipenv --user`
- Install the development dependencies `pipenv` command: `pipenv install --dev`
