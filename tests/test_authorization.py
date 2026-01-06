"""Test for radikoplaylist.authorization."""

import pytest

from radikoplaylist.authorization import Authorization
from radikoplaylist.exceptions import BadHttpStatusCodeError
from radikoplaylist.exceptions import HttpRequestTimeoutError


class TestAuthorization:
    """Test for Authorization."""

    @staticmethod
    @pytest.mark.usefixtures("mock_auth_1_timeout")
    def test_timeout() -> None:
        authorization = Authorization()
        with pytest.raises(HttpRequestTimeoutError):
            authorization.auth()

    @staticmethod
    @pytest.mark.usefixtures("mock_auth_1_status_code")
    def test_status_code_error() -> None:
        authorization = Authorization()
        with pytest.raises(BadHttpStatusCodeError):
            authorization.auth()

    @staticmethod
    @pytest.mark.usefixtures("mock_auth_1", "mock_auth_2")
    def test_with_radiko_session() -> None:
        """Test that radiko_session cookie is added to headers."""
        radiko_session = "test_session_value_123"
        authorization = Authorization(radiko_session=radiko_session)
        headers = authorization.auth()
        assert "Cookie" in headers
        assert headers["Cookie"] == f"radiko_session={radiko_session}"
