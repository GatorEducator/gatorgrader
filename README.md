# GatorGrader

![Image of Logo](https://raw.githubusercontent.com/GatorEducator/gatorgrader/master/.github/gatorgraderlogotitled.png)

<p align="center">
<b>
The only tool you'll need to ensure your student's code and writing is up to
speed!
</b>
</p>

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-orange.svg)](https://github.com/GatorEducator/gatorgrader/graphs/commit-activity) [![GitHub license](https://img.shields.io/github/license/GatorEducator/gatorgrader.svg)](https://github.com/GatorEducator/gatorgrader/blob/master/LICENSE.md) [![All Contributors](https://img.shields.io/badge/all_contributors-33-orange.svg?style=flat-square)](#contributors)

## Quickstart Guide

- Starter Repositories
  An easy way to get started with GatorGrader is to check out our sample starter repositories.
  The following starter repositories provide examples of how GatorGrader files should be created
  to check programs and documentation for different languages:
  [Java](https://github.com/GatorEducator/java-assignment-starter-100-01),
  [Python](https://github.com/GatorEducator/python-assignment-starter-203-05), [LaTeX](https://github.com/GatorEducator/latex-assignment-starter-100-01) and [HTML with CSS](https://github.com/GatorEducator/html-assignment-starter-302-03). These
  examples also show how to integrate GatorGrader with [GitHub
  Classroom](https://classroom.github.com/) and [Travis
  CI](https://travis-ci.com/). When you follow these examples, the Gradle plugin
  for GatorGrader will install it automatically when you run `gradle grade` in a
  terminal window. Please be aware that these repositories are meant to have a majority
  of red checks. This is only meant to be a “starter” and give an insight into what must be accomplished within the lab.
- Solution Repositories
  The next step to get involved with GatorGrader is to checkout our sample solution
  repositories. The following solution repositories provide examples of how GatorGrader files should be
  created to check programs and documentation for different languages:
  [Java](https://github.com/GatorEducator/java-assignment-solution-100-01),
  [Python](https://github.com/GatorEducator/python-assignment-solution-203-05), [LaTex](https://github.com/GatorEducator/latex-assignment-solution-100-01) , and [HTML with CSS](https://github.com/GatorEducator/html-assignment-solution-302-03). These examples
  also show how to integrate GatorGrader with [GitHub
  Classroom](https://classroom.github.com/) and [Travis
  CI](https://travis-ci.com/). When you follow these examples, the Gradle plugin
  for GatorGrader will install it automatically when you run `gradle grade` in a
  terminal window. Please be aware that these repositories are meant to have a majority
  of green checks. This is meant to show what must be accomplished within a lab/practical
  and what it looks like when those tasks are completed.

## Key Features

GatorGrader automatically checks the work of technical writers and programmers.
It can:

- Enable [GatorGrade](https://github.com/GatorEducator/gatorgrade) to check
  projects implemented and documented in a wide variety of languages (e.g.,
  Java, Python, LaTeX, Markdown, HTML, and CSS).

- Integrate with [GitHub Classroom](https://classroom.github.com/) to check
  solution and starter repositories created for professors and students,
  respectively.

- Run in a cloud-based environment like [Travis CI](https://travis-ci.com/) or
  on the command-line of a developer's workstation.

- Operate as a "batteries included" grading tool, supporting automated checks
  like the following:

  - Does a file exist in the correct directory with the requested name?

  - Does technical writing contain the desired number of words and paragraphs?

  - Does source code contain the designated number of language-specific comments?

  - Does source code or technical writing contain a required fragment or match
    a specified regular expression?

  - Does a command execute correctly and produce the expected number of output
    lines?

  - Does a command execute and produce output containing a fragment or matching
    a regular expression?

  - Does a GitHub repository contain the anticipated number of commits?

Aligning with key recommendations in a recent [National Academies
report](https://www.nap.edu/catalog/24926/assessing-and-responding-to-the-growth-of-computer-science-undergraduate-enrollments),
GatorGrader helps instructors automatically check student submissions in both
introductory and application-oriented classes using languages like Markdown,
Java, Python, JavaScript, CSS, and HTML. GatorGrader does not aim to solve
problems related to building and linting a project or managing an assignment's
submission, instead integrating with existing tools and systems like
[Gradle](https://gradle.org/), [GitHub](https://github.com/), and [GitHub
Classroom](https://classroom.github.com/) to effectively handle those tasks.

## Installing GatorGrader

Installing GatorGrader is not necessary if you intend to use it through [GatorGrade](https://github.com/GatorEducator/gatorgrade).
If you want to participate in the development of GatorGrader, you should
first install [Git](https://git-scm.com/) to access the project's GitHub
repository and [uv](https://docs.astral.sh/uv/) for its support of fast
package and virtual environment management. After completing the installation
of these tools, you can type the following command in your terminal window to
clone GatorGrader's GitHub repository:

```bash
git clone https://github.com/GatorEducator/gatorgrader.git
```

If you plan to develop new features for GatorGrader or if you want to run the
tool's test suite in [Pytest](https://github.com/pytest-dev/pytest), then you
will need to install a virtual environment for development by typing `uv sync`
in the directory that contains GatorGrader. For help with this process, refer to
[uv's documentation](https://docs.astral.sh/uv/).

## Testing GatorGrader

### Automated Testing

The developers use [Pytest](https://docs.pytest.org/en/latest/) for the testing
of GatorGrader. Depending on your goals, there are several different
configurations in which you can run the provided test suite. If you want to run
the test suite to see if the test cases are passing, then running this command
in a terminal window will perform testing with the version of Python with which
uv's virtual environment was initialized.

```
uv run task test
```

### Test Coverage

Along with running the test suite, the developers of GatorGrader use statement
and branch coverage to enhance their testing activities. To see the coverage of
the tests while also highlighting the lines that are not currently covered by
the tests, you can run this command in a terminal window. As with the previous
command, this will run the tests in the version of Python with which uv's
virtual environment was initialized.

```
uv run task cover
```

### Testing with Multiple Python Versions

The previous two commands run the test suite in the version of Python with
which uv was initialized. If you want to run the test suite against a
different Python version, you can switch uv's Python version before running
the task:

```bash
uv python pin <python-version>
uv run task test
```

For example, to test with Python 3.12:

```bash
uv python pin 3.12
uv run task test
```

### Code Linting

The developers of GatorGrader use [Ruff](https://docs.astral.sh/ruff/) for
linting and code formatting, along with additional tools like
[bandit](https://github.com/PyCQA/bandit) for security analysis,
[radon](https://github.com/rubik/radon) for complexity metrics, and
[xenon](https://github.com/rubik/xenon) for code quality thresholds.
After installing GatorGrader's development dependencies with uv, you can
run all of the linters by typing this command in a terminal window:

```bash
uv run task lint
```

You can also run individual linters as needed:

```bash
uv run task lint-ruff       # ruff linting
uv run task lint-ruff-format # ruff formatting check
uv run task lint-bandit     # security analysis
uv run task lint-xenon      # code quality thresholds
```

### Automated Checks

Want to learn about our linting checks? Check us out on our website,
[GatorGrader](https://www.gatorgrader.org/)! We have detailed
descriptions of our linting checks and more! To get an idea of the linting checks we
offer, here is a quick list:

1. ConfirmFileExists

1. CountCommandOutput

1. CountCommits

1. CountFileLines

1. CountFileParagraphs

Want to learn about our automated checks? Check them out on our website,
[gatorgrader.org](http://www.gatorgrader.org)! We have detailed
descriptions of our automated checks and more!

Something you should know when working with our checks is that all of
them come with some **optional arguments**. Optional arguments that you are likely
to encounter:

- `-h`
- `--help`
- `--exact`
- `--advanced`

If `--help` is tagged along with a check then a help message will be displayed and
then exited. If further assistance is needed, please contact us on GitHub.

Another feature with our automated checks is the **plug-in based approach**. This allows
users to implement their own check if our initial checks do not fulfill a check that
you find necessary.

## Running GatorGrader

Students and instructors normally use GatorGrader through [GatorGrade](https://github.com/GatorEducator/gatorgrade),
specifying the requested checks in a `gatorgrade.yml` file. When run through GatorGrade, GatorGrader
reports each check that it performed, additionally sharing a diagnostic message
for each check that did not pass. Individuals who want to run GatorGrader as a
stand-alone Python application can install GatorGrader itself through [Pipx](https://pypa.github.io/pipx/),
and then run `gatorgrader --help` to get more details on the command-line interface.

Instructors often run GatorGrader in conjunction with other tools that check
source code and technical writing. For instance, in a Java-based introductory
course, instructors could verify student submissions with
[Checkstyle](https://github.com/checkstyle/checkstyle), thereby ensuring that
the Java source code adheres to the requirements in the [Google Java Style
Guide](https://google.github.io/styleguide/javaguide.html). In this course, an
instructor could require that Markdown files with technical writing meet the
standards described in the [Markdown Syntax
Guide](https://guides.github.com/features/mastering-markdown/), meaning that all
Markdown files must pass the checks performed by the [Markdown linting
tool](https://github.com/markdownlint/markdownlint). These assignments could
also require that all submitted technical writing must adhere to the standards
set by the [Proselint tool](http://proselint.com/). Since GatorGrader can run an
arbitrary command and check its error code, it is also possible to integrate it
with a wide variety of other linters, code formatters, and testing tools.

Instructors may at times need to see a full list of checks to have a better understanding
and therefore, we feel that it is important to know that there is an easy way for that to happen.
This action will be completed through command line and therefore, you can type
`gatorgrader ListChecks` into your terminal, if you've installed GatorGrader as detailed above.
This allows for all of the checks to be printed out as output. This output will have the necessary
name labeled with the required and optional arguments. If this output does not give enough content,
we warmly invite you to navigate to our website, where we go into more detail about our Automated Checks.

## Using Docker

_Note: Docker supports the older GatorGrader execution tool, [GatorGradle](https://github.com/GatorEducator/gatorgradle). It is not needed for GatorGrade!_

A vital part of our process for GatorGrader is to implement and use new techniques
to further our tool to grow. This is why we chose to use Docker! Docker is a container
platform and therefore, allows students using GatorGrader to just open a container
and have easy access to run all commands that would allow them to build, run, and
grade their labs and practicals. Docker is an industry standard and therefore,
gives us an advantage. To open a container that will allow for the use of GatorGrader,
run the following command in your terminal window:

```
docker run -it --rm --name dockagator \
  -v "$(pwd)":/project \
  -v "$HOME/.dockagator":/root/.local/share \
  gatoreducator/dockagator /bin/bash
```

From here, you are set! Test it out by building, running, or grading your lab/practical!
If you would like to learn more about Docker, please follow this [link](https://www.docker.com).

## Comparison to Other Tools

Other automated grading tools include:

- [autograde-github-classroom](https://github.com/apanangadan/autograde-github-classroom): "scripts to download and grade submissions to Github Classroom"
- [check50](https://github.com/cs50/check50): "a tool for checking student code"
- [Classroom Assistant](https://classroom.github.com/assistant): "desktop application to help you get student repositories for grading"
- [nbgrader](https://github.com/jupyter/nbgrader): "a system for assigning and grading notebooks"
- [nerfherder](https://github.com/kevinwortman/nerfherder): "scripts for automating grading with GitHub Classroom and Moodle"
- [Submitty](https://github.com/Submitty/Submitty): "homework submission, automated grading, and TA grading system"
- [WebCat](https://github.com/web-cat): "all-in-one plugin for full processing and feedback generation"

Designed for instructors who want an alternative to simple scripts or
stand-alone platforms that do not integrate with industry-standard
infrastructure like GitHub and Travis CI, GatorGrader is a tool that
automatically checks the work of technical writers and programmers. Unlike other
systems, GatorGrader provides a "batteries included" approach to automated
grading that makes it easy for instructors to combine well-tested checks for
projects that students implement in a wide variety of programming languages.
GatorGrader's developers take its engineering seriously, maintaining
standards-compliant source code, a test suite with 100% statement and branch
coverage, and top-notch source code and user documentation.

## Presentations

GatorGrader's creators give presentations about the development, use, and
assessment of the tool. Please contact one of the developers if you would like
to feature a presentation about GatorGrader at your technical conference. The
following list includes some of our team's recent presentations:

- [A Hands-on Guide to Teaching Programming with GitHub, Travis CI, and Python](https://speakerdeck.com/gkapfham/a-hands-on-guide-to-teaching-programming-with-github-travis-ci-and-python) <br> *at PyOhio 2018*
- [Using GitHub, Travis CI, and Python to Introduce Collaborative Software Development](https://speakerdeck.com/gkapfham/using-github-travis-ci-and-python-to-introduce-collaborative-software-development) <br> *at PyCon Education Summit 2018*
- [Using Python, Travis CI, and GitHub to Effectively Teach Programming](https://speakerdeck.com/gkapfham/using-python-travis-ci-and-github-to-effectively-teach-programming) <br> *at PyGotham 2018*

## Contributing

Are you interested in contributing to
[GatorGrader](https://github.com/GatorEducator/gatorgrader),
[GatorGradle](https://github.com/GatorEducator/gatorgradle), or any of the
sample assignments (e.g.,
[Java](https://github.com/GatorEducator/java-assigment-starter),
[LaTeX](https://github.com/GatorEducator/latex-assignment-starter), or [HTML
with CSS](https://github.com/GatorEducator/html-css-assignment-starter))? Great,
because we appreciate the involvement of new contributors! Before you raise an
issue or start to make a contribution to GatorGrader's repository, we ask that
you review the project's [code of conduct](CODE_OF_CONDUCT.md) and the
[contribution guidelines](CONTRIBUTING.md).
