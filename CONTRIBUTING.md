# How to Contribute

Thank you for taking time to contribute to GatorGrader! This guide should help
you effectively do so by following the systems already in place for maintaining
the repository.

## Table of Contents

* [Code of Conduct](#code-of-conduct)
* [Raising an Issue](#raising-an-issue)
* [Making a Pull Request](#making-a-pull-request)
* [Coding Standards](#coding-standards)
  * [Code Style](#code-style)
  * [Testing](#testing)
* [Updating .gitignore File](#updating_.gitignore_file)
* [External Resources](#external-resources)

## Code of Conduct

This repository and everyone contributing to is subject to follow the adopted
[code of conduct](CODE_OF_CONDUCT.md). Should you choose to contribute, the
project's maintainers will expect you to uphold this code. Please report any
violations to [@gkapfham](https://github.com/gkapfham).

## Raising an Issue

First, check the [Issue
Tracker](https://github.com/GatorEducator/gatorgrader/issues) to make sure it
that someone has not already raised your issue. If you have a new issue to
raise, go ahead and [raise
it](https://github.com/GatorEducator/gatorgrader/issues/new/choose)! At this
point you should decide if your issue is a "Bug report" or a "Feature request"
and then click the green "Get started" button. Please follow the provided
template when you are describing your issue.

## Making a Pull Request

If you have a new feature or bug fix that you want to the project maintainers to
merge into GatorGrader, then you should make a [pull
request](https://github.com/GatorEducator/gatorgrader/pulls). Please follow the
provided template when you are describing your pull request, bearing in mind
that the project maintainers will not merge any pull requests that do not adhere
to the template or break the any aspects of the automated build. You should read
the following subsection to learn more about the coding standards to which all
of GatorGrader's contributors adhere.

## Project Standards

### Development Environment

If you want to participate in the development of GatorGrader, the project
maintainers suggest the use of [Pyenv](https://github.com/pyenv/pyenv) to
install Python 3.6 or above. In addition to installing
[Git](https://git-scm.com/) to access the project's GitHub repository, you
should also install [Pipenv](https://github.com/pypa/pipenv) for its support of
package and virtual environment management. The project's maintainers do not
require the use of a specific text editor on integrated development environment.
Once you have installed Git, Pyenv, and Pipenv, you can type the following
command in your terminal window to clone GatorGrader's GitHub repository:

```bash
git clone https://github.com/GatorEducator/gatorgrader.git
```

If you are not already a member of GatorGrader's development team, then we
suggest that you fork its GitHub repository and use it for the work that you
intend to contribute. If you plan to develop new features for GatorGrader or if
you want to run the tool's test suite in
[Pytest](https://github.com/pytest-dev/pytest), then you will need to install
the developer dependencies by typing `pipenv install --dev` in the directory
that contains GatorGrader. If you want to use GatorGrader, then you can type
`pipenv install` instead.

### Automated Testing

The developers use [Pytest](https://docs.pytest.org/en/latest/) for testing
GatorGrader. There are several different ways in which you can run the provided
test suite. If you want to run the test suite to see if the test cases are
passing, then you can type this command in a terminal window.

```bash
pipenv run test
```

### Test Coverage

Along with running the test suite, the developers of GatorGrader use statement
and branch coverage to inform their testing activities. Please make sure that
you maintain 100% statement and branch coverage as you add new features or
introduce bug fixes. If it is not possible for you to maintain complete
statement and branch coverage, please document the circumstances in your pull
request. To see the coverage of the tests while also highlighting the lines that
are not currently covered by the tests, you can type this command in a terminal
window.

```bash
pipenv run cover
```

### Code Linting

The developers of GatorGrader use linting and code formatting tools, such as
[Pylint](https://github.com/PyCQA/pylint),
[Pydocstyle](https://github.com/PyCQA/pydocstyle), and
[Black](https://github.com/python/black). Please make sure that the source code
in your pull request fully adheres to the project's coding standard as enforced
by all of the automated linting tools. If it is not possible for you to maintain
compliance with these tools, then please document the circumstances in your pull
request. If you have installed GatorGrader's development dependencies with
Pipenv, you can run all of the linters by typing this command in a terminal
window.

```bash
pipenv run lint --check
```

### Continuous Integration

GatorGrader is a Python 3 application that we build and test in Linux and MacOS
on Travis CI and in Windows on AppVeyor. Whenever feasible, we run all tests and
checks on all three of these operating systems and the most recent version of
Python versions 3.6 and 3.7

## External Resources

GatorGrader's creators give presentations about the development, use, and
assessment of the tool. To better understand the goals of GatorGrader, you can
review the following list of presentations given by our team.

- [A Hands-on Guide to Teaching Programming with GitHub, Travis CI, and Python](https://speakerdeck.com/gkapfham/a-hands-on-guide-to-teaching-programming-with-github-travis-ci-and-python) <br> *at PyOhio 2018*
- [Using GitHub, Travis CI, and Python to Introduce Collaborative Software Development](https://speakerdeck.com/gkapfham/using-github-travis-ci-and-python-to-introduce-collaborative-software-development) <br> *at PyCon Education Summit 2018*
- [Using Python, Travis CI, and GitHub to Effectively Teach Programming](https://speakerdeck.com/gkapfham/using-python-travis-ci-and-github-to-effectively-teach-programming) <br> *at PyGotham 2018*
