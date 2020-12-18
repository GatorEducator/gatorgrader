"""Perform the spell checking processes to determine that technical writing in a report is correctly spelled."""

from symspellpy import SymSpell, Verbosity
import pkg_resources

def spellcheck(input_object):
    """Function to run the spellchecking tool on the contents of the input file."""
    spell_check_suggestions = []

    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt")
    # term_index is the column of the term and count_index is the
    # column of the term frequency
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
  
    for element in input_object:
        suggestions = sym_spell.lookup(element, Verbosity.CLOSEST)
        # display suggestion term, term frequency, and edit distance
        for suggestion in suggestions:
            spell_check_suggestions.append(suggestion)
    return spell_check_suggestions