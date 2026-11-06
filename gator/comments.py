"""Check that a file in a directory contains a specified number of singleline or multiline comments."""

import tree_sitter_c as tsC
import tree_sitter_cpp as tsCPP
import tree_sitter_java as tsJava
import tree_sitter_javascript as tsJavaScript
import tree_sitter_python as tsPython
from tree_sitter import Language, Parser

from gator import constants


def language_to_parse(lang):
    """Match language to feed to parser."""
    match lang:
        case "Python":
            return Language(tsPython.language())
        case "Java":
            return Language(tsJava.language())
        case "CPP":
            return Language(tsCPP.language())
        case "C":
            return Language(tsC.language())
        case _:
            return Language(tsJavaScript.language())


def count_comments_java(multi, types):
    """Count multiline or singleline java comments."""
    if multi:
        return types.count("block_comment")
    else:
        return types.count("line_comment")


def count_comments_python(multi, types, node_list, c):
    """Count python comments, handling how multiline comments are parsed."""
    if not multi:
        return types.count("comment")
    else:
        comment_count = 0
        for node in node_list:
            if node.type == "string":
                if c[node.start_byte : node.end_byte].startswith('"""'):
                    comment_count += 1
        return comment_count


def count_comments_other(multi, comments):
    """Count multiline or singleline comments from parsed comments."""
    comment_count = 0
    if multi:
        for com in comments:
            if com.startswith("/*"):
                comment_count += 1
    else:
        for com in comments:
            if com.startswith("//"):
                comment_count += 1
    return comment_count


def parse_tree_sitter(code, language, multiline=False):
    """Use chosen language to parse source code, counting comments by specification."""

    def get_node_types(node, node_types):
        comments = []
        nodes.append(node)
        node_types.append(node.type)
        if node.type == "comment":
            comments.append(code[node.start_byte : node.end_byte])
        for child in node.children:
            comments.extend(get_node_types(child, node_types))
        return comments

    PARSE_LANGUAGE = language_to_parse(language)
    parser = Parser(PARSE_LANGUAGE)
    tree = parser.parse(code.encode("utf-8"))

    nodes = []
    node_types = []
    coms = get_node_types(tree.root_node, node_types)

    if language == "Java":
        return count_comments_java(multiline, node_types)
    elif language == "Python":
        return count_comments_python(multiline, node_types, nodes, code)
    else:
        return count_comments_other(multiline, coms)


def count_singleline_java_comment(contents):
    """Count the number of singleline Java comments in the code."""
    matches_count = parse_tree_sitter(contents, "Java", False)
    return matches_count, {constants.markers.First: matches_count}


def count_singleline_cpp_comment(contents):
    """Count the number of singleline CPP comments in the code."""
    matches_count = parse_tree_sitter(contents, "CPP", False)
    return matches_count, {constants.markers.First: matches_count}


def count_singleline_c_comment(contents):
    """Count the number of singleline C comments in the code."""
    matches_count = parse_tree_sitter(contents, "C", False)
    return matches_count, {constants.markers.First: matches_count}


def count_singleline_javascript_comment(contents):
    """Count the number of singleline JavaScript comments in the code."""
    matches_count = parse_tree_sitter(contents, "JavaScript", False)
    return matches_count, {constants.markers.First: matches_count}


def count_singleline_python_comment(contents):
    """Count the number of singleline Python comments in the code."""
    matches_count = parse_tree_sitter(contents, "Python", False)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_java_comment(contents):
    """Count the number of multiline Java comments in the code."""
    matches_count = parse_tree_sitter(contents, "Java", True)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_cpp_comment(contents):
    """Count the number of multiline CPP comments in the code."""
    matches_count = parse_tree_sitter(contents, "CPP", True)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_c_comment(contents):
    """Count the number of multiline C comments in the code."""
    matches_count = parse_tree_sitter(contents, "C", True)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_javascript_comment(contents):
    """Count the number of multiline JavaScript comments in the code."""
    matches_count = parse_tree_sitter(contents, "JavaScript", True)
    return matches_count, {constants.markers.First: matches_count}


def count_multiline_python_comment(contents):
    """Count the number of multiline Python comments in the code."""
    matches_count = parse_tree_sitter(contents, "Python", True)
    return matches_count, {constants.markers.First: matches_count}
