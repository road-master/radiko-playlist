"""Implements get process fot master playlist."""

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING
from typing import Mapping
from typing import cast

import m3u8

from radikoplaylist.authorization import Authorization
from radikoplaylist.master_playlist import MasterPlaylist
from radikoplaylist.requester import Requester

if TYPE_CHECKING:
    from radikoplaylist.master_playlist_request import MasterPlaylistRequest

__all__ = ["MasterPlaylistClient"]


class MasterPlaylistClient:
    """Implements get process fot master playlist."""

    @classmethod
    def get(
        cls,
        master_playlist_request: MasterPlaylistRequest,
        *,
        area_id: str = Authorization.ARIA_ID_DEFAULT,
        radiko_session: str | None = None,
    ) -> MasterPlaylist:
        """Gets master playlist.

        Args:
            master_playlist_request: Request object (Live, TimeFree, or TimeFree30Day)
            area_id: Area ID for radiko (default: JP13 for Tokyo)
            radiko_session: Optional radiko premium session cookie for 30-day timefree access.
                Required for TimeFree30DayMasterPlaylistRequest to access premium content.
        """
        headers = Authorization(area_id=area_id, radiko_session=radiko_session).auth()
        url_master_playlist = cls._get_url(master_playlist_request, headers)
        return MasterPlaylist(url_master_playlist, headers)

    @classmethod
    def _get_url(cls, master_playlist_request: MasterPlaylistRequest, headers: Mapping[str, str | bytes]) -> str:
        """Gets URL of master playlist."""
        logger = getLogger(__name__)
        response = Requester.get(master_playlist_request.build_url(headers), headers)
        master_playlist_url = m3u8.loads(response.content.decode("utf-8")).playlists[0].uri
        logger.debug("master_playlist_url: %s", master_playlist_url)
        return cast("str", master_playlist_url)
