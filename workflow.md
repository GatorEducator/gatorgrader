# How to Get Started Using GatorGrader

## Table of Contents
* [Introduction](#Introduction)
* [Setting Up A gatorgrader.yml File](#Setting-Up-A-gatorgraderyml-File)
* [Setting Up a GitHub Repository](#Setting-Up-A-GitHub-Repository)
* [Additional Programs to Install](#Additional-Programs-to-Install)
* [How to Run GatorGrader](#How-to-Run-GatorGrader)
* [Things to Include](#Things-to-Include)

## Introduction

## Setting Up A gatorgrader.yml File

In order to set up a **gatorgrader.yml** file, you first need to set up a directory in the repository the assignment you want to use GatorGrader with. The purpose of the **gatorgrader.yml** file is to provide GatorGrader with a series of "checks" to run, specific to the assignment/file it is supposed to be run with. In the following sections, the process for setting up a **gatorgrader.yml** file will be detailed and will include picture examples of existing gatorgrader.yml files.

1. After setting up a directory called "config", open your code editor/text editor/IDE and create and open a file named "gatorgrader.yml".

2. Start off by typing this into the file named "gatorgrader.yml":


    ```
    ---
    name:
    break: true
    indent: 4
    ---
    ```

- In the section "name", is where you put the naming convention of the assignment/file that you are trying to run through GatorGrader.

3. Then, create two empty lines after typing the above section. After creating this space, you can begin on specifying the specific checks needed to be run for your file.

4. First, if you have multiple files that will require checks, it is important to separate the checks for each by the file that they are for. For example, if in your repository you had a folder than contains three different files in it, you would have to specify each file and the checks for each. Here is an example of how you would set up different checks for different files.

    ```
    papers/draft1_paper1.md:
    ConfirmFileExists
    CountFileWords --count 1000 --exact
    CountMarkdownTags --tag "heading" --count 4 --exact
    CountMarkdownTags --tag "Works Cited" --count 1 --exact
    MatchFileFragment --fragment "Add Your Name Here" -- count 0 --exact
    MatchFileFragment --fragment "TODO" --count 0 --exact
    ```

* In this example, the checks are listed after the location of the file you would like to run them with. The file we are checking here is called "draft1_paper1.md", which is located within the folder called "papers". Then each of the lines following that convention are checks to be run for the file in order for it to meet the minimum passing requirements (set by you, of course).

* Some common checks are:

    - `ConfirmFileExists`: This checks that the file exists in the repository, given the specific file destination that is given in the gatorgrader.yml file.

   - `MatchFileFragment`: This checks that the certain fragments, specified by you, are in the file.

    - `CountFileWords`: This counts the amount of words in a file up to a certain amount that is specified by you in the .yml file.

    - `ExecuteCommand`: This checks that a command executes correctly (a --command tag must be used in conjunction with this check).

    - `CountMarkdownTags`: This counts the amount of markdown tags in a file up to a certain amount that is specified by you in the .yml file.

    - `CountCommits`: This counts the amount of commits committed to a GitHub repository.

* Some common tags are:

    - `--fragment`: used to add specific fragments, needs "" marks surrounding the specific fragment to be used, and is used with the `MatchFileFragment` check.

    - `--count`: used to specify specific number counts and is used with checks like `CountFileWords` and `CountMarkdownTags`.

    - `--exact`: used to specify that you want an exact value to be checked, can be used with any of the "count" checks or with the `MatchFileFragment` check.

    - `--language`: used to specify a specific coding language, like Java or Python, in order to do things like run commands using the `ExecuteCommand` check.

    - `--tag`: used to specify a certain tag to be used or looked for in a file, used most commonly with checks like `CheckMarkdownTags`.

    - `--command`: used to specify a specific command, like those used in the Command Line/Terminal, and is usually used in conjunction with the `ExecuteCommand` check.

* A full list of checks that GatorGrader supports can be referenced using this [link](https://www.gatorgrader.org/ember).

5. After adding all the checks you would like to use, for every file included in the assignment you are trying to evaluate, you will have completed your gatorgrader.yml file.

  * Here is an example of a fully-functional gatorgrader.yml file. (The yml file was taken from a practical assignment for Professor Janyl Jumadinova's CMPSC203 Software Engineering Course)

      ```
      ---
      name: cmpsc-203-spring-2021-practical2
      break: true
      indent: 4
      ---

      # note that without an "--exact" the check is an "at least"
      termfrequency:
          compute_tf_cookbook.py:
            ConfirmFileExists
            CountMultipleLineComments --language Python --count 7
            CountSingleLineComments --language Python --count 14
            MatchFileFragment --fragment "import string" --count 1 --exact
            MatchFileFragment --fragment "TODO" --count 0 --exact
            MatchFileFragment --fragment "with open" --count 1
            MatchFileFragment --fragment "global data" --count 3
            MatchFileFragment --fragment "global words" --count 3
            MatchFileFragment --fragment "as data_file" --count 1
            MatchFileFragment --fragment "word_freqs" --count 9
            MatchFileFragment --fragment "data = []" --count 1
            MatchFileFragment --fragment "words = []" --count 1
            MatchFileFragment --fragment "word_freqs = []" --count 1

      tests:
          test_compute_tf_cookbook.py:
            ConfirmFileExists
            CountMultipleLineComments --language Python --count 3
            CountSingleLineComments --language    Python --count 0
            MatchFileFragment --fragment "test_" --count 3
            MatchFileFragment --fragment "assert" --count 3
            MatchFileFragment --fragment "TODO" --count 0 --exact

      # --> check the technical writing
      writing/reflection.md:
        ConfirmFileExists
        CountFileWords --count 400
        CountMarkdownTags --tag "heading" --count 9 --exact
        CountMarkdownTags --tag "code_block" --count 1 --exact
        CountMarkdownTags --tag "list" --count 2 --exact
        MatchFileFragment --fragment "Add Your Name Here" --count 0 --exact
        MatchFileFragment --fragment "TODO" --count 0 --exact

      # --> check the number of commits beyond a threshold
      CountCommits --count 5
      ```


## Things to Include in the Repository
- gradle stuff
- any stuff for specific dependencies needed to run certain programs etc.
- git pull repo
- setting up github assignment (is that the only way to use gg?)
- setting up git, gradle, pipenv, docker? (are these necessary for administrators/instructors trying to use gg for assignments)
