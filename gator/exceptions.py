"""Provide Exception and Error classes for use by GatorGrader."""


class InvalidCheckArgumentsError(Exception):
    """The check arguments are invalid."""

    def __init__(self, arguments, usage, error, check_name=None):
        """Initialize the InvalidCheckArgumentsError."""
        self.arguments = arguments
        self.usage = usage.strip()
        self.error = error.strip()
        if check_name:
            self.check_name = check_name.strip()


class InvalidSystemArgumentsError(Exception):
    """The system arguments are invalid."""

    def __init__(self, arguments):
        """Initialize the InvalidSystemArgumentsError."""
        self.arguments = arguments


class InvalidCheckError(InvalidSystemArgumentsError):
    """The check is invalid."""

    def __init__(self, arguments, check_name):
        """Initialize the InvalidCheckError."""
        super().__init__(arguments)
        self.check_name = check_name.strip()
