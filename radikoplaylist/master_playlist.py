"""Model of master playlist."""

from typing import Mapping, Union


# pylint: disable=too-few-public-methods
class MasterPlaylist:
    def __init__(self, media_playlist_url: str, headers: Mapping[str, Union[str, bytes]]) -> None:
        self.media_playlist_url = media_playlist_url
        self.headers = headers
