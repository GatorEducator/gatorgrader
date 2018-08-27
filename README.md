# GatorGrader

[![Build Status](https://api.travis-ci.org/GatorEducator/gatorgrader.svg?branch=master)](https://travis-ci.org/GatorEducator/gatorgrader) [![codecov.io](http://codecov.io/github/GatorEducator/gatorgrader/coverage.svg?branch=master)](http://codecov.io/github/GatorEducator/gatorgrader?branch=master) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-orange.svg)](https://www.python.org/)

Designed for use with [GitHub](https://github.com/), [GitHub
Classroom](https://classroom.github.com/), [Travis CI](https://travis-ci.com/),
and [Gradle](https://gradle.org/), GatorGrader is an automated assessment tool
that checks the work of programmers and writers. While other tools already exist
to, for instance, enforce a style guide for source code or build a program,
GatorGrader focuses on automating the checks and activities that are not already
nicely supported. For example, GatorGrader can check how many Git commits a
student or a team performed during the completion of an assignment. Along with
checking for the existence of files, the tool can also count a wide variety of
entities in a project submission, including words and paragraphs in technical
writing, comments in source code, and fragments in either source code or program
output. In alignment with key recommendations in a recent [National Academies
report](https://www.nap.edu/catalog/24926/assessing-and-responding-to-the-growth-of-computer-science-undergraduate-enrollments),
instructors have used GatorGrader to automatically check student submissions in
both introductory and application-oriented classes using languages like
Markdown, Java, Python, JavaScript, CSS, and HTML.

Although it can be used independently of a containing project or additional
support tools, GatorGrader is commonly used in conjunction with the
[GatorGradle](https://github.com/GatorEducator/gatorgradle) plugin for the
[Gradle](https://gradle.org/) build tool. It's worth noting that even though
[Gradle](https://gradle.org/) is commonly associated with the Java programming
language, you can use GatorGrader and
[GatorGradle](https://github.com/GatorEducator/gatorgradle) to check the work
that students complete in a wide variety of languages. The tool also effectively
supports the checking of the "solution" and "starter" Git repositories that an
instructor normally builds when creating an assignment in [GitHub
Classroom](https://classroom.github.com/). GatorGrader's simple, yet useful,
automated checks can also be integrated into the continuous integration build
process supported by a system like [Travis CI](https://travis-ci.com/). Since it
is a [Python 3](https://www.python.org/) program that students and instructors
can easily run on the command-line, GatorGrader effectively integrates into many
diverse workflows and development environments. In contrast to other automated
grading tools, GatorGrader does not attempt to solve problems related to
building a project or managing an assignment's submission, instead relying on
existing tools to effectively handle those tasks.

## What Do People Think about GatorGrader?

GatorGrader addresses some of the challenges that an instructor faces when
designing automated checkers for the source code or technical writing that a
student submits through an assignment on [GitHub
Classroom](https://classroom.github.com/). Feedback from the teaching assistants
and students who use GatorGrader has been positive. Here is what people think
about GatorGrader!

> This tool suite made it easier for me to talk with students about
> technical requirements. It helped me to make complex assignments
> more accessible to students. **Maria Kim**

<!-- -->
> GatorGrader encouraged me to add better code comments and try out
> language constructs that I would not have otherwise investigated.
> The tool was a big help this semester! **Samatha Darris**

<!-- -->
> GatorGrader is like having a constant coach! I liked receiving
> feedback on the quality of my source code and writing before
> turning in the final version of my lab. **Anna Yeager**

## Installing GatorGrader

As a Python 3 program, GatorGrader relies on
[Pipenv](https://github.com/pypa/pipenv) for the installation of the libraries
on which it depends and the creation of the virtual environments in which it
runs. To install GatorGrader, you should first follow Pipenv's installation
instructions. You should also ensure that you have installed Git on your
computer and that you can run Git commands in a terminal window. Then, you can
type the following command in your terminal window to clone GatorGrader's GitHub
repository:

```
git clone https://github.com/GatorEducator/gatorgrader.git 
```

If you plan to develop new features for GatorGrader or if you want to run the
tool's test suite in [Pytest](https://github.com/pytest-dev/pytest), then you
will need to install the developer dependencies by typing `pipenv install --dev`
in the directory that contains GatorGrader. If you only want to use GatorGrader,
then you can type `pipenv install` instead. Once these commands complete
successfully, that's all you you have to do to install GatorGrader! It is worth
noting that if you only plan to use GatorGrader with the
[GatorGradle](https://github.com/GatorEducator/gatorgradle) then there is a
[sample laboratory
assignment](https://github.com/GatorEducator/gatorgrader-samplelab) that you can
try &mdash; it does not require you to complete these steps and instead it will
download and install GatorGrader and run all of the preconfigured checks when
you type `gradle grade` in your terminal window.

## Testing GatorGrader

GatorGrader uses [Pytest](https://docs.pytest.org/en/latest/) for testing.
Depending on your goals, there are several different configurations in which you
can run the provided test suite. If you want to run the test suite to see if all
of the test cases are correctly passing, then you can type the following command
in your terminal window:

```
pipenv run pytest
```

Please note that you must preface the execution of the test suite with the
command `pipenv run` if you want to ensure that the tests run with the correct
access to their Python packages and in the desired virtual environment. If you
are using GatorGrader and you find that a test fails in your development
environment, please raise an issue in GatorGrader's issue tracker. With that
said, if you are developing new features for Pytest and you want it to produce
console output and stop when it runs the first failing test, you can type:

```
pipenv run pytest -x -s
```

The developers of GatorGrader used statement coverage to inform their testing of
the tool. To see the current coverage of the tests while also highlighting the
lines that are not currently covered by the tests, you can type this command:

```
pipenv run pytest -x -s --cov-config pytest.cov --cov-report term-missing --cov
```

A recent run of the test suite yielded the following output. If you do not see
output that looks like this when you run the tests in your development
environment, then please raise an issue in the issue tracker!

```
 tests/test_arguments.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓  9% ▉
                         ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓ 18% █▊
                         ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓ 26% ██▋
                         ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓ 35% ███▌
                         ✓✓✓✓✓✓✓✓✓✓                              37% ███▊
 tests/test_comments.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓ 46% ████▋
                        ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓ 55% █████▋
                        ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓               61% ██████▎
 tests/test_display.py ✓✓✓                                       62% ██████▎
 tests/test_files.py ✓✓✓✓                                        63% ██████▍
 tests/test_fragments.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓ 72% ███████▎
                         ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓ 80% ████████▏
                         ✓✓✓                                     81% ████████▎
 tests/test_invoke.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓                     86% ████████▋
 tests/test_leave.py ✓✓✓✓✓✓✓✓✓✓                                  88% ████████▉
 tests/test_orchestrate.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓                     92% █████████▎
 tests/test_report.py ✓✓✓✓✓✓✓✓✓✓✓✓✓                              95% █████████▌
 tests/test_repository.py ✓✓✓✓✓✓                                 96% █████████▋
 tests/test_run.py ✓✓                                            97% █████████▊
 tests/test_util.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓                              100% ██████████

----------- coverage: platform linux, python 3.6.6-final-0 -----------
Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
gator/__init__.py          0      0   100%
gator/arguments.py       131      0   100%
gator/comments.py         17      0   100%
gator/display.py          15      0   100%
gator/entities.py         13      0   100%
gator/files.py             5      0   100%
gator/fragments.py        90      0   100%
gator/invoke.py           99      0   100%
gator/leave.py             4      0   100%
gator/orchestrate.py     109      0   100%
gator/report.py           71      0   100%
gator/repository.py       13      0   100%
gator/run.py              28      2    93%   33-34
gator/util.py             35      0   100%
----------------------------------------------------
TOTAL                    630      2    99%

Results (2.95s):
     444 passed

```

## Running GatorGrader

If your environment supports it, then please set the `GATORGRADER_HOME`
environment variable. For instance, typing the command `export
GATORGRADER_HOME="/home/travis/build/gkapfham/gatorgrader"` would set
`GATORGRADER_HOME` environment variable to the appropriate directory for
building it on Travis CI under the `gkapfham` account. If you do not set the
`GATORGRADER_HOME` environment variable, then GatorGrader will attempt to guess
the best setting for it.

GatorGrader can perform simple checks on both writing and source code. For
instance, the following command uses GatorGrader to ensure that the
`internal/java` directory contains the file called `Sample.java` and that
this file contains at least two single-line comments (e.g., those lines that
start with `//`) and two multiple-line comments (e.g., content that is
surrounded by `/** */`).

```
python3 gatorgrader.py \
        --directories internal/java \
        --checkfiles Sample.java \
        --singlecomments 2 \
        --multicomments 2 \
        --languages Java
```

Since many computer science courses at Allegheny College require students to
write technical documents, GatorGrader also provides a feature to check how many
paragraphs of writing are in a file. The following example shows how to use
GatorGrader to ensure that the `README.md` file in the root of this repository
contains at least four paragraphs of writing.

```
python3 gatorgrader.py \
        --directories . \
        --checkfiles README.md \
        --paragraphs 4
```

Each of the previous commands were run on an Ubuntu 16.04 workstation running
Python 3.6. However, GatorGrader should run correctly on a wide variety of
operating systems that support Python version 3.

## GatorGrader Options

GatorGrader comes equipped with a few commands line arguments that can be used to
configure an individual run of the system. These include:

- `--checkfiles`

Determines which file to look to. This should be followed by the name of a file.

- `--directories`

Tells GatorGrader which path to follow to find the file. This should be followed
 by the filepath to the file.

- `--singlecomments`

Indicates to look for a number of single-line comments. This should be followed
by a number of single-line comments to look for. The language must also be
specified with the `--langauge` option.

- `--multicomments`

Indicates to look for a number of multi-line comments. This should be followed
by the number of multi-line comments to look for. The language must also be
specified with the `--langauge` option.

- `--paragraphs`

Indicates to look for a number of paragraphs in a md file. This should be
followed by the number of paragraphs to check for in the file.

- `--wordcount`

Indicates to look for a number of words in each paragraph in a Markdown file.
Should be followed by the number of words to look for.

- `--fragments`

Looks for a particular fragment in the code. This should be followed by the
fragment to be looked for. This can also be used after a `--commands` flag to
check if the output contains the fragment specified.

- `--fragmentcounts`

Indicates how many times the code must have a fragment. This should be followed
by the number of times the user wants the fragment in the code.

- `--language`

Indicates what language the code snippet will be. This should be followed by a
programming language, such as Java or Python.

- `--commands`

Runs a command; the results can be used further on. This should be
followed by a command such as `"gradle build"`.

- `--outputlines`

Ensures that the program outputs a number of lines. Should be followed by the
number of lines that the user wants output. Used in conjunction with `--commands`.

- `--commits`

Checks that the user commit a number of times. This should be followed by the
number of commits the user would like the student to commit.

## GatorGrader in Action

GatorGrader is commonly used in conjunction with other tools that check source
code. For instance, in the introductory computer science classes at Allegheny
College, the submissions are verified by
[Checkstyle](https://github.com/checkstyle/checkstyle) and thus the Java source
code must adhere to all of the requirements in the [Google Java Style
Guide](https://google.github.io/styleguide/javaguide.html). Moreover, Markdown
files that contain writing must meet the standards described in the [Markdown
Syntax Guide](https://guides.github.com/features/mastering-markdown/), meaning
that all Markdown files must pass the checks performed by the [Markdown linting
tool](https://github.com/markdownlint/markdownlint). Finally, all submitted
technical writing must adhere to the writing standards set by the [Proselint
tool](http://proselint.com/).

The solution repositories for the laboratory assignments in Computer Science
courses at Allegheny College are kept private. However, the "starter"
repositories for assignments are publicly available so as to support their
integration into [GitHub Classroom](https://classroom.github.com/). As
GatorGrader continues to be adopted by more courses, we will expand this list of
GitHub repositories that provide starting code templates and furnish GatorGrader
as a Git submodule.

- [Computer Science 111 Laboratory #1](https://github.com/Allegheny-Computer-Science-111-F2017/cs111-F2017-lab1-starter)

## Acknowledgements

We gratefully acknowledge Nicholas Tocci and Race Mahoney for pointing out that
the GatorGrader submodule did not have a `.gitignore` file, thus causing the
derived Python files and directories to seem to be untracked.

## Problems or Praise

If you have any problems with installing or using GatorGrader, then please
create an issue associated with this Git repository using the "Issues" link at
the top of this site. The contributors to GatorGrader will do all that they can
to resolve your issue and ensure that the entire tool works well in your
teaching and development environment.
