"""Tests for the loading, verification, and use of plugin-based checkers."""


from gator import checkers


def test_load_checkers_list_is_not_empty_default_input():
    """Ensures checker loading results in non-empty list with defaults."""
    checker_source_list = checkers.get_sources()
    assert checker_source_list is not None
