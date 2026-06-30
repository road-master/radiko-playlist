"""This module implements exceptions for this package."""

# This command prevents docformatter from removing blank lines in docstring against PEP8 (conflicts with Ruff (Black))
# - The docformatter removes blank line against PEP8 (conflicts with Ruff (Black)) · Issue #350 · PyCQA/docformatter
#   https://github.com/PyCQA/docformatter/issues/350


class Error(Exception):
    """Base class for exceptions in this module.

    @see https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions
    """


class HttpRequestError(Error):
    """HTTP request failed."""


class HttpRequestTimeoutError(HttpRequestError):
    """HTTP request timed out."""


class BadHttpStatusCodeError(HttpRequestError):
    """HTTP status code is not 200."""


class NoAvailableUrlError(Error):
    """No available URL."""


# Reason: This is not error like StopIteration
class FoundFastestHostToDownload(Error):  # noqa: N818
    """Found fastest host to download."""
