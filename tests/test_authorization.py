"""Test for radikoplaylist.authorization."""
import pytest

from radikoplaylist.authorization import Authorization
from radikoplaylist.exceptions import BadHttpStatusCodeError, HttpRequestTimeoutError


class TestAuthorization:
    """Test for Authorization."""

    @staticmethod
    @pytest.mark.usefixtures("mock_auth_1_timeout")
    def test_timeout() -> None:
        with pytest.raises(HttpRequestTimeoutError):
            authorization = Authorization()
            authorization.auth()

    @staticmethod
    @pytest.mark.usefixtures("mock_auth_1_status_code")
    def test_status_code_error() -> None:
        with pytest.raises(BadHttpStatusCodeError):
            authorization = Authorization()
            authorization.auth()
