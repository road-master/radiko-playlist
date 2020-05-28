"""Tests for radikoplaylist.playlist_create_url_getter"""
import pytest  # type: ignore

from radikoplaylist.playlist_create_url_getter import PlaylistCreateUrlGetter
from tests.testlibraries.instance_resource import InstanceResource, ParameterExpectedPlaylistCreateUrlString


class TestPlaylistCreateUrlGetter:
    """Tests for PlaylistCreateUrlGetter"""

    @staticmethod
    @pytest.mark.parametrize(
        "xml_playlist_create_url, expected",
        InstanceResource.concat(InstanceResource.LIST_STATION, ParameterExpectedPlaylistCreateUrlString.to_list(),),
        indirect=["xml_playlist_create_url"],
    )
    def test(xml_playlist_create_url, expected):
        """Method get_playlist_create_url should return appropriate URL."""
        assert PlaylistCreateUrlGetter.get_playlist_create_url(xml_playlist_create_url, True) == expected
