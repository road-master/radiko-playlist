"""Implements get process fot master playlist."""

from logging import getLogger
from typing import cast, Mapping, Union

import m3u8

from radikoplaylist.authorization import Authorization
from radikoplaylist.master_playlist import MasterPlaylist
from radikoplaylist.master_playlist_request import MasterPlaylistRequest
from radikoplaylist.requester import Requester

__all__ = ["MasterPlaylistClient"]


class MasterPlaylistClient:
    """Implements get process fot master playlist."""

    @classmethod
    def get(
        cls,
        master_playlist_request: MasterPlaylistRequest,
        *,
        area_id: str = Authorization.ARIA_ID_DEFAULT,
    ) -> MasterPlaylist:
        """Gets master playlist."""
        headers = Authorization(area_id=area_id).auth()
        url_master_playlist = cls._get_url(master_playlist_request, headers)
        return MasterPlaylist(url_master_playlist, headers)

    @classmethod
    def _get_url(cls, master_playlist_request: MasterPlaylistRequest, headers: Mapping[str, Union[str, bytes]]) -> str:
        """Gets URL of master playlist."""
        logger = getLogger(__name__)
        response = Requester.get(master_playlist_request.build_url(headers), headers)
        master_playlist_url = m3u8.loads(response.content.decode("utf-8")).playlists[0].uri
        logger.debug("master_playlist_url: %s", master_playlist_url)
        return cast("str", master_playlist_url)
