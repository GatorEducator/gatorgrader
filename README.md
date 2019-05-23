# Gator Grader

![Image of Logo](https://raw.githubusercontent.com/GatorEducator/gatorgrader/master/.github/gatorgraderlogo.png)

<center>
The only tool you'll need to ensure your code is up to speed!
Whenever you feel in doubt, know GatorGrader is there to help.
</center>

[![Build Status](https://api.travis-ci.org/GatorEducator/gatorgrader.svg?branch=master)](https://travis-ci.org/GatorEducator/gatorgrader) [![codecov.io](http://codecov.io/github/GatorEducator/gatorgrader/coverage.svg?branch=master)](http://codecov.io/github/GatorEducator/gatorgrader?branch=master) [![codacy.com](https://api.codacy.com/project/badge/Grade/3dade81be6dc467b8e34cde66eb5cdc6)](https://www.codacy.com/app/GatorEducator/gatorgrader?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=GatorEducator/gatorgrader&amp;utm_campaign=Badge_Grade) [![All Contributors](https://img.shields.io/badge/all_contributors-32-orange.svg?style=flat)](#contributors) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-orange.svg)](https://www.python.org/)

## How to Use
For those who are interested in using GatorGrader, this program allows for an
easy implementation into the lab that needs graded. Provided below are starter
labs that will help you to follow along with the implementation of GatorGrader!
The links are starter labs for [Java](https://github.com/GatorEducator/java-starter),
[LaTeX](https://github.com/GatorEducator/latex-assignment-starter), &
[HTML with CSS](https://github.com/GatorEducator/html-css-assignment-starter).
They do not require you to complete these steps and instead it will download
and install GatorGrader and run all of the preconfigured checks when you type
`gradle grade` in your terminal window.

## Key Features

For instance:

* Can automatically check and assess the work of writers and programmers.

* Can be used in conjunction with [GatorGradle](https://github.com/GatorEducator/gatorgradle)
  to check Gradle projects

* Can be used to check "solution" and "starter" GitHub Classroom repositories

* Can use GatorGrader in a cloud base environment (e.g. Travis CI) or through
  command-line.

* Effectively integrates into many diverse workflows and development environments.

* Can be used with any text-based programming language or document.

* Can check for sentence fragments and text and regular expression fragments.

* Can check to see if required files exist and are in the correct directory, and
  that the directory exists.

* Can check for a specified number of single line or multi-line comments in source code.

* Can check the number of words and paragraphs in Markdown files.

* Can check for a required minimum number of Git commits.

Designed for use with [GitHub](https://github.com/), [GitHub
Classroom](https://classroom.github.com/), [Travis CI](https://travis-ci.com/),
and [Gradle](https://gradle.org/), GatorGrader is an automated assessment tool
that checks the work of programmers and writers. While other tools already exist
to, for instance, enforce a style guide for source code or build a program,
GatorGrader focuses on automating the checks and activities that are not already
nicely supported. In alignment with key recommendations in a recent [National Academies
report](https://www.nap.edu/catalog/24926/assessing-and-responding-to-the-growth-of-computer-science-undergraduate-enrollments),
instructors have used GatorGrader to automatically check student submissions in
both introductory and application-oriented classes using languages like
Markdown, Java, Python, JavaScript, CSS, and HTML. GatorGrader's simple, yet
useful, automated checks can also be integrated into the continuous integration
build process supported by a system like [Travis CI](https://travis-ci.com/).
In contrast to other automated grading tools, GatorGrader does not aim to solve
problems related to building a project or managing an assignment's submission,
instead relying on existing tools that can effectively handle those tasks.

## What Do People Think about GatorGrader?

GatorGrader addresses some of the challenges that an instructor faces when
designing automated checks for the source code or technical writing that a
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

Installing GatorGrader is not necessary if the intended use case includes
[GatorGradle](https://github.com/GatorEducator/gatorgradle). If a separate
installation is needed, however, you should first install
[Pipenv](https://github.com/pypa/pipenv) by following Pipenv's installation
instructions. Please also be sure that you have installed Git on your computer
and that you can run Git commands in a terminal window. Then, you can type the
following command in your terminal window to clone GatorGrader's GitHub
repository:

```bash
git clone https://github.com/GatorEducator/gatorgrader.git
```

If you plan to develop new features for GatorGrader or if you want to run the
tool's test suite in [Pytest](https://github.com/pytest-dev/pytest), then you
will need to install the developer dependencies by typing `pipenv install --dev`
in the directory that contains GatorGrader. If you only want to use GatorGrader,
then you can type `pipenv install` instead. Once these commands are completed
successfully, you have officially installed GatorGrader!

## Testing GatorGrader

GatorGrader uses [Pytest](https://docs.pytest.org/en/latest/) for testing.
Depending on your goals, there are several different configurations in which you
can run the provided test suite. If you want to run the test suite to see if
all of the test cases are correctly passing, then you can type the first (located
below) in your terminal window. Along with running the test suite, the developers
of GatorGrader used statement coverage to inform their testing of the tool. To
see the current coverage of the tests while also highlighting the lines that are
not currently covered by the tests, type the second command below in your terminal
window.

```bash
pipenv run test
```

or

```bash
pipenv run cover
```

## Running GatorGrader

GatorGrader can automatically perform simple checks on both writing and source
code. You can learn about GatorGrader's checks and defaults by typing `pipenv
run python3 gatorgrader.py --help` in your terminal window and/or following the
provided link. GatorGrader employs many checks to ensure that you configure it
with the correct command-line arguments.

## GatorGrader in Action

GatorGrader is commonly used in conjunction with other tools that check source
code and technical writing. For instance, in the introductory Computer Science
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
GitHub repositories that provide starting code templates.

## Comparison to Existing Tools

In today's world, there are so many new up and coming systems in the study of
Computer Science. The most noticeable change is the amount of automated
grading systems that are being created by schools and companies. Three that can
be referenced when talking about GatorGrader are:

1. [CS50 Harvard](https://github.com/cs50/check50)
2. [Submitty](https://github.com/Submitty/Submitty)
3. [Web Cat](https://github.com/web-cat/web-cat-plugin-JavaTddPlugin)

When it comes to CS50 Harvard, the first step to a great program is
documentation, however, that is what they are lacking but it is something that
we can assure you is a priority on our side. It does not seem like CS50 is
known for its integration within multiple classes or languages. It only makes
direct references to the use in a CS50 class at Harvard and nothing about what
languages that encompasses. However, when it comes to our tool GatorGrader,
it can be used on classes that have languages such as Java, HTML, or even
LaTex.

For Submitty, there tool rather similar to ours. However, the one difference is
that they are modeling more of a GitHub type of tool. In other words, they are
modeling a system that will hold assignments and leave them there for grading.
Besides questions that may already have programmed answers, other checks like
those that accompany a test case being written, seem like they must be hand
graded. Therefore, it eliminates the idea of an automated grading system.
In contrast, GatorGrader does all the grading for you. You input checks into
a `yml` file and when students submit their work, the checks are checked to see
if they have been fulfilled. Therefore, eliminating the need for the professor
to hand grade an assignment.

Web Cat is a private grading system that one needs an account or access too.
Therefore, it is impossible to be open for other users that do not have
or specifically want Web Cat.

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
Our development team uses the [GitHub Flow
Model](https://guides.github.com/introduction/flow/) to guide our engineering of
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
