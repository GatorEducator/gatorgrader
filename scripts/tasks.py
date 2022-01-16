"""Run tasks that support easy testing across multiple Python versions."""

from invoke import task


# the default version of Python for use in invoke tasks
DEFAULT_PYENV_VERSION = "3.7.3"


def internal_cover(c, cover=True):
    """Run the test suite, optionally with coverage tracking enabled."""
    # run test suite with coverage analysis
    if cover:
        c.run("poetry run task cover")
    # run test suite without coverage analysis
    else:
        c.run("poetry run task test")


def internal_switch(c, pyenv=DEFAULT_PYENV_VERSION):
    """Switch the version of Python managed by Pipenv to specified version."""
    # select current_pyenv as the version of Python
    c.run("pyenv local " + pyenv)
    # create the virtualenv managed by Pipenv with current_pyenv
    c.run("poetry env use `pyenv which python`")
    # display diagnostic information about new version of Python
    c.run("python --version")


@task
def switch(c, pyenv=DEFAULT_PYENV_VERSION):
    """Task to switch the version of Python managed by Pipenv to specified version."""
    internal_switch(c, pyenv)


@task(iterable=["pyenv"])
def cover(c, pyenv):
    """Run coverage-monitored tests with Pytest after full setup of each provided Pyenv version."""
    # Note that this task will leave a developer in the last specified version of Python
    # run the test suite for all of the provided versions of Python managed by Pyenv
    for current_pyenv in pyenv:
        print("Python version: " + current_pyenv)
        internal_switch(c, current_pyenv)
        # run the test suite and collect coverage information
        internal_cover(c, cover=True)


@task(iterable=["pyenv"])
def test(c, pyenv):
    """Run tests with Pytest after full setup of each provided Pyenv version."""
    # Note that this task will leave a developer in the last specified version of Python
    # run the test suite for all of the provided versions of Python managed by Pyenv
    for current_pyenv in pyenv:
        print("Python version: " + current_pyenv)
        internal_switch(c, current_pyenv)
        # run the test suite
        internal_cover(c, cover=False)
