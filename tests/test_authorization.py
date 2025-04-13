"""Test for radikoplaylist.authorization."""

import pytest

from radikoplaylist.authorization import Authorization
from radikoplaylist.exceptions import BadHttpStatusCodeError, HttpRequestTimeoutError


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
