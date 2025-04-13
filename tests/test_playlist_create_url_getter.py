"""Tests for radikoplaylist.playlist_create_url_getter."""

from typing import TYPE_CHECKING

from defusedxml import ElementTree
import pytest

from radikoplaylist.playlist_create_url_getter import LivePlaylistCreateUrlGetter, TimeFreePlaylistCreateUrlGetter
from tests.testlibraries.instance_resource import InstanceResource, ParameterExpectedLivePlaylistCreateUrlString

if TYPE_CHECKING:
    # - defusedxml lacks an Element class · Issue #48 · tiran/defusedxml
    #   https://github.com/tiran/defusedxml/issues/48#issuecomment-1511284750
    from xml.etree.ElementTree import Element  # nosec B405


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
        InstanceResource.LIST_STATION,
        indirect=["xml_playlist_create_url"],
    )
    def test_time_free(xml_playlist_create_url: str) -> None:
        """Method get_playlist_create_url should return appropriate URL."""
        url = TimeFreePlaylistCreateUrlGetter.get_playlist_create_url(xml_playlist_create_url)
        assert url == "https://radiko.jp/v2/api/ts/playlist.m3u8"

    def test_strip_playlist_create_url(self) -> None:
        """Method strip_playlist_create_url should return appropriate URL."""
        element_url = ElementTree.fromstring(
            """<?xml version="1.0"?>
            <data>
                <playlist_create_url>https://radiko.jp/v2/api/ts/playlist.m3u8</playlist_create_url>"
            </data>
            """,
            forbid_dtd=True,
        )
        url = LivePlaylistCreateUrlGetter.strip_playlist_create_url(element_url)
        assert url == "https://radiko.jp/v2/api/ts/playlist.m3u8"

    @pytest.mark.parametrize(
        ("element_url", "error_message"),
        [
            (
                ElementTree.fromstring(
                    """<?xml version="1.0"?>
                    <data>
                    </data>
                    """,
                    forbid_dtd=True,
                ),
                "playlist_create_url element not found",
            ),
            (
                ElementTree.fromstring(
                    """<?xml version="1.0"?>
                    <data>
                        <playlist_create_url></playlist_create_url>"
                    </data>
                    """,
                    forbid_dtd=True,
                ),
                "playlist_create_url text is None",
            ),
        ],
    )
    def test_strip_playlist_create_url_error(self, element_url: "Element", error_message: str) -> None:
        """Method strip_playlist_create_url should raise ValueError."""
        # Reason: The mypy's issue:
        #   Incompatible types in assignment (expression has type "str", variable has type "Element")
        with pytest.raises(ValueError, match=error_message):
            LivePlaylistCreateUrlGetter.strip_playlist_create_url(element_url)
