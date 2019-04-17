# Gator Grader

![Image of Logo](https://raw.githubusercontent.com/GatorEducator/gatorgrader/master/.github/gatorgraderlogo.png)

<center>The only tool you'll need to ensure your code is up to speed! GatorGrader
provides all the necessary checks for your code, from linting to searching
commit messages. Whenever you feel in doubt, know GatorGrader is there to
help.</center>

[![Build Status](https://api.travis-ci.org/GatorEducator/gatorgrader.svg?branch=master)](https://travis-ci.org/GatorEducator/gatorgrader) [![codecov.io](http://codecov.io/github/GatorEducator/gatorgrader/coverage.svg?branch=master)](http://codecov.io/github/GatorEducator/gatorgrader?branch=master) [![All Contributors](https://img.shields.io/badge/all_contributors-32-orange.svg?style=flat-square)](#contributors) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-orange.svg)](https://www.python.org/)

## Key Features

* Automatically checks and assesses the work of writers and programmers through the use of different linting tools.
  * Can check for a specified required minimum number of git commits.
  * Can check to see if required files exist and are in the correct directory, and that the directory exists.
  * Can check for a specified number of single line or multi-line comments in source code.
  * Can check the number of words and paragraphs in Markdown files.
  * Can check for specified sentence fragments along with pure text and regular expression fragments within Markdown files and
    source code.
* Can be use with any text-based programming language or document.
* Effectively integrates into many diverse workflows and development environments.
* Can use GatorGrader in a cloud base environment (Travis CI) or local machine through command-line.
* Can be used in conjunction with [GatorGradle](https://github.com/GatorEducator/gatorgradle)
  to support checking gradle projects and "solution" and "starter" GitHub Classroom repositories in GitHub Classroom Assignments.

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
grading tools, GatorGrader does not aim to solve problems related to building a
project or managing an assignment's submission, instead relying on existing
tools that can effectively handle those tasks.

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
runs. You may skip the *Dependencies* subsection if you have Python 3 and Pipenv
installed. You should also ensure that you have installed Git on your computer
and that you can run Git commands in a terminal window. Then, you can type the
following command in your terminal window to clone GatorGrader's GitHub
repository:

```
git clone https://github.com/GatorEducator/gatorgrader.git
```

If you plan to develop new features for GatorGrader or if you want to run the
tool's test suite in [Pytest](https://github.com/pytest-dev/pytest), then you
will need to install the developer dependencies by typing `pipenv install
--dev` in the directory that contains GatorGrader. If you only want to use
GatorGrader, then you can use `pipenv install` instead. It is worth noting that
if you only plan to use GatorGrader with
[GatorGradle](https://github.com/GatorEducator/gatorgradle) then there are
several sample laboratories including:
[Java ](https://github.com/GatorEducator/java-starter),
[LaTeX](https://github.com/GatorEducator/latex-assignment-starter), &
[HTML with CSS](https://github.com/GatorEducator/html-css-assignment-starter)
that you can try &mdash; they do not require you to complete these steps and
instead it will download and install GatorGrader and run all of the
preconfigured checks when you type `gradle grade` in your terminal window.

### Dependencies

Python comes pre-installed on many different distributions, and is available as
a package on most systems. However, there are certain features you might want
to use that are not available on your distro’s package. Simply google `python
download` for your OS or follow the download and installation instructions on
[the Python website](https://www.python.org/).

[Pipenv](https://github.com/pypa/pipenv) is used by GatorGrader to create a
virtual environment, install and manage packages, and run Python commands. To
learn how to install and use Pipenv, please refer to the [Pipenv
Documentation](https://pipenv.readthedocs.io/en/latest/install/).

## Testing GatorGrader

GatorGrader uses [Pytest](https://docs.pytest.org/en/latest/) for testing.
Depending on your goals, there are several different configurations in which you
can run the provided test suite. If you want to run the test suite to see if all
of the test cases are correctly passing, then you can type one of the following
commands in your terminal window:

```
pipenv run pytest
```

```
pipenv run test
```

Please note that you must preface the execution of the test suite with the
command `pipenv run` if you want to ensure that the tests run with the correct
access to their Python packages and in the desired virtual environment. The first
command runs `pytest` explicitely, while the second utilizes `pytest-xdist`. If you
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
pipenv run cover
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

 ----------- coverage: platform linux, python 3.6.7-final-0 -----------
 Name                   Stmts   Miss  Cover   Missing
 ----------------------------------------------------
 gator/__init__.py          0      0   100%
 gator/arguments.py       131      0   100%
 gator/comments.py         17      0   100%
 gator/display.py          15      0   100%
 gator/entities.py         13      0   100%
 gator/files.py             5      0   100%
 gator/fragments.py        90      0   100%
 gator/invoke.py          110      0   100%
 gator/leave.py             4      0   100%
 gator/orchestrate.py     114      0   100%
 gator/report.py           71      0   100%
 gator/repository.py       13      0   100%
 gator/run.py              29      0   100%
 gator/util.py             35      0   100%
 ----------------------------------------------------
 TOTAL                    647      0   100%


 Results (1.48s):
      455 passed
```

if you would like to run a specific test run

```
pytest test_mod.py::name-of-test-function
```
OR

```
pytest test_mod.py::TestClass::name-of-test_method
```

The -r options accepts a number of characters after it, with a used above meaning “all except passes”.

Here is the full list of available characters that can be used:

-  f - failed
-  E - error
-  s - skipped
-  x - xfailed
-  X - xpassed
-  p - passed
-  P - passed with output
-  a - all except pP

More than one character can be used, so for example to only see failed and skipped tests, you can execute:

```
$ pytest -rfs
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR, inifile:
collected 6 items

test_example.py .FEsxX                                               [100%]

================================== ERRORS ==================================
_______________________ ERROR at setup of test_error _______________________

    @pytest.fixture
    def error_fixture():
>       assert 0
E       assert 0

test_example.py:6: AssertionError
================================= FAILURES =================================
________________________________ test_fail _________________________________

    def test_fail():
>       assert 0
E       assert 0

test_example.py:14: AssertionError
========================= short test summary info ==========================
FAILED test_example.py::test_fail
SKIPPED [1] $REGENDOC_TMPDIR/test_example.py:23: skipping this test
 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 xpassed, 1 error in 0.12 seconds
Using p lists the passing tests, whilst P adds an extra section “PASSES” with those tests that passed but had captured output:

$ pytest -rpP
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-4.x.y, py-1.x.y, pluggy-0.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR, inifile:
collected 6 items

test_example.py .FEsxX                                               [100%]

================================== ERRORS ==================================
_______________________ ERROR at setup of test_error _______________________

    @pytest.fixture
    def error_fixture():
>       assert 0
E       assert 0

test_example.py:6: AssertionError
================================= FAILURES =================================
________________________________ test_fail _________________________________

    def test_fail():
>       assert 0
E       assert 0

test_example.py:14: AssertionError
========================= short test summary info ==========================
PASSED test_example.py::test_ok
================================== PASSES ==================================
_________________________________ test_ok __________________________________
--------------------------- Captured stdout call ---------------------------
ok
 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 xpassed, 1 error in 0.12 seconds
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
                      [--fragment FRAGMENT] [--regex REGEX]
                      [--markdown MARKDOWN] [--count COUNT] [--exact]

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
  --regex REGEX         regular expression that exists in code or output
                        (default: None)
  --markdown MARKDOWN   markdown tag that exists in a file (default: None)
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

Since GatorGrader's commands support many different checks for the various
deliverables of a project in a computer science course, this documentation will
walk through several example commands. Using these examples, you are encouraged
to try out new combinations of the arguments. If you notice any problems with
using GatorGrader, the tool's developers ask that you raise an issue on the
issue tracker. To start, the following command uses GatorGrader to ensure that
the `internal/java` directory contains the file called `Sample.java` and the
subsequent commands check that this file contains at least two single-line
comments (e.g., those lines that start with `//`) and two multiple-line comments
(e.g., content that is surrounded by `/** */`). In these and the remaining
examples, you will first see the command and then the output that it produces.
Finally, while in practice you would normally type these commands on a single
line in your terminal window, we give them on multiple lines to ensure that
they are easily viewed on a wide variety of displays.

```
$ pipenv run python3 gatorgrader.py \
--directory internal/java \
--file Sample.java \
--exists

✔ GatorGrader: Automatically Check the Files of Programmers and Writers
https://github.com/GatorEducator/gatorgrader

✔ The file Sample.java exists in the internal/java directory
```

```
$ pipenv run python3 gatorgrader.py \
--directory internal/java \
--file Sample.java \
--single 1 \
--language Java

✔ GatorGrader: Automatically Check the Files of Programmers and Writers
https://github.com/GatorEducator/gatorgrader

✔ The Sample.java in internal/java has at least 1 single-line Java comment(s)
```

```
$ pipenv run python3 gatorgrader.py \
--directory internal/java \
--file Sample.java \
--multiple 1 \
--language Java

✔ GatorGrader: Automatically Check the Files of Programmers and Writers
https://github.com/GatorEducator/gatorgrader

✔ The Sample.java in internal/java has at least 1 multiple-line Java comment(s)
```

Since computer science courses at the developers' institution require students
to write technical documents, GatorGrader also provides a feature to check how
many words are in each of the paragraphs or how many times a word appears in the
text. The following examples show how to use GatorGrader to ensure that the
`README.md` file in this repository contains at least and then exactly 10
appearances of the word "GatorGrader". The third example in this listing shows
how GatorGrader can check for the number of paragraphs in technical writing.

```
$ pipenv run python3 gatorgrader.py \
--file README.md \
--directory . \
--fragment GatorGrader \
--count 10

✔ GatorGrader: Automatically Check the Files of Programmers and Writers
https://github.com/GatorEducator/gatorgrader

✔ The README.md in . has at least 10 of the 'GatorGrader' fragment
```

```
$ pipenv run python3 gatorgrader.py \
--file README.md \
--directory . \
--fragment GatorGrader \
--count 10 \
--exact

✔ GatorGrader: Automatically Check the Files of Programmers and Writers
https://github.com/GatorEducator/gatorgrader

✘ The README.md in . has exactly 10 of the 'GatorGrader' fragment
   ➔ Found 56 fragment(s) in the output or the specified file
```

```
$ pipenv run python3 gatorgrader.py \
--file README.md \
--directory . \
--paragraphs 40 \
--exact

✔ GatorGrader: Automatically Check the Files of Programmers and Writers
https://github.com/GatorEducator/gatorgrader

✘ The README.md in . has exactly 40 paragraph(s)
   ➔ Found 36 paragraph(s) in the specified file
```

Each of the previous commands were run on an Ubuntu 16.04 workstation running
Python 3.6.6. However, GatorGrader should run correctly on a wide variety of
operating systems that support Python version 3. It is also important to note
that, in adherence to GatorGrader's design philosophy, each of the previous
checks inspect a single aspect of the solution to a programming project.
Finally, to ensure that it integrates effectively with [Travis
CI](https://travis-ci.com/), GatorGrader returns a non-zero exit code when its
check fails, ensure that the continuous integration system will fail the build
as soon as a single check does not pass. That is, if you ran the previous
GatorGrader check and then then command `echo $?` you would see that GatorGrader
returned the value of `1`.

## GatorGrader in Action

GatorGrader is commonly used in conjunction with other tools that check source
code and technical writing. For instance, in the introductory computer science
classes at the institution of the developers, the submissions are verified by
[Checkstyle](https://github.com/checkstyle/checkstyle) and thus the Java source
code must adhere to all of the requirements in the [Google Java Style
Guide](https://google.github.io/styleguide/javaguide.html). Moreover, Markdown
files that contain writing must meet the standards described in the [Markdown
Syntax Guide](https://guides.github.com/features/mastering-markdown/), meaning
that all Markdown files must pass the checks performed by the [Markdown linting
tool](https://github.com/markdownlint/markdownlint). Finally, all submitted
technical writing must adhere to the writing standards set by the [Proselint
tool](http://proselint.com/).

The solution repositories for the laboratory and practical assignments in
Computer Science courses at Allegheny College are kept private. However, the
"starter" repositories for assignments are publicly available so as to support
their integration into [GitHub Classroom](https://classroom.github.com/). As
GatorGrader continues to be adopted by more courses, we will expand this list of
GitHub repositories that provide starting code templates. Here are some courses
that have recently used GatorGrader:

- [Computer Science 111 Fall 2017 at Allegheny College](https://github.com/Allegheny-Computer-Science-111-F2017)
- [Computer Science 280 Fall 2017 at Allegheny College](https://github.com/allegheny-computer-science-280-f2017)
- [Computer Science 103 Spring 2018 at Allegheny College](https://github.com/Allegheny-Computer-Science-103-S2018)
- [Computer Science 112 Spring 2018 at Allegheny College](https://github.com/Allegheny-Computer-Science-112-S2018)

## Presentations

GatorGrader's creators give presentations about the development, use, and
assessment of the tool. Please contact one of the developers if you would like
to feature a presentation about GatorGrader at your technical conference. The
following list includes some of our recent presentations:

- [A Hands-on Guide to Teaching Programming with GitHub, Travis CI, and Python](https://speakerdeck.com/gkapfham/a-hands-on-guide-to-teaching-programming-with-github-travis-ci-and-python) <br> *at PyOhio 2018*
- [Using GitHub, Travis CI, and Python to Introduce Collaborative Software Development](https://speakerdeck.com/gkapfham/using-github-travis-ci-and-python-to-introduce-collaborative-software-development) <br> *at PyCon Education Summit 2018*
- [Using Python, Travis CI, and GitHub to Effectively Teach Programming](https://speakerdeck.com/gkapfham/using-python-travis-ci-and-github-to-effectively-teach-programming) <br> *at PyGotham 2018*

## Contributing

Are you interested in contributing to
[GatorGrader](https://github.com/GatorEducator/gatorgrader),
[GatorGradle](https://github.com/GatorEducator/gatorgradle), or
any of the sample labs ([Java](https://github.com/GatorEducator/java-assigment-starter), [LaTeX](https://github.com/GatorEducator/latex-assignment-starter), [HTML with CSS](https://github.com/GatorEducator/html-css-assignment-starter))?
Our development team uses the [GitHub flow
model](https://guides.github.com/introduction/flow/) to guide our engineering of
these tools and we invite you to also follow it as you make a contribution. Of
course, if you have any problems with installing, testing, or using GatorGrader,
then please raise an issue associated with this Git repository using the
"Issues" link at the top of this site. The contributors to GatorGrader will do
all that they can to resolve your issue and ensure that the entire tool works
well in your teaching and development environment.

## Contributors

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
<table><tr><td align="center"><a href="https://www.gregorykapfhammer.com"><img src="https://avatars2.githubusercontent.com/u/926029?v=4" width="64px;" alt="Gregory M. Kapfhammer"/><br /><sub><b>Gregory M. Kapfhammer</b></sub></a><br /><a href="#talk-gkapfham" title="Talks">📢</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=gkapfham" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=gkapfham" title="Documentation">📖</a> <a href="#design-gkapfham" title="Design">🎨</a> <a href="#infra-gkapfham" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=gkapfham" title="Tests">⚠️</a></td><td align="center"><a href="https://saejinmh.com"><img src="https://avatars1.githubusercontent.com/u/5274499?v=4" width="64px;" alt="Saejin Mahlau-Heinert"/><br /><sub><b>Saejin Mahlau-Heinert</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=Michionlion" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=Michionlion" title="Documentation">📖</a> <a href="#infra-Michionlion" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#review-Michionlion" title="Reviewed Pull Requests">👀</a></td><td align="center"><a href="https://github.com/dubswalker"><img src="https://avatars2.githubusercontent.com/u/37150088?v=4" width="64px;" alt="Christian Walker"/><br /><sub><b>Christian Walker</b></sub></a><br /><a href="#content-dubswalker" title="Content">🖋</a></td><td align="center"><a href="https://github.com/everitt-andrew"><img src="https://avatars3.githubusercontent.com/u/31443695?v=4" width="64px;" alt="Andrew Everitt"/><br /><sub><b>Andrew Everitt</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=everitt-andrew" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=everitt-andrew" title="Documentation">📖</a></td><td align="center"><a href="https://www.christianlussier.com"><img src="https://avatars2.githubusercontent.com/u/32375724?v=4" width="64px;" alt="Christian Lussier"/><br /><sub><b>Christian Lussier</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=lussierc" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=lussierc" title="Documentation">📖</a></td><td align="center"><a href="https://www.simon-burrows.com"><img src="https://avatars2.githubusercontent.com/u/25254767?v=4" width="64px;" alt="Simon Burrows"/><br /><sub><b>Simon Burrows</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=burrowss" title="Code">💻</a></td><td align="center"><a href="https://www.austinbristol.com/"><img src="https://avatars1.githubusercontent.com/u/19804014?v=4" width="64px;" alt="Austin Bristol"/><br /><sub><b>Austin Bristol</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=bristola" title="Code">💻</a></td><td align="center"><a href="https://github.com/JattMones"><img src="https://avatars0.githubusercontent.com/u/22432176?v=4" width="64px;" alt="Matt"/><br /><sub><b>Matt</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=JattMones" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=JattMones" title="Documentation">📖</a></td><td align="center"><a href="https://github.com/cmiller365"><img src="https://avatars3.githubusercontent.com/u/27263493?v=4" width="64px;" alt="Christopher Miller"/><br /><sub><b>Christopher Miller</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=cmiller365" title="Code">💻</a> <a href="#design-cmiller365" title="Design">🎨</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=cmiller365" title="Documentation">📖</a></td><td align="center"><a href="http://spencerhuang.netlify.com"><img src="https://avatars0.githubusercontent.com/u/31478964?v=4" width="64px;" alt="Spencer Huang"/><br /><sub><b>Spencer Huang</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=huangs1" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=huangs1" title="Documentation">📖</a></td></tr><tr><td align="center"><a href="https://github.com/ilikerustoo"><img src="https://avatars3.githubusercontent.com/u/25516043?v=4" width="64px;" alt="Mohammad Khan"/><br /><sub><b>Mohammad Khan</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=ilikerustoo" title="Code">💻</a></td><td align="center"><a href="http://www.shafferz.com"><img src="https://avatars1.githubusercontent.com/u/26298864?v=4" width="64px;" alt="Zachary Shaffer"/><br /><sub><b>Zachary Shaffer</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=shafferz" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=shafferz" title="Documentation">📖</a></td><td align="center"><a href="http://alexander.yarkosky.xyz"><img src="https://avatars1.githubusercontent.com/u/36210455?v=4" width="64px;" alt="Alexander Yarkosky"/><br /><sub><b>Alexander Yarkosky</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/issues?q=author%3AAlex-Yarkosky" title="Bug reports">🐛</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=Alex-Yarkosky" title="Documentation">📖</a></td><td align="center"><a href="https://github.com/thomad74"><img src="https://avatars1.githubusercontent.com/u/31478969?v=4" width="64px;" alt="Dillon"/><br /><sub><b>Dillon</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=thomad74" title="Documentation">📖</a></td><td align="center"><a href="http://zacharyleonardo.com"><img src="https://avatars2.githubusercontent.com/u/35816642?v=4" width="64px;" alt="Zachary Leonardo"/><br /><sub><b>Zachary Leonardo</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=leonardoz15" title="Code">💻</a></td><td align="center"><a href="https://github.com/mendezjw"><img src="https://avatars2.githubusercontent.com/u/23535739?v=4" width="64px;" alt="Jonathan W. Mendez"/><br /><sub><b>Jonathan W. Mendez</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=mendezjw" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=mendezjw" title="Documentation">📖</a></td><td align="center"><a href="https://github.com/lylet-AC"><img src="https://avatars3.githubusercontent.com/u/31486141?v=4" width="64px;" alt="Tyler Lyle"/><br /><sub><b>Tyler Lyle</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=lylet-AC" title="Code">💻</a></td><td align="center"><a href="https://github.com/finneyj2"><img src="https://avatars3.githubusercontent.com/u/31444681?v=4" width="64px;" alt="finneyj2"/><br /><sub><b>finneyj2</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=finneyj2" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=finneyj2" title="Documentation">📖</a></td><td align="center"><a href="https://github.com/schultzh"><img src="https://avatars0.githubusercontent.com/u/42979565?v=4" width="64px;" alt="schultzh"/><br /><sub><b>schultzh</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/issues?q=author%3Aschultzh" title="Bug reports">🐛</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=schultzh" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=schultzh" title="Documentation">📖</a> <a href="#review-schultzh" title="Reviewed Pull Requests">👀</a></td><td align="center"><a href="https://github.com/alexheinle"><img src="https://avatars3.githubusercontent.com/u/35603755?v=4" width="64px;" alt="alexheinle"/><br /><sub><b>alexheinle</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/issues?q=author%3Aalexheinle" title="Bug reports">🐛</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=alexheinle" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=alexheinle" title="Documentation">📖</a> <a href="#review-alexheinle" title="Reviewed Pull Requests">👀</a></td></tr><tr><td align="center"><a href="https://github.com/ZachAndrews98"><img src="https://avatars1.githubusercontent.com/u/15204124?v=4" width="64px;" alt="Zachary Andrews"/><br /><sub><b>Zachary Andrews</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=ZachAndrews98" title="Code">💻</a> <a href="#design-ZachAndrews98" title="Design">🎨</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=ZachAndrews98" title="Documentation">📖</a></td><td align="center"><a href="https://github.com/toccinAC"><img src="https://avatars2.githubusercontent.com/u/31412566?v=4" width="64px;" alt="Nicholas Tocci"/><br /><sub><b>Nicholas Tocci</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=toccinAC" title="Documentation">📖</a></td><td align="center"><a href="https://github.com/hodevin"><img src="https://avatars2.githubusercontent.com/u/31478952?v=4" width="64px;" alt="Devin Ho"/><br /><sub><b>Devin Ho</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=hodevin" title="Documentation">📖</a></td><td align="center"><a href="https://github.com/baldeosinghm"><img src="https://avatars0.githubusercontent.com/u/42876742?v=4" width="64px;" alt="Matthew Baldeosingh"/><br /><sub><b>Matthew Baldeosingh</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=baldeosinghm" title="Documentation">📖</a></td><td align="center"><a href="https://durchburch.xyz"><img src="https://avatars2.githubusercontent.com/u/31478922?v=4" width="64px;" alt="Jordan Durci"/><br /><sub><b>Jordan Durci</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=durcij" title="Code">💻</a></td><td align="center"><a href="https://www.linkedin.com/in/karol-vargas-a9a925b8/"><img src="https://avatars0.githubusercontent.com/u/31486084?v=4" width="64px;" alt="Karol Vargas"/><br /><sub><b>Karol Vargas</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=karolvargas" title="Documentation">📖</a></td><td align="center"><a href="https://github.com/cerdamejiaj"><img src="https://avatars3.githubusercontent.com/u/25254696?v=4" width="64px;" alt="Jerfenson Cerda Mejia"/><br /><sub><b>Jerfenson Cerda Mejia</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=cerdamejiaj" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=cerdamejiaj" title="Documentation">📖</a></td><td align="center"><a href="https://github.com/ohnoanarrow"><img src="https://avatars0.githubusercontent.com/u/22673907?v=4" width="64px;" alt="Tara Douglass"/><br /><sub><b>Tara Douglass</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=ohnoanarrow" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=ohnoanarrow" title="Documentation">📖</a></td><td align="center"><a href="https://github.com/ALEXANDERB82"><img src="https://avatars0.githubusercontent.com/u/31444387?v=4" width="64px;" alt="Alexander Butler"/><br /><sub><b>Alexander Butler</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=ALEXANDERB82" title="Code">💻</a></td><td align="center"><a href="https://github.com/corlettim"><img src="https://avatars3.githubusercontent.com/u/35552969?v=4" width="64px;" alt="corlettim"/><br /><sub><b>corlettim</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/issues?q=author%3Acorlettim" title="Bug reports">🐛</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=corlettim" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=corlettim" title="Documentation">📖</a> <a href="#review-corlettim" title="Reviewed Pull Requests">👀</a></td></tr><tr><td align="center"><a href="https://github.com/quigley-c"><img src="https://avatars1.githubusercontent.com/u/35495466?v=4" width="64px;" alt="Carson Quigley"/><br /><sub><b>Carson Quigley</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=quigley-c" title="Code">💻</a></td><td align="center"><a href="https://github.com/yeej2"><img src="https://avatars1.githubusercontent.com/u/22895281?v=4" width="64px;" alt="Joshua Yee"/><br /><sub><b>Joshua Yee</b></sub></a><br /><a href="https://github.com/GatorEducator/gatorgrader/commits?author=yeej2" title="Code">💻</a> <a href="https://github.com/GatorEducator/gatorgrader/commits?author=yeej2" title="Documentation">📖</a></td></tr></table>

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
