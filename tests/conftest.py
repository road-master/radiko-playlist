"""Config of pytest."""

from pathlib import Path
from typing import cast

import pytest
from requests.exceptions import ConnectTimeout
from requests_mock import Mocker

from tests.testlibraries.instance_resource import InstanceResource


@pytest.fixture
def mock_auth_1(requests_mock: Mocker) -> None:
    requests_mock.get(
        InstanceResource.URL_RADIKO_AUTH_1,
        headers=InstanceResource.RESPONSE_HEADER_AUTH_1_EXAMPLE,
    )


@pytest.fixture
def mock_auth_1_timeout(requests_mock: Mocker) -> None:
    requests_mock.get(
        InstanceResource.URL_RADIKO_AUTH_1,
        exc=ConnectTimeout,
    )


@pytest.fixture(params=InstanceResource.LIST_STATUS_CODE_ERROR)
def mock_auth_1_status_code(requests_mock: Mocker, request: "pytest.FixtureRequest") -> None:
    requests_mock.get(
        InstanceResource.URL_RADIKO_AUTH_1,
        headers=InstanceResource.RESPONSE_HEADER_AUTH_1_EXAMPLE,
        status_code=request.param,
    )


@pytest.fixture
def mock_auth_2(requests_mock: Mocker) -> None:
    requests_mock.get(InstanceResource.URL_RADIKO_AUTH_2)


@pytest.fixture
def xml_playlist_create_url(resource_path_root: Path, request: "pytest.FixtureRequest") -> str:
    return get_xml_text(request, resource_path_root)


@pytest.fixture
def mock_get_playlist_create_url(
    requests_mock: Mocker,
    resource_path_root: Path,
    request: "pytest.FixtureRequest",
) -> None:
    requests_mock.get(
        InstanceResource.URL_RADIKO_STREAM_PC_HTML_5 + request.param + ".xml",
        text=get_xml_text(request, resource_path_root),
    )


def get_xml_text(request: "pytest.FixtureRequest", resource_path_root: Path) -> str:
    return cast("str", (resource_path_root / "xml_playlist_create_url" / (request.param + ".xml")).read_text())
