"""Tests for radikoplaylist.playlist_create_url_getter."""
import pytest

from radikoplaylist.playlist_create_url_getter import LivePlaylistCreateUrlGetter, TimeFreePlaylistCreateUrlGetter
from tests.testlibraries.instance_resource import InstanceResource, ParameterExpectedLivePlaylistCreateUrlString


class TestPlaylistCreateUrlGetter:
    """Tests for PlaylistCreateUrlGetter."""

    @staticmethod
    @pytest.mark.parametrize(
        "xml_playlist_create_url, expected",
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
