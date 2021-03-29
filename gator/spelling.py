"""Perform the spell checking processes to determine that technical writing in a report is correctly spelled."""

from symspellpy import SymSpell, Verbosity
import pkg_resources, re, markdown
from gator import fragments, files


# TODO: Finish the spellchecking function that includes file reading, spell checking, and returning the result of the checks.
def check(input_file, file_directory, ignore):
    """Function to run the symspellpy tool on the contents of the input file."""
    # Define variables that are used to find if the words in a markdown document are correctly spelled.
    markdown_file_contents = []
    spell_check_suggestions = []
    spell_check_outcome = True
    incorrect_spell_check_count = 0

    # Input the markdown file + separate words by spaces and save the contents into a list.
    for file_for_checking in files.create_paths(file=input_file, home=file_directory):
        markdown_file_contents = file_for_checking.read_text().splitlines()

    # Initialize the files and libraries to perform the spellchecking.
    spellcheck = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = pkg_resources.resource_filename(
        "symspellpy", "frequency_dictionary_en_82_765.txt"
    )

    # term_index is the column of the term and count_index is the column of the term frequency
    spellcheck.load_dictionary(dictionary_path, term_index=0, count_index=1)


    # NOTE: Things to consider in the future implementation.
    # 1. How to make sure that you don't spell check inside of code blocks, segments, and links.
    # 2. DONE: How to detect garbage words. (Test the tool to see how good it is.) (Tested and works pretty well.)

    # For a detected incorrect word make the check fail and increment the incorrect_spell_check_count by 1.
    for line in range(len(markdown_file_contents)):        
        # Remove multiple spaces + symbols + setup suggestion for line.
        markdown_file_contents[line] = re.sub(r"[,!@\'~?*_~\.$%_:;]#", "", markdown_file_contents[line], flags=re.I)
        markdown_file_contents[line] = re.sub(r"\s+", " ", markdown_file_contents[line], flags=re.I)
        
        filter_out_characters = False
        end_block_to_filter_out = ""
        
     
        # If a code block is detected iterate through each proceding line until you reach the end of the code block.
        if '```' in markdown_file_contents[line]:
            end_block_to_filter_out = "```"
            filter_out_characters = True
        if '`' in markdown_file_contents[line] and not filter_out_characters:
            end_block_to_filter_out = "`"
            filter_out_characters = True
        if '(' and ')' and '[' and ']' in markdown_file_contents and not filter_out_characters:
            end_block_to_filter_out = ')'
            filter_out_characters = True

        # If special case characters are detected remove all contents contained in code segment and code blocks.
        if filter_out_characters:
            for i, _ in enumerate(range(0, len(markdown_file_contents[line]) + 1)):
                print("made it!", markdown_file_contents[line][0:i])
                if end_block_to_filter_out in markdown_file_contents[line][0:i]:
                    if i <= len(markdown_file_contents[line]):
                        markdown_file_contents[line] = markdown_file_contents[line][i + 1:len(markdown_file_contents[line])]
                        filter_out_characters = False
                        break
                    elif i > len(markdown_file_contents[line]):
                        markdown_file_contents[line] = ""
                        filter_out_characters = False
                        break
                else:
                    continue

    
        print("Perform Spell Checking: ", markdown_file_contents[line])
        # Perform spell checking if the current line is not empty.
        if markdown_file_contents[line] != "":
            # Generate spell check suggestions.
            suggestions = spellcheck.lookup(markdown_file_contents[line], Verbosity.CLOSEST, transfer_casing=True)
            #print("Line: ", markdown_file_contents[line])
            # For each suggestion for the current line if the first suggestion doesn't match the current word record one incorrect word.
            for suggested_correction in suggestions:
                suggested_correction_list = str(suggested_correction).split(",")
                # When a word is spelled incorrectly increase the incorrect spell count by one.
                #print("CORRECTION: ", suggested_correction_list[0])
                if markdown_file_contents[line] != suggested_correction_list[0]:
                    print("CORRECTION: ", suggested_correction_list[0])
                    incorrect_spell_check_count += 1
                    spell_check_outcome = False
                    break


    # If the incorrecT_spellcheck count minus the ignore is 0 or greater perform the subtraction.
    # Else just return 0.
    if incorrect_spell_check_count - abs(ignore) > 0:
        incorrect_spell_check_count -= ignore
    else:
        incorrect_spell_check_count = 0
    
    # Send back the number of incorrectly spelled words and the correctly spelled file state.
    return incorrect_spell_check_count, spell_check_outcome