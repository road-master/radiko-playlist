"""Implements getting process URL to create playlist."""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeVar

from defusedxml import ElementTree

from radikoplaylist.exceptions import FoundFastestHostToDownload
from radikoplaylist.exceptions import NoAvailableUrlError
from radikoplaylist.requester import Requester

if TYPE_CHECKING:
    from collections.abc import Mapping

    # - defusedxml lacks an Element class · Issue #48 · tiran/defusedxml
    #   https://github.com/tiran/defusedxml/issues/48#issuecomment-1511284750
    from xml.etree.ElementTree import Element  # nosec B405


# Reason: This class is intentionally designed as a base class for other classes.
class UrlChecker(ABC):  # noqa: B024
    """To check URL whether FFmpeg supported or not."""

    C_RPAA = "https://c-rpaa.smartstream.ne.jp"
    SI_C_RADIKO = "https://si-c-radiko.smartstream.ne.jp"
    SI_F_RADIKO = "https://si-f-radiko.smartstream.ne.jp"
    RD_WOWZA_RADIKO = "https://rd-wowza-radiko.radiko-cf.com"
    F_RADIKO = "https://f-radiko.smartstream.ne.jp"

    def __init__(self) -> None:
        self.tuple_ffmpeg_unsupported = self.get_tuple_ffmpeg_unsupported()

    def get_tuple_ffmpeg_unsupported(self) -> tuple[str, ...]:
        return (self.C_RPAA, self.SI_C_RADIKO, self.SI_F_RADIKO)

    def is_ffmpeg_supported(self, url: str) -> bool:
        return not url.startswith(self.tuple_ffmpeg_unsupported)


class LiveUrlChecker(UrlChecker):
    # Following URL forcibly connects not Time Free but Live
    C_RADIKO = "https://c-radiko.smartstream.ne.jp"


class TimeFreeUrlChecker(UrlChecker):
    """To check URL for Time Free whether FFmpeg supported or not."""

    RADIKO_JP = "https://radiko.jp"
    RPAA = "https://rpaa.smartstream.ne.jp"
    TF_C_RPAA_RADIKO = "https://tf-c-rpaa-radiko.smartstream.ne.jp"
    TF_F_RPAA_RADIKO = "https://tf-f-rpaa-radiko.smartstream.ne.jp"

    def get_tuple_ffmpeg_unsupported(self) -> tuple[str, ...]:
        return (*super().get_tuple_ffmpeg_unsupported(), self.TF_C_RPAA_RADIKO, self.TF_F_RPAA_RADIKO, self.RPAA)

    @staticmethod
    def is_fastest_host_to_download(url: str) -> bool:
        return url.startswith(TimeFreeUrlChecker.RADIKO_JP)


TypeVarHost = TypeVar("TypeVarHost", bound=UrlChecker)


class PlaylistCreateUrlGetter(Generic[TypeVarHost]):
    """Implements getting process URL to create playlist."""

    @classmethod
    def get(cls, station_id: str, headers: Mapping[str, str | bytes]) -> str:
        url = "https://radiko.jp/v3/station/stream/pc_html5/" + station_id + ".xml"
        response = Requester.get(url, headers)
        return cls.get_playlist_create_url(response.text)

    @staticmethod
    def has_premium_session(headers: Mapping[str, str | bytes]) -> bool:
        """Check whether headers carry a radiko premium session cookie."""
        cookie = headers.get("Cookie", "")
        cookie_text = cookie.decode("utf-8") if isinstance(cookie, bytes) else cookie
        return "radiko_session=" in cookie_text

    @classmethod
    def get_playlist_create_url(cls, string_xml: str) -> str:
        """Parse XML and extract target URL to create playlist."""
        root = ElementTree.fromstring(string_xml, forbid_dtd=True)
        list_url = [
            url
            for url in root.findall(".//url")
            if url.get("areafree") == "1" and url.get("timefree") == cls.time_free()
        ]
        list_playlist_create_url = [cls.strip_playlist_create_url(url) for url in list_url]
        return cls.filter_playlist_create_url(list_playlist_create_url)

    @classmethod
    def strip_playlist_create_url(cls, url: Element) -> str:
        """Strip playlist create URL."""
        element = url.find("./playlist_create_url")
        if element is None:
            msg = "playlist_create_url element not found"
            raise ValueError(msg)
        if element.text is None:
            msg = "playlist_create_url text is None"
            raise ValueError(msg)
        return element.text

    @classmethod
    def filter_playlist_create_url(cls, list_playlist_create_url: list[str]) -> str:
        """Filter playlist create URL.

        This method is the part divided from get_playlist_create_url() since radon grades unified method as B.
        """
        host = cls.create_host()
        try:
            candidacy = [
                playlist_create_url
                for playlist_create_url in list_playlist_create_url
                if cls.filter_url(playlist_create_url, host)
            ]
        except FoundFastestHostToDownload as error:
            return str(error)
        if candidacy:
            return candidacy[0]
        if list_playlist_create_url:
            msg = f"All candidate URLs are FFmpeg-unsupported: {list_playlist_create_url}"
            raise NoAvailableUrlError(msg)
        msg = f"No playlist create URL found in XML for timefree={cls.time_free()}"
        raise NoAvailableUrlError(msg)

    @classmethod
    @abstractmethod
    def time_free(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create_host(cls) -> TypeVarHost:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def filter_url(cls, playlist_create_url: str, host: TypeVarHost) -> bool:
        raise NotImplementedError


class LivePlaylistCreateUrlGetter(PlaylistCreateUrlGetter[LiveUrlChecker]):
    """Implements getting process Live URL to create playlist."""

    @classmethod
    def time_free(cls) -> str:
        return "0"

    @classmethod
    def create_host(cls) -> LiveUrlChecker:
        return LiveUrlChecker()

    @classmethod
    def filter_url(cls, playlist_create_url: str, host: UrlChecker) -> bool:
        return host.is_ffmpeg_supported(playlist_create_url)


class TimeFreePlaylistCreateUrlGetterBase(PlaylistCreateUrlGetter[TimeFreeUrlChecker]):
    """Shared implementation for time-free URL getters (7-day and 30-day).

    Unlike live playback, radiko's CDN enforces premium authentication on some area-free (``areafree="1"``) hosts for
    time-free content, while free accounts are only entitled to the in-area (``areafree="0"``) hosts. This class
    considers both, preferring in-area hosts unless the request headers carry a premium session cookie.
    """

    @classmethod
    def get(cls, station_id: str, headers: Mapping[str, str | bytes]) -> str:
        url = "https://radiko.jp/v3/station/stream/pc_html5/" + station_id + ".xml"
        response = Requester.get(url, headers)
        return cls.get_playlist_create_url(response.text, has_premium=cls.has_premium_session(headers))

    @classmethod
    def get_playlist_create_url(cls, string_xml: str, *, has_premium: bool = False) -> str:
        """Parse XML and extract target URL to create playlist.

        Args:
            string_xml: Station stream XML returned by radiko.
            has_premium: Whether the caller has a premium radiko session. Area-free URLs are preferred when `True`;
                in-area URLs are preferred otherwise, since free accounts are only entitled to those.
        """
        root = ElementTree.fromstring(string_xml, forbid_dtd=True)
        list_url = [url for url in root.findall(".//url") if url.get("timefree") == cls.time_free()]
        area_free = [cls.strip_playlist_create_url(url) for url in list_url if url.get("areafree") == "1"]
        in_area = [cls.strip_playlist_create_url(url) for url in list_url if url.get("areafree") == "0"]
        list_playlist_create_url = area_free + in_area if has_premium else in_area + area_free
        return cls.filter_playlist_create_url(list_playlist_create_url)

    @classmethod
    def time_free(cls) -> str:
        return "1"

    @classmethod
    def create_host(cls) -> TimeFreeUrlChecker:
        return TimeFreeUrlChecker()

    @classmethod
    def filter_url(cls, playlist_create_url: str, host: TimeFreeUrlChecker) -> bool:
        if host.is_fastest_host_to_download(playlist_create_url):
            raise FoundFastestHostToDownload(playlist_create_url)
        return host.is_ffmpeg_supported(playlist_create_url)


class TimeFreePlaylistCreateUrlGetter(TimeFreePlaylistCreateUrlGetterBase):
    """Implements getting process Time Free URL to create playlist."""


class TimeFree30DayPlaylistCreateUrlGetter(TimeFreePlaylistCreateUrlGetterBase):
    """Implements getting process Time Free 30-day URL to create playlist.

    This URL getter supports radiko's 30-day timefree feature (extended from the standard 7-day window). Uses the same
    XML filtering as TimeFreePlaylistCreateUrlGetter since the API XML response does not distinguish between 7-day and
    30-day content. The distinction is made at the query parameter level (type=c vs type=b).
    """
