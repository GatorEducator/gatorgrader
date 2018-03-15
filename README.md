# GatorGrader

[![Build Status](https://api.travis-ci.org/gkapfham/gatorgrader.svg?branch=master)](https://travis-ci.org/gkapfham/gatorgrader)

Designed for use with [GitHub Classroom](https://classroom.github.com/),
GatorGrader is an automated grading tool that checks the work of programmers and
writers. Although it can be used independently of a containing project,
GatorGrader is commonly used by faculty in the [Department of Computer Science
at Allegheny College](https://github.com/Allegheny-Computer-Science) as a Git
submodule in a Git repository for a specific assignment. Since it is a Python 3
program that can easily be run on the command-line, GatorGrader also works
nicely with [Travis CI](https://travis-ci.com/) &mdash; which is again how
faculty members at Allegheny College commonly use it in conjunction with other
automated checking tools.

## Installing GatorGrader

As a Python 3 program, GatorGrader relies on
[pip](https://pip.pypa.io/en/stable/installing/) for installation. To ensure
that all of the dependencies are installed correctly, please type
the following commands before running GatorGrader.

- `pip install --upgrade pip`
- `pip install -r requirements.txt`

Note that you may have Python 3 setup in different ways on your computer. For
instance, you may prefer to install GatorGrader's dependencies in a site-wide
location and then you would have to type, for instance, `sudo pip install -r
requirements.txt`. Alternatively, you may choose to install the dependencies by
typing `pip install --user -r requirements.txt`.

GatorGrader was developed to easily run in conjunction with a [venv-based Python
3 virtual environment](https://docs.python.org/3/library/venv.html). This means
that if you are in the directory that contains the `gatorgrader` directory then
you could type `python3 -m venv gatorgrader` to create all of the components of
a venv-based virtual environment in the `gatorgrader` directory. Once you
complete this step, you can type the command `source gatorgrader/bin/activate`
to activate the venv-based virtual environment. Interested in learning more
about the basics of virtual environments in Python 3? You can read this
[article](http://www.cs.allegheny.edu/sites/gkapfham/programming/research/idea/2017/07/14/Virtual-Environments/)
to further develop your understanding of this topic.

## Testing GatorGrader

GatorGrader uses [pytest](https://docs.pytest.org/en/latest/) for testing. To
run GatorGrader's comprehensive test suite of over 150 test cases, please type
`pytest tests` in the root of the project's repository. If any of the test cases
fail in your development environment, please please raise an issue in
GatorGrader's issue tracker.

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

Since introductory courses at Allegheny College commonly use the Java
programming language and compile and run programs using
[Gradle](https://gradle.org/), the following commands shows how to use
GatorGrader to ensure that running the program yields exactly four lines of
output.

```
python3 gatorgrader/gatorgrader.py \
        --commands "gradle run" \
        --outputlines 4 \
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
Python 3.5.2. However, GatorGrader should run correctly on a wide variety of
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

- `--sentences`

Indicates to look for a number of sentences in a md file. Should be followed by
the number of sentences to look for.

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
