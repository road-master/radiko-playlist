"""Implements request model to build URL to request master playlist."""

from abc import ABC, abstractmethod
import datetime
import hashlib
from logging import getLogger
from random import SystemRandom
from typing import Mapping, Union

from radikoplaylist.playlist_create_url_getter import LivePlaylistCreateUrlGetter, TimeFreePlaylistCreateUrlGetter

__all__ = ["LiveMasterPlaylistRequest", "MasterPlaylistRequest", "TimeFreeMasterPlaylistRequest"]


class MasterPlaylistRequest(ABC):
    """Request for MasterPlaylist."""

    # Reason: Temporary ignore since this is referenced by user's code.
    def __init__(self, station_id: str, is_time_free: bool) -> None:  # noqa: FBT001
        self.station_id = station_id
        self.is_time_free = is_time_free
        self.logger = getLogger(__name__)

    def build_url(self, headers: Mapping[str, Union[str, bytes]]) -> str:
        """Creates URL of master playlist."""
        url = self.get_playlist_create_url(headers) + "?" + self.build_query()
        self.logger.debug("playlist url:%s", url)
        return url

    @abstractmethod
    def get_playlist_create_url(self, headers: Mapping[str, Union[str, bytes]]) -> str:
        raise NotImplementedError

    @abstractmethod
    def build_query(self) -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def generate_uid() -> str:
        """@see https://turtlechan.hatenablog.com/entry/2019/06/25/195451"""


class LiveMasterPlaylistRequest(MasterPlaylistRequest):
    """MasterPlayListRequest for live."""

    def __init__(self, station_id: str) -> None:
        super().__init__(station_id, is_time_free=False)

    def get_playlist_create_url(self, headers: Mapping[str, Union[str, bytes]]) -> str:
        return LivePlaylistCreateUrlGetter.get(self.station_id, headers)

    def build_query(self) -> str:
        return "station_id=" + self.station_id + "&l=15&lsid=" + self.generate_uid() + "&type=b"

    @staticmethod
    def generate_uid() -> str:
        return "11111111111111111111111111111111111111"


class TimeFreeMasterPlaylistRequest(MasterPlaylistRequest):
    """MasterPlayListRequest for time free."""

    JST = datetime.timezone(datetime.timedelta(hours=9), "JST")

    def __init__(self, station_id: str, start_at: int, end_at: int) -> None:
        super().__init__(station_id, is_time_free=True)
        self.start_at = start_at
        self.end_at = end_at

    def get_playlist_create_url(self, headers: Mapping[str, Union[str, bytes]]) -> str:
        return TimeFreePlaylistCreateUrlGetter.get(self.station_id, headers)

    def build_query(self) -> str:
        return (
            "station_id=" + self.station_id + "&"
            "start_at=" + str(self.start_at) + "&"
            "ft=" + str(self.start_at) + "&"
            "end_at=" + str(self.end_at) + "&"
            "to=" + str(self.end_at) + "&"
            "l=15&"
            "lsid=" + self.generate_uid() + "&"
            "type=b"
        )

    @staticmethod
    def generate_uid() -> str:
        rnd = SystemRandom().random() * 1000000000
        now = datetime.datetime.now(tz=TimeFreeMasterPlaylistRequest.JST)
        start = datetime.datetime(1970, 1, 1, tzinfo=TimeFreeMasterPlaylistRequest.JST)
        micro_second = datetime.timedelta.total_seconds(now - start) * 1000
        # Reason: 2023-02-06 Javascript in radiko.jp still use MD5_hexhash().
        #   DUO130: Flake8 is using this.
        return hashlib.md5(str(rnd + micro_second).encode("utf-8")).hexdigest()  # noqa: S324 DUO130 RUF100  # nosec
