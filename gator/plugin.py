"""Documentation of the external checker contract.

External checker modules (loaded from a directory passed via ``--checkerdir``)
implement three module-level functions: ``get_parser``, ``parse`` and ``act``.
This module describes that contract as a :py:class:`~typing.Protocol` so plugin
authors can type-check against it, and provides a small validation helper for
the static checks that GatorGrader itself performs at load time.

The protocol and helper use only the standard library: plugin authors do not
need to import private ``gator`` internals to be checked.
"""

import argparse
import inspect
from typing import Protocol


class CheckerModule(Protocol):
    """Shape of an external checker module loaded via ``--checkerdir``.

    The CLI check name is the module filename with the leading ``check_``
    prefix stripped (e.g. ``check_WordCount.py`` becomes ``WordCount``).
    """

    def get_parser() -> argparse.ArgumentParser:
        """Return the argument parser for this check.

        Set ``prog`` to the check name so that ``--help`` output is correct.
        """

    def parse(args) -> argparse.Namespace:
        """Parse ``args`` using the parser from ``get_parser``.

        Built-in checks delegate to ``gator.checkers.parse(get_parser, args)``;
        the docstring parser here does the same.
        """

    def act(main_parsed_arguments, check_remaining_arguments) -> bool:
        """Run the check and report its outcome.

        Args:
            main_parsed_arguments: GatorGrader's top-level parsed arguments.
            check_remaining_arguments: Remaining arguments for this check.

        Returns:
            True when the check passes, False otherwise.

        """


def verify_check_functions(check, functions=("act", "get_parser", "parse")):
    """Return True when *check* has every function in *functions*.

    Mirrors ``gator.checkers.verify_check_functions`` so plugin authors can
    validate a module before shipping it.
    """
    return all(hasattr(check, function) for function in functions)


def verify_act_returns_bool(check):
    """Return True when *check*'s ``act`` is annotated to return a bool.

    Runtime behaviour is the final arbiter; this catches the common mistake of
    forgetting the annotation, not a genuinely broken ``act`` body.
    """
    act = getattr(check, "act", None)
    if not callable(act):
        return False
    annotation = inspect.signature(act).return_annotation
    return annotation is bool
