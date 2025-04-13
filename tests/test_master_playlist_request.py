"""Tests for radikoplaylist.master_playlist_request."""

import re
from urllib.parse import urlparse

import pytest

from radikoplaylist.master_playlist_request import LiveMasterPlaylistRequest, TimeFreeMasterPlaylistRequest
from tests.testlibraries.expected_url import ExpectedUrl
from tests.testlibraries.instance_resource import (
    InstanceResource,
    ParameterExpectedLiveUrl,
    ParameterExpectedTimeFreeUrl,
)


class TestMasterPlaylistRequest:
    """Tests for MasterPlaylistRequest."""

    @staticmethod
    @pytest.mark.usefixtures("mock_get_playlist_create_url")
    @pytest.mark.parametrize(
        ("mock_get_playlist_create_url", "station", "expected_url"),
        InstanceResource.concat(
            InstanceResource.LIST_STATION,
            InstanceResource.LIST_STATION,
            ParameterExpectedLiveUrl.to_list(),
        ),
        indirect=["mock_get_playlist_create_url"],
    )
    # pylint: disable=unused-argument
    def test_build_live_master_playlist_url(station: str, expected_url: ExpectedUrl) -> None:
        """Method build_url() should build_url appropriate URL."""
        url = LiveMasterPlaylistRequest(station).build_url(InstanceResource.HEADERS_EXAMPLE)
        parse_result_url = urlparse(url)
        expected_url.check(parse_result_url)

    @staticmethod
    @pytest.mark.usefixtures("mock_get_playlist_create_url")
    @pytest.mark.parametrize(
        ("mock_get_playlist_create_url", "station", "expected_url"),
        InstanceResource.concat(
            InstanceResource.LIST_STATION,
            InstanceResource.LIST_STATION,
            ParameterExpectedTimeFreeUrl.to_list(),
        ),
        indirect=["mock_get_playlist_create_url"],
    )
    # pylint: disable=unused-argument
    def test_build_time_free_master_playlist_url(station: str, expected_url: ExpectedUrl) -> None:
        """Method build_url() should build_url appropriate URL."""
        date_time_start = 20200518215700
        date_time_end = 20200518220000
        playlist_request = TimeFreeMasterPlaylistRequest(station, date_time_start, date_time_end)
        url = playlist_request.build_url(InstanceResource.HEADERS_EXAMPLE)
        parse_result_url = urlparse(url)
        expected_url.check(parse_result_url)

    @staticmethod
    def test_generate_uid() -> None:
        assert re.match(r"^[a-fA-F0-9]{32}$", TimeFreeMasterPlaylistRequest.generate_uid())
