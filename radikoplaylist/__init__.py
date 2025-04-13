"""Top-level package for radiko playlist."""

from radikoplaylist.master_playlist_client import *  # noqa: F403
from radikoplaylist.master_playlist_request import *  # noqa: F403

__author__ = """Master"""
__email__ = "roadmasternavi@gmail.com"
__version__ = "1.1.1"

__all__ = []
__all__ += master_playlist_request.__all__  # type:ignore[name-defined] # noqa: F405 pylint: disable=undefined-variable
__all__ += master_playlist_client.__all__  # type:ignore[name-defined] # noqa: F405 pylint: disable=undefined-variable
