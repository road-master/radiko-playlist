"""Config of pytest."""
from typing import Generator

import pytest  # type: ignore
from requests.exceptions import ConnectTimeout

from tests.testlibraries.instance_resource import InstanceResource


@pytest.fixture
def mock_auth_1(requests_mock) -> None:
    requests_mock.get(
        InstanceResource.URL_RADIKO_AUTH_1, headers=InstanceResource.RESPONSE_HEADER_AUTH_1_EXAMPLE,
    )


@pytest.fixture
def mock_auth_1_timeout(requests_mock) -> None:
    requests_mock.get(
        InstanceResource.URL_RADIKO_AUTH_1, exc=ConnectTimeout,
    )


@pytest.fixture(params=InstanceResource.LIST_STATUS_CODE_ERROR)
def mock_auth_1_status_code(requests_mock, request) -> None:
    requests_mock.get(
        InstanceResource.URL_RADIKO_AUTH_1,
        headers=InstanceResource.RESPONSE_HEADER_AUTH_1_EXAMPLE,
        status_code=request.param,
    )


@pytest.fixture
def mock_auth_2(requests_mock) -> None:
    requests_mock.get(InstanceResource.URL_RADIKO_AUTH_2)


@pytest.fixture
def xml_playlist_create_url(resource_path_root, request) -> Generator[str, None, None]:
    yield get_xml_text(request, resource_path_root)


@pytest.fixture
def mock_get_playlist_create_url(requests_mock, resource_path_root, request) -> None:
    requests_mock.get(
        InstanceResource.URL_RADIKO_STREAM_PC_HTML_5 + request.param + ".xml",
        text=get_xml_text(request, resource_path_root),
    )


def get_xml_text(request, resource_path_root) -> str:
    return (resource_path_root / "xml_playlist_create_url" / (request.param + ".xml")).read_text()
