"""Run tasks that support easy testing across multiple Python versions."""

from invoke import task


@task(iterable=['pyenv'])
def test(c, pyenv):
    """Run tests with Pytest after full setup of each provided Pyenv version."""
    for current_pyenv in pyenv:
        print("Python version: " + current_pyenv)
        # select current_pyenv as the version of Python
        c.run("pyenv local " + current_pyenv)
        # create the virtualenv managed by Pipenv with current_pyenv
        c.run("yes | pipenv install --python=`pyenv which python` --dev")
        # display diagnostic information about new version of Python
        c.run("python --version")
        # run the test suite and collect coverage information
        c.run("pipenv run cover")
