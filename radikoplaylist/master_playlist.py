"""Model of master playlist."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping


# pylint: disable=too-few-public-methods
class MasterPlaylist:
    def __init__(self, media_playlist_url: str, headers: Mapping[str, str | bytes]) -> None:
        self.media_playlist_url = media_playlist_url
        self.headers = headers
