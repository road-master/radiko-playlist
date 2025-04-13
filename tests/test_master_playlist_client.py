"""Test for radikoplaylist.master_playlist_client."""

from typing import Any, List, Tuple

import pytest
from requests_mock import Mocker

from radikoplaylist.exceptions import BadHttpStatusCodeError
from radikoplaylist import MasterPlaylistClient, TimeFreeMasterPlaylistRequest
from tests.testlibraries.instance_resource import InstanceResource


class TestConcat:
    """Test for concat()."""

    @staticmethod
    @pytest.mark.parametrize(
        ("parameter", "expected"),
        [
            (([],), []),
            ((["a", "b", "c"],), [["a"], ["b"], ["c"]]),
            ((["a", "b", "c"], ["A", "B", "C"]), [["a", "A"], ["b", "B"], ["c", "C"]]),
            ((["a", "b", "c"], ["A", "B", "C"], ["1", "2", "3"]), [["a", "A", "1"], ["b", "B", "2"], ["c", "C", "3"]]),
        ],
    )
    def test(parameter: Tuple[List[Any]], expected: List[Any]) -> None:
        """Method concat() should transpose array."""
        actual = InstanceResource.concat(*parameter)
        assert expected == actual


class TestMasterPlaylistClient:
    """Test for MasterPlaylistClient."""

    @staticmethod
    @pytest.mark.usefixtures("mock_get_playlist_create_url", "mock_auth_1", "mock_auth_2")
    @pytest.mark.parametrize(
        ("mock_get_playlist_create_url", "station"),
        InstanceResource.concat(
            InstanceResource.LIST_STATION,
            InstanceResource.LIST_STATION,
        ),
        indirect=["mock_get_playlist_create_url"],
    )
    def test_time_free(requests_mock: Mocker, station: str) -> None:
        """Method build_url() should reutrn appropriate master playlist."""
        date_time_start = 20200518215700
        date_time_end = 20200518220000
        expect_media_playlist_url = "https://radiko.jp/v2/api/ts/chunklist/Tt6TRp6b.m3u8"
        master_playlist_request = TimeFreeMasterPlaylistRequest(station, date_time_start, date_time_end)
        # Reason: To replace with mock
        master_playlist_request.generate_uid = InstanceResource.MOCK_GENERATE_UID  # type: ignore[method-assign]
        url = master_playlist_request.build_url(InstanceResource.HEADERS_EXAMPLE)
        expected_url = (
            "https://radiko.jp/v2/api/ts/playlist.m3u8?station_id="
            + station
            + (
                "&start_at=20200518215700"
                "&ft=20200518215700"
                "&end_at=20200518220000"
                "&to=20200518220000"
                "&l=15"
                "&lsid=45f59aed8851994d2d5ecc8e7a946018"
                "&type=b"
            )
        )
        assert url == expected_url
        requests_mock.get(url, content=InstanceResource.RESPONSE_CONTENT_MASTER_PLAY_LIST)
        master_playlist = MasterPlaylistClient.get(master_playlist_request)
        assert master_playlist.media_playlist_url == expect_media_playlist_url
        assert master_playlist.headers == InstanceResource.HEADERS_EXAMPLE

    @staticmethod
    @pytest.mark.usefixtures("mock_get_playlist_create_url", "mock_auth_1", "mock_auth_2")
    @pytest.mark.parametrize(
        ("status_code", "mock_get_playlist_create_url", "station"),
        InstanceResource.combination(
            [[value] for value in InstanceResource.LIST_STATUS_CODE_ERROR],
            InstanceResource.concat(
                ["NACK5"],
                ["NACK5"],
            ),
        ),
        indirect=["mock_get_playlist_create_url"],
    )
    # pylint: disable=unused-argument
    def test_error(requests_mock: Mocker, status_code: int, station: str) -> None:
        """Method build_url() should raise error when HTTP status code is not 200."""
        date_time_start = 20200518215700
        date_time_end = 20200518220000
        master_playlist_request = TimeFreeMasterPlaylistRequest(station, date_time_start, date_time_end)
        # Reason: To replace with mock
        master_playlist_request.generate_uid = InstanceResource.MOCK_GENERATE_UID  # type: ignore[method-assign]
        url = master_playlist_request.build_url(InstanceResource.HEADERS_EXAMPLE)
        requests_mock.get(url, status_code=status_code)
        with pytest.raises(BadHttpStatusCodeError):
            MasterPlaylistClient.get(master_playlist_request)
