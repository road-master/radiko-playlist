"""Tests for radikoplaylist.master_playlist_request"""
import re
from urllib.parse import urlparse

import pytest  # type: ignore

from radikoplaylist.master_playlist_request import LiveMasterPlaylistRequest, TimeFreeMasterPlaylistRequest
from tests.testlibraries.instance_resource import InstanceResource, ParameterExpectedUrl


class TestMasterPlaylistRequest:
    """Tests for MasterPlaylistRequest"""

    @staticmethod
    @pytest.mark.parametrize(
        "mock_get_playlist_create_url, station, expected_url",
        InstanceResource.concat(
            InstanceResource.LIST_STATION, InstanceResource.LIST_STATION, ParameterExpectedUrl.to_list(),
        ),
        indirect=["mock_get_playlist_create_url"],
    )
    # pylint: disable=unused-argument
    def test_make_master_playlist_url(mock_get_playlist_create_url, station, expected_url) -> None:
        """Method build_url() should build_url appropriate URL."""
        url = LiveMasterPlaylistRequest(station).build_url(InstanceResource.HEADERS_EXAMPLE)  # type: ignore
        parse_result_url = urlparse(url)
        expected_url.check(parse_result_url)

    @staticmethod
    def test_generate_uid() -> None:
        assert re.match(r"^[a-fA-F0-9]{32}$", TimeFreeMasterPlaylistRequest.generate_uid())
