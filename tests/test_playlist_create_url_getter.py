"""Tests for radikoplaylist.playlist_create_url_getter."""

from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import pytest
from defusedxml import ElementTree

from radikoplaylist.exceptions import NoAvailableUrlError
from radikoplaylist.playlist_create_url_getter import LivePlaylistCreateUrlGetter
from radikoplaylist.playlist_create_url_getter import PlaylistCreateUrlGetter
from radikoplaylist.playlist_create_url_getter import TimeFree30DayPlaylistCreateUrlGetter
from radikoplaylist.playlist_create_url_getter import TimeFreePlaylistCreateUrlGetter
from radikoplaylist.playlist_create_url_getter import TimeFreeUrlChecker
from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.instance_resource import ParameterExpectedLivePlaylistCreateUrlString

if TYPE_CHECKING:
    # - defusedxml lacks an Element class · Issue #48 · tiran/defusedxml
    #   https://github.com/tiran/defusedxml/issues/48#issuecomment-1511284750
    from xml.etree.ElementTree import Element  # nosec B405

HTML_PLAYLIST_CREATE_URL = dedent("""\
    <?xml version="1.0"?>
    <data>
        <playlist_create_url>https://radiko.jp/v2/api/ts/playlist.m3u8</playlist_create_url>
    </data>
""")
HTML_PLAYLIST_CREATE_URL_ELEMENT_NOT_FOUND = dedent("""\
    <?xml version="1.0"?>
    <data>
    </data>
""")
HTML_PLAYLIST_CREATE_URL_ELEMENT_TEXT_IS_NONE = dedent("""\
    <?xml version="1.0"?>
    <data>
        <playlist_create_url></playlist_create_url>
    </data>
""")

LIST_TIME_FREE_GETTER_CLASS = [TimeFreePlaylistCreateUrlGetter, TimeFree30DayPlaylistCreateUrlGetter]


class TestPlaylistCreateUrlGetter:
    """Tests for PlaylistCreateUrlGetter."""

    @staticmethod
    @pytest.mark.parametrize(
        ("xml_playlist_create_url", "expected"),
        InstanceResource.concat(
            InstanceResource.LIST_STATION,
            ParameterExpectedLivePlaylistCreateUrlString.to_list(),
        ),
        indirect=["xml_playlist_create_url"],
    )
    def test_live(xml_playlist_create_url: str, expected: str) -> None:
        """Method get_playlist_create_url should return appropriate URL."""
        assert LivePlaylistCreateUrlGetter.get_playlist_create_url(xml_playlist_create_url) == expected

    @staticmethod
    @pytest.mark.parametrize(
        "xml_playlist_create_url",
        ["SYNTHETIC-LIVE-AREAFREE-DENIED"],
        indirect=["xml_playlist_create_url"],
    )
    def test_live_falls_back_to_in_area(xml_playlist_create_url: str) -> None:
        """Method get_playlist_create_url should fall back to an in-area URL when area-free is FFmpeg-unsupported."""
        url = LivePlaylistCreateUrlGetter.get_playlist_create_url(xml_playlist_create_url)
        assert url == "https://f-radiko.smartstream.ne.jp/DUMMY/_definst_/simul-stream.stream/playlist.m3u8"

    @staticmethod
    @pytest.mark.parametrize(
        "xml_playlist_create_url",
        ["TBS"],
        indirect=["xml_playlist_create_url"],
    )
    def test_live_prefers_area_free(xml_playlist_create_url: str) -> None:
        """Method get_playlist_create_url should prefer area-free URL for live regardless of premium status."""
        url = LivePlaylistCreateUrlGetter.get_playlist_create_url(xml_playlist_create_url, has_premium=False)
        assert url == "https://c-radiko.smartstream.ne.jp/TBS/_definst_/simul-stream.stream/playlist.m3u8"

    @staticmethod
    @pytest.mark.parametrize(
        "xml_playlist_create_url",
        InstanceResource.LIST_STATION,
        indirect=["xml_playlist_create_url"],
    )
    def test_time_free(xml_playlist_create_url: str) -> None:
        """Method get_playlist_create_url should return appropriate URL."""
        url = TimeFreePlaylistCreateUrlGetter.get_playlist_create_url(xml_playlist_create_url)
        assert url == "https://radiko.jp/v2/api/ts/playlist.m3u8"

    @staticmethod
    @pytest.mark.parametrize(
        "xml_playlist_create_url",
        InstanceResource.LIST_STATION,
        indirect=["xml_playlist_create_url"],
    )
    def test_time_free_30day(xml_playlist_create_url: str) -> None:
        """Method get_playlist_create_url should return appropriate URL for 30-day timefree."""
        url = TimeFree30DayPlaylistCreateUrlGetter.get_playlist_create_url(xml_playlist_create_url)
        assert url == "https://radiko.jp/v2/api/ts/playlist.m3u8"

    @staticmethod
    @pytest.mark.parametrize("getter_cls", LIST_TIME_FREE_GETTER_CLASS)
    @pytest.mark.parametrize(
        "xml_playlist_create_url",
        ["SYNTHETIC-MIXED-AREAFREE"],
        indirect=["xml_playlist_create_url"],
    )
    def test_time_free_mixed_areafree_free_account(
        xml_playlist_create_url: str,
        getter_cls: type[PlaylistCreateUrlGetter[TimeFreeUrlChecker]],
    ) -> None:
        """Method get_playlist_create_url should prefer the in-area URL when no premium session is present."""
        url = getter_cls.get_playlist_create_url(xml_playlist_create_url, has_premium=False)
        assert url == "https://tf-rpaa.smartstream.ne.jp/tf/playlist.m3u8"

    @staticmethod
    @pytest.mark.parametrize("getter_cls", LIST_TIME_FREE_GETTER_CLASS)
    @pytest.mark.parametrize(
        "xml_playlist_create_url",
        ["SYNTHETIC-MIXED-AREAFREE"],
        indirect=["xml_playlist_create_url"],
    )
    def test_time_free_mixed_areafree_premium(
        xml_playlist_create_url: str,
        getter_cls: type[PlaylistCreateUrlGetter[TimeFreeUrlChecker]],
    ) -> None:
        """Method get_playlist_create_url should prefer the area-free URL when a premium session is present."""
        url = getter_cls.get_playlist_create_url(xml_playlist_create_url, has_premium=True)
        assert url == "https://dr-wowza.radiko-cf.com/tf/playlist.m3u8"

    @staticmethod
    @pytest.mark.parametrize("has_premium", [False, True])
    @pytest.mark.parametrize("getter_cls", LIST_TIME_FREE_GETTER_CLASS)
    @pytest.mark.parametrize(
        "xml_playlist_create_url",
        ["SYNTHETIC-AREAFREE-DENIED"],
        indirect=["xml_playlist_create_url"],
    )
    def test_time_free_area_free_denied_falls_back_to_in_area(
        xml_playlist_create_url: str,
        getter_cls: type[PlaylistCreateUrlGetter[TimeFreeUrlChecker]],
        has_premium: bool,  # noqa: FBT001
    ) -> None:
        """Method get_playlist_create_url should fall back to in-area URL when all area-free candidates are denied."""
        url = getter_cls.get_playlist_create_url(xml_playlist_create_url, has_premium=has_premium)
        assert url == "https://tf-rpaa.smartstream.ne.jp/tf/playlist.m3u8"

    @staticmethod
    @pytest.mark.parametrize("getter_cls", LIST_TIME_FREE_GETTER_CLASS)
    @pytest.mark.parametrize(
        "xml_playlist_create_url",
        ["SYNTHETIC-ALL-DENIED"],
        indirect=["xml_playlist_create_url"],
    )
    def test_time_free_all_denied_raises_with_unsupported_message(
        xml_playlist_create_url: str,
        getter_cls: type[PlaylistCreateUrlGetter[TimeFreeUrlChecker]],
    ) -> None:
        """Method get_playlist_create_url should raise NoAvailableUrlError distinguishing all-unsupported case."""
        with pytest.raises(NoAvailableUrlError, match="FFmpeg-unsupported"):
            getter_cls.get_playlist_create_url(xml_playlist_create_url)

    @staticmethod
    @pytest.mark.parametrize("getter_cls", LIST_TIME_FREE_GETTER_CLASS)
    @pytest.mark.parametrize(
        "xml_playlist_create_url",
        ["SYNTHETIC-NO-TIMEFREE"],
        indirect=["xml_playlist_create_url"],
    )
    def test_time_free_no_url_raises_with_no_url_message(
        xml_playlist_create_url: str,
        getter_cls: type[PlaylistCreateUrlGetter[TimeFreeUrlChecker]],
    ) -> None:
        """Method get_playlist_create_url should raise NoAvailableUrlError distinguishing the empty-XML case."""
        with pytest.raises(NoAvailableUrlError, match="No playlist create URL"):
            getter_cls.get_playlist_create_url(xml_playlist_create_url)

    @staticmethod
    @pytest.mark.parametrize("getter_cls", LIST_TIME_FREE_GETTER_CLASS)
    @pytest.mark.parametrize(
        "xml_playlist_create_url",
        ["TBS"],
        indirect=["xml_playlist_create_url"],
    )
    def test_time_free_fastest_host_short_circuit_with_premium(
        xml_playlist_create_url: str,
        getter_cls: type[PlaylistCreateUrlGetter[TimeFreeUrlChecker]],
    ) -> None:
        """Method get_playlist_create_url should still short-circuit to radiko.jp when a premium session is present."""
        url = getter_cls.get_playlist_create_url(xml_playlist_create_url, has_premium=True)
        assert url == "https://radiko.jp/v2/api/ts/playlist.m3u8"

    def test_strip_playlist_create_url(self) -> None:
        """Method strip_playlist_create_url should return appropriate URL."""
        element_url = ElementTree.fromstring(HTML_PLAYLIST_CREATE_URL, forbid_dtd=True)
        url = LivePlaylistCreateUrlGetter.strip_playlist_create_url(element_url)
        assert url == "https://radiko.jp/v2/api/ts/playlist.m3u8"

    @pytest.mark.parametrize(
        ("element_url", "error_message"),
        [
            (
                ElementTree.fromstring(HTML_PLAYLIST_CREATE_URL_ELEMENT_NOT_FOUND, forbid_dtd=True),
                "playlist_create_url element not found",
            ),
            (
                ElementTree.fromstring(HTML_PLAYLIST_CREATE_URL_ELEMENT_TEXT_IS_NONE, forbid_dtd=True),
                "playlist_create_url text is None",
            ),
        ],
    )
    def test_strip_playlist_create_url_error(self, element_url: Element, error_message: str) -> None:
        """Method strip_playlist_create_url should raise ValueError."""
        # Reason: The mypy's issue:
        #   Incompatible types in assignment (expression has type "str", variable has type "Element")
        with pytest.raises(ValueError, match=error_message):
            LivePlaylistCreateUrlGetter.strip_playlist_create_url(element_url)

    def test_has_premium_session(self) -> None:
        """Method has_premium_session should return True when the Cookie header carries a radiko_session."""
        assert PlaylistCreateUrlGetter.has_premium_session({"Cookie": "radiko_session=abc123"}) is True

    def test_has_premium_session_no_cookie(self) -> None:
        """Method has_premium_session should return False when no radiko_session cookie is present."""
        assert PlaylistCreateUrlGetter.has_premium_session(InstanceResource.HEADERS_EXAMPLE) is False

    def test_has_premium_session_bytes_cookie(self) -> None:
        """Method has_premium_session should decode a bytes Cookie header before matching."""
        assert PlaylistCreateUrlGetter.has_premium_session({"Cookie": b"radiko_session=abc123"}) is True
