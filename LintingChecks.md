### Linting Checks

✔ GatorGrader: Automatically Check the Files of Programmers and Writers
https://github.com/GatorEducator/gatorgrader

✔ Find the available checks that match an optional pattern

usage: ConfirmFileExists [-h] --file FILE --directory DIR
Check Provided by GatorGrader: ConfirmFileExists
optional arguments:
  -h, --help       show this help message and exit
required checker arguments:
  --file FILE      file for checking (default: None)
  --directory DIR  directory with file for checking (default: None)

usage: CountCommandOutput [-h] --command COMMAND --count COUNT [--exact]
Check Provided by GatorGrader: CountCommandOutput
optional arguments:
  -h, --help         show this help message and exit
required checker arguments:
  --command COMMAND  command to execute (default: None)
  --count COUNT      how many of lines of output should exist (default: None)
optional check arguments:
  --exact            equals instead of a minimum number (default: False)

usage: CountCommits [-h] --count COUNT [--exact]
Check Provided by GatorGrader: CountCommits
optional arguments:
  -h, --help     show this help message and exit
required check arguments:
  --count COUNT  minimum number of git commits (default: None)
optional check arguments:
  --exact        equals instead of a minimum number (default: False)

usage: CountFileLines [-h] --file FILE --directory DIR --count COUNT [--exact]
Check Provided by GatorGrader: CountFileLines
optional arguments:
  -h, --help       show this help message and exit
required checker arguments:
  --file FILE      file for checking (default: None)
  --directory DIR  directory with file for checking (default: None)
  --count COUNT    how many lines should exist (default: None)
optional check arguments:
  --exact          equals instead of a minimum number (default: False)

usage: CountFileParagraphs [-h] --file FILE --directory DIR --count COUNT
                           [--exact]
Check Provided by GatorGrader: CountFileParagraphs
optional arguments:
  -h, --help       show this help message and exit
required checker arguments:
  --file FILE      file for checking (default: None)
  --directory DIR  directory with file for checking (default: None)
  --count COUNT    how many paragraphs should exist (default: None)
optional check arguments:
  --exact          equals instead of a minimum number (default: False)

usage: CountFileWords [-h] --file FILE --directory DIR --count COUNT [--exact]
Check Provided by GatorGrader: CountFileWords
optional arguments:
  -h, --help       show this help message and exit
required checker arguments:
  --file FILE      file for checking (default: None)
  --directory DIR  directory with file for checking (default: None)
  --count COUNT    how many total words should exist in the file (default:
                   None)
optional check arguments:
  --exact          equals instead of a minimum number (default: False)

usage: CountMarkdownTags [-h] --tag TAG --file FILE --directory DIR --count
                         COUNT [--exact]
Check Provided by GatorGrader: CountMarkdownTags
optional arguments:
  -h, --help       show this help message and exit
required checker arguments:
  --tag TAG        markdown tag that exists in a file
  --file FILE      file for checking
  --directory DIR  directory with file for checking
  --count COUNT    how many tag instances should exist
optional check arguments:
  --exact          equals instead of a minimum number
examples of available tags: code, code_block, heading, image, link, list, paragraph
markdown tag reference: https://spec.commonmark.org/0.29/

usage: CountMultipleLineComments [-h] --file FILE --directory DIR --count
                                 COUNT [--language LANG] [--exact]
Check Provided by GatorGrader: CountMultipleLineComments
optional arguments:
  -h, --help       show this help message and exit
required checker arguments:
  --file FILE      file for checking (default: None)
  --directory DIR  directory with file for checking (default: None)
  --count COUNT    how many multiple-line comments should exist (default:
                   None)
  --language LANG  language for the multiple-line comments (default: None)
optional check arguments:
  --exact          equals instead of a minimum number (default: False)

usage: CountParagraphWords [-h] --file FILE --directory DIR --count COUNT
                           [--exact]
Check Provided by GatorGrader: CountParagraphWords
optional arguments:
  -h, --help       show this help message and exit
required checker arguments:
  --file FILE      file for checking (default: None)
  --directory DIR  directory with file for checking (default: None)
  --count COUNT    how many words should exist in every paragraph (default:
                   None)
optional check arguments:
  --exact          equals instead of a minimum number (default: False)

usage: CountSingleLineComments [-h] --file FILE --directory DIR --count COUNT
                               [--language {Java,Python}] [--exact]
Check Provided by GatorGrader: CountSingleLineComments
optional arguments:
  -h, --help            show this help message and exit
required checker arguments:
  --file FILE           file for checking (default: None)
  --directory DIR       directory with file for checking (default: None)
  --count COUNT         how many single-line comments should exist (default:
                        None)
  --language {Java,Python}
                        language for the single-line comments (default: None)
optional check arguments:
  --exact               equals instead of a minimum number (default: False)

usage: ExecuteCommand [-h] --command COMMAND
Check Provided by GatorGrader: ExecuteCommand
optional arguments:
  -h, --help         show this help message and exit
required checker arguments:
  --command COMMAND  command to execute (default: None)

usage: ListChecks [-h] [--namecontains LABEL]
Check Provided by GatorGrader: ListChecks
optional arguments:
  -h, --help            show this help message and exit
optional check arguments:
  --namecontains LABEL  filter by label that name must contain (default: None)

usage: MatchCommandFragment [-h] --command CMD --fragment FRAG --count COUNT
                            [--exact]
Check Provided by GatorGrader: MatchCommandFragment
optional arguments:
  -h, --help       show this help message and exit
required checker arguments:
  --command CMD    command to execute (default: None)
  --fragment FRAG  fragment that exists in command output (default: None)
  --count COUNT    how many of fragment should exist (default: None)
optional check arguments:
  --exact          equals instead of a minimum number (default: False)

usage: MatchCommandRegex [-h] --command CMD --regex REGEX --count COUNT
                         [--exact]
Check Provided by GatorGrader: MatchCommandRegex
optional arguments:
  -h, --help     show this help message and exit
required checker arguments:
  --command CMD  command to execute (default: None)
  --regex REGEX  regular expression that matches command output (default:
                 None)
  --count COUNT  how many regex matches should exist (default: None)
optional check arguments:
  --exact        equals instead of a minimum number (default: False)

usage: MatchFileFragment [-h] --file FILE --directory DIR --fragment FRAG
                         --count COUNT [--exact]
Check Provided by GatorGrader: MatchFileFragment
optional arguments:
  -h, --help       show this help message and exit
required checker arguments:
  --file FILE      file for checking (default: None)
  --directory DIR  directory with file for checking (default: None)
  --fragment FRAG  fragment that exists in the file (default: None)
  --count COUNT    how many of a fragment should exist (default: None)
optional check arguments:
  --exact          equals instead of a minimum number (default: False)

usage: MatchFileRegex [-h] --file FILE --directory DIR --regex REGEX --count
                      COUNT [--exact]
Check Provided by GatorGrader: MatchFileRegex
optional arguments:
  -h, --help       show this help message and exit
required checker arguments:
  --file FILE      file for checking (default: None)
  --directory DIR  directory with file for checking (default: None)
  --regex REGEX    regular expression that matches file contents (default:
                   None)
  --count COUNT    how many regex matches should exist (default: None)
optional check arguments:
  --exact          equals instead of a minimum number (default: False)
