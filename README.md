# GatorGrader

Designed for use with [GitHub Classroom](https://classroom.github.com/),
GatorGrader is an automated grading tool that checks the work of programmers and
writers. Although it can be used independently of a project, GatorGrader is
commonly used by faculty in the [Department of Computer Science at Allegheny
College](https://github.com/Allegheny-Computer-Science) as a Git submodule in a
Git repository for a specific assignment. Since it is a Python 3 program that
can easily be run on the command-line, GatorGrader also works nicely with
[Travis CI](https://travis-ci.com/) &mdash; which is again how faculty members
at Allegheny College commonly use it in conjunction with other automated
checking tools.

## Installation

As a Python 3 program, GatorGrader relies on
[pip](https://pip.pypa.io/en/stable/installing/) for installation. To ensure
that all of the dependencies are installed correctly, please type
the following commands to install GatorGrader.

- `pip install --upgrade pip`
- `pip install -r requirements.txt`

## Running GatorGrader

If your environment supports it, then please set the `GATORGRADER_HOME`
environment variable. For instance, typing the command `export
GATORGRADER_HOME="/home/travis/build/gkapfham/gatorgrader"` would set
`GATORGRADER_HOME` so that [Gregory M.
Kapfhammer](http://www.cs.allegheny.edu/sites/gkapfham) could run GatorGrader on
Travis CI. You should set this environment variable so that it points to the
directory that contains the file called `gatorgrader.py`.

## Problems or Praise

If you have any problems with installing or using GatorGrader, then please
create an issue associated with this Git repository using the "Issues" link at
the top of this site. The contributors to the GatorGrader will do all that they
can to resolve your issue and ensure that the entire tool works well in your
teaching and development environment.
