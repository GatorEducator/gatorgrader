"""Run tasks that support easy testing across multiple Python versions."""

from invoke import task


@task
def switch(c, pyenv="3.7.3"):
    """Switch the version of Python managed by Pipenv to specified version."""
    # select current_pyenv as the version of Python
    c.run("pyenv local " + pyenv)
    # create the virtualenv managed by Pipenv with current_pyenv
    c.run("pipenv install --skip-lock --python=`pyenv which python` --dev")
    # display diagnostic information about new version of Python
    c.run("python --version")


@task(iterable=['pyenv'])
def test(c, pyenv):
    """Run tests with Pytest after full setup of each provided Pyenv version."""
    # Note that this task will leave a developer in the last specified version of Python
    # run the test suite for all of the provided versions of Python managed by Pyenv
    for current_pyenv in pyenv:
        print("Python version: " + current_pyenv)
        # select current_pyenv as the version of Python
        c.run("pyenv local " + current_pyenv)
        # create the virtualenv managed by Pipenv with current_pyenv
        c.run("pipenv install --skip-lock --python=`pyenv which python` --dev")
        # display diagnostic information about new version of Python
        c.run("python --version")
        # run the test suite and collect coverage information
        c.run("pipenv run cover")
