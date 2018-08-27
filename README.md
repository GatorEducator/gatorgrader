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

Finally, if you are developing new features for GatorGrader, please attempt to
preserve the high levels of statement coverage achieved by the test suite. The
GatorGrader development team uses [CodeCov.io](https://codecov.io/) to track the
coverage of the tests and, without a thorough justification from new
contributors, will not agree to merge new source code into the master branch
unless it is covered by the test suite. With that said, a recent run of the test
suite yielded the following output. If you do not see output that looks like
this when you run the tests in your development environment, then please raise
an issue in the issue tracker! 

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

GatorGrader can automatically perform simple checks on both writing and source
code. You can learn about GatorGrader's checks and defaults by typing `pipenv
run python3 gatorgrader.py --help` in your terminal window and then reviewing
the following output, observing that the tool can, for instance, inspect a
command's output or the source code of a Java or Python program.

```
usage: gatorgrader.py [-h] [--nowelcome] [--json] [--commits COMMITS]
                      [--directory DIR] [--file FILE] [--exists]
                      [--single COUNT] [--multiple COUNT]
                      [--language {Java,Python}] [--paragraphs COUNT]
                      [--words WORDS] [--command COMMAND] [--executes]
                      [--fragment FRAGMENT] [--count COUNT] [--exact]

optional arguments:
  -h, --help            show this help message and exit
  --nowelcome           do not display the welcome message (default: False)
  --json                print reports in JSON (default: False)
  --commits COMMITS     minimum number of git commits (default: None)
  --directory DIR       directory with file for checking (default: None)
  --file FILE           file for checking (default: None)
  --exists              does a file in a directory exist (default: False)
  --single COUNT        minimum number of single comments (default: None)
  --multiple COUNT      minimum number of multi comments (default: None)
  --language {Java,Python}
                        language for the single comments (default: None)
  --paragraphs COUNT    minimum number of paragraphs (default: None)
  --words WORDS         minimum number of words in paragraphs (default: None)
  --command COMMAND     command to run (default: None)
  --executes            does a command execute without error (default: False)
  --fragment FRAGMENT   fragment that exists in code or output (default: None)
  --count COUNT         how many of an entity should exist (default: None)
  --exact               equals instead of a minimum number (default: False)

```

GatorGrader employs many checks to ensure that you configure it with the correct
command-line arguments. For instance, if you type the command `pipenv run
python3 gatorgrader.py --command ls --fragment pytest --count 1 --exacts` (which
spells the argument as `--exacts` instead of `--exact`), then you will receive
the following error message `gatorgrader.py: error: unrecognized arguments:
--exacts`. While a command like  `pipenv run python3 gatorgrader.py --fragment
pytest --count 1 --exact` uses the correct names for all of the specified
arguments, it does not tell GatorGrader what type of deliverable to check (e.g.,
a program's source code or a command's output), thus leading GatorGrader to
report `Incorrect command-line arguments`.

Since GatorGrader's commands support many different checks for the various for a
computer science project, this documentation will walk through several example
commands. Using these examples, you are encouraged to try out new combinations
of the arguments. If you notice any problems with using GatorGrader, the tool's
developers ask that you raise an issue on the issue tracker. To start, the
following command uses GatorGrader to ensure that the `internal/java` directory
contains the file called `Sample.java` and the subsequent commands check that
this file contains at least two single-line comments (e.g., those lines that
start with `//`) and two multiple-line comments (e.g., content that is
surrounded by `/** */`).


Since computer science courses at Allegheny College require students to
write technical documents, GatorGrader also provides a feature to check how many
paragraphs of writing are in a file. The following example shows how to use
GatorGrader to ensure that the `README.md` file in the root of this repository
contains at least four paragraphs of writing.


Each of the previous commands were run on an Ubuntu 16.04 workstation running
Python 3.6. However, GatorGrader should run correctly on a wide variety of
operating systems that support Python version 3.

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
