"""Perform the spell checking processes to determine that technical writing in a report is correctly spelled."""

from symspellpy import SymSpell, Verbosity
import pkg_resources, re, markdown
from gator import fragments, files


# TODO: Finish the spellchecking function that can filter out contents contained inside of a code block.
def check(input_file, file_directory, ignore):
    """Function to run the symspellpy tool on the contents of the input file."""
    # Define variables that are used to find if the words in a markdown document are correctly spelled.
    file = []
    spell_check_suggestions = []
    filter_types = []
    spell_check_outcome = True
    incorrect_spell_check_count = 0

    # Input the markdown file + separate words by spaces and save the contents into a list.
    for file_for_checking in files.create_paths(file=input_file, home=file_directory):
        file = file_for_checking.read_text().splitlines()

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
    for line in range(len(file)):
        # Remove multiple spaces + symbols + setup suggestion for line.
        file[line] = re.sub(r"[,!@\'~?*_~\.$%#]", "", file[line], flags=re.I)
        file[line] = re.sub(r"\s+", " ", file[line], flags=re.I)
        # file[line] = re.sub(r"```", "++", file[line], flags=re.I)

        block_character_counter = 0
        # Iterate through the line and count the frequency of the "`" symbol to determine whether the file needs to check for code blocks or code segments.
        for index in file[line]:
            if index == "`":
                block_character_counter += 1

        # If a code block is detected iterate through each proceding line until you reach the end of the code block.
        if block_character_counter % 2 == 1:
            filter_types.append("```")
        if block_character_counter % 2 == 0:
            filter_types.append("`")

        temp_line = line
        work = True
        i = 0

        filtering_code_block = False
        if len(filter_types) != 0:
            for i in filter_types:
                # CASE: If we're checking for the code segment markdown formatter.
                if i == "`":
                    filter_active = False
                    # NOTE: If there are multiple code segments iterate through the string and intelligently filter out everything inside of them until you reach the end of the line.
                    if block_character_counter % 2 == 0 and i == "`" and i in file[line]:
                        for counter, character in enumerate(file[line]):
                            if character == i and filter_active == False:
                                filter_active = True
                                open_character = counter
                            elif character == i and filter_active == True:
                                file[line] = file[line][0:open_character-1] + file[line][counter + 1:len(file[line])]
                                filter_active = False
                                break
                                #work = False
                # CASE: If we're checking for the code block markdown formatter and found the opening characters for a code block.
                elif i == "```":
                    if not filtering_code_block:
                        file[line] == ""
                        filtering_code_block = True
                        #work = False

                    # If we're still in the code block set the line to empty.
                    if filtering_code_block:
                        file[line] = ""
                        #work = False

                    # Once we have reached the end of the code block 
                    if i == '```' and filtering_code_block:
                        file[line] == ""
                        filtering_code_block = False
                        #work = False

        # Remove every un-spellcheckable fragment in the list.
        # print("Length: ", len(filter_types))
        # if len(filter_types) != 0:
            # while work:
            #     # If it reaches the end of the file, return the values and stop spellchecking.
            #     if temp_line == len(file):
            #         file[temp_line - 1] = ""
            #         return incorrect_spell_check_count, spell_check_outcome

            #     end_index = len(file[temp_line]) + 1
                
            #     # If the fragment filter type was detected rearrange the string to exclude everything after the second appearance.
            #     if filter_types[i] in file[temp_line] and len(file[temp_line]) != len(
            #         filter_types[i]
            #     ):
            #         if len(filter_types[i]) == 1:
            #             # If the end filter type is not at the end of the line snip everything contained and retain everything after it on the current line.
            #             current_line = file[temp_line]
            #             start_index = current_line.index(str(filter_types[i]))
            #             cut_and_fitted_string = file[temp_line][
            #                 start_index + int(len(filter_types[i])) : end_index
            #             ]
            #             end_point_index = cut_and_fitted_string.index(filter_types[i])
            #             file[temp_line] = file[temp_line][end_point_index + 2:end_index]
            
            #             print("Opening Cut Index: ", cut_and_fitted_string)
            #             print("Fitted String: ", file[temp_line])
            #             print("Complex: ", file[temp_line][end_point_index + 2:end_index])

            #             filter_types[i] = ""

            #             work = False
            #             break

            #         elif len(filter_types[i]) == 3:
            #             file[temp_line] == ""
            #             filter_types[i] = ""
            #             work = False
            #         current_line = file[temp_line]
            #         start_index = current_line.index(str(filter_types[i]))
            #         cut_and_fitted_string = file[temp_line][
            #             start_index + int(len(filter_types[i])) : end_index
            #         ]
            #         end_point_index = cut_and_fitted_string.index(filter_types[i])
            #         # Case: If the end point is less than the length of the characters in the file, cut among specific indexes.
            #         if end_point_index < len(file[temp_line]):
            #             #print("End point less than length of file: ", cut_and_fitted_string)

            #             val = file[temp_line][
            #                 start_index + int(len(filter_types[i])) : end_index
            #             ]

            #             print("Val", val)

            #             file[temp_line] = str(val)

            #             filter_types[i] = ""
            #             temp_line += 1
            #             # work = False
            #         # If the end filter is at the end of the line make the line entry empty.
            #         # Case: If the closing filter is not seen on this line, empty everything on the line after the opening format character.
            #         else:
            #             print("Erase Activated")

            #             file[line] = ""
            #             filter_types[i] = ""
            #             temp_line += 1
            #             # work = False

            #     # Case: If the closing format specifier is the only set of characters on a line, empty the line and stop checking for the closing format specifier.
            #     elif filter_types[i] in file[temp_line] and len(file[temp_line]) == len(
            #         filter_types[i]
            #     ):
            #         file[temp_line] = ""
            #         work = False
            #     # Case: If the end fragment was not found remove everything on the entire line and iterate to the next line.
            #     else:
            #         file[temp_line] = file[temp_line][:]
            #         temp_line += 1
            # i += 1

        print("\tRUN: ", file[line])
        # Perform spell checking if the current line is not empty.
        if file[line] != "":
            # Generate spell check suggestions.
            suggestions = spellcheck.lookup(
                file[line], Verbosity.CLOSEST, transfer_casing=True
            )
            # For each suggestion for the current line if the first suggestion doesn't match the current word record one incorrect word.
            for suggested_correction in suggestions:
                suggested_correction_list = str(suggested_correction).split(",")
                # When a word is spelled incorrectly increase the incorrect spell count by one.
                if file[line] != suggested_correction_list[0]:
                    print("\tCORRECTION: ", suggested_correction_list[0])
                    incorrect_spell_check_count += 1
                    spell_check_outcome = False
                    break

    # If the incorrect_spellcheck count minus the ignore is 0 or greater perform the subtraction.
    # Else just return 0.
    if incorrect_spell_check_count - abs(ignore) > 0:
        incorrect_spell_check_count -= ignore
    else:
        incorrect_spell_check_count = 0

    #print(file)

    # Send back the number of incorrectly spelled words and the correctly spelled file state.
    return incorrect_spell_check_count, spell_check_outcome
