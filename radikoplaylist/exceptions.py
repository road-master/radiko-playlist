"""This module implements exceptions for this package."""


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


class FoundFastestHostToDownload(Error):
    """Found fastest host to download."""
