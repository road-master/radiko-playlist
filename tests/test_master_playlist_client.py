"""Test for radikoplaylist.master_playlist_client"""
import pytest  # type: ignore

from radikoplaylist import MasterPlaylistClient, TimeFreeMasterPlaylistRequest
from radikoplaylist.exceptions import BadHttpStatusCodeError
from tests.testlibraries.instance_resource import InstanceResource


class TestMasterPlaylistClient:
    """Test fpr MasterPlaylistClient"""

    @staticmethod
    @pytest.mark.parametrize(
        "mock_get_playlist_create_url, station",
        InstanceResource.concat(InstanceResource.LIST_STATION, InstanceResource.LIST_STATION),
        indirect=["mock_get_playlist_create_url"],
    )
    # pylint: disable=unused-argument
    def test(mock_auth_1, mock_auth_2, mock_get_playlist_create_url, requests_mock, station) -> None:
        """Method build_url() should reutrn appropriate master playlist."""
        date_time_start = 20200518215700
        date_time_end = 20200518220000
        expect_url = "https://radiko.jp/v2/api/ts/chunklist/Tt6TRp6b.m3u8"
        master_playlist_request = TimeFreeMasterPlaylistRequest(station, date_time_start, date_time_end)
        # noinspection PyTypeHints
        master_playlist_request.generate_uid = InstanceResource.MOCK_GENERATE_UID  # type: ignore
        url = master_playlist_request.build_url(InstanceResource.HEADERS_EXAMPLE)  # type: ignore
        requests_mock.get(
            url,
            # request_headers=InstanceResource.RESPONSE_HEADER_AUTH_1_EXAMPLE,
            content=InstanceResource.RESPONSE_CONTENT_MASTER_PLAY_LIST,
        )
        master_playlist = MasterPlaylistClient.get(master_playlist_request)
        assert master_playlist.media_playlist_url == expect_url
        assert master_playlist.headers == InstanceResource.HEADERS_EXAMPLE

    @staticmethod
    @pytest.mark.parametrize(
        "status_code, mock_get_playlist_create_url, station",
        InstanceResource.combination(
            [[value] for value in InstanceResource.LIST_STATUS_CODE_ERROR],
            InstanceResource.concat(["NACK5"], ["NACK5"],),
        ),
        indirect=["mock_get_playlist_create_url"],
    )
    # pylint: disable=unused-argument,too-many-arguments
    def test_error(mock_auth_1, mock_auth_2, mock_get_playlist_create_url, requests_mock, status_code, station) -> None:
        """Method build_url() should raise error when HTTP status code is not 200."""
        date_time_start = 20200518215700
        date_time_end = 20200518220000
        master_playlist_request = TimeFreeMasterPlaylistRequest(station, date_time_start, date_time_end)
        # noinspection PyTypeHints
        master_playlist_request.generate_uid = InstanceResource.MOCK_GENERATE_UID  # type: ignore
        url = master_playlist_request.build_url(InstanceResource.HEADERS_EXAMPLE)  # type: ignore
        requests_mock.get(
            url,
            # request_headers=InstanceResource.RESPONSE_HEADER_AUTH_1_EXAMPLE,
            status_code=status_code,
        )
        with pytest.raises(BadHttpStatusCodeError):
            MasterPlaylistClient.get(master_playlist_request)
