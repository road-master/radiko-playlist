"""Test for radikoplaylist.authorization"""
import pytest  # type: ignore

from radikoplaylist.authorization import Authorization
from radikoplaylist.exceptions import BadHttpStatusCodeError, HttpRequestTimeoutError


class TestAuthorization:
    """Test for Authorization"""

    @staticmethod
    # pylint: disable=unused-argument
    def test_timeout(mock_auth_1_timeout) -> None:
        with pytest.raises(HttpRequestTimeoutError):
            authorization = Authorization()
            authorization.auth()

    @staticmethod
    # pylint: disable=unused-argument
    def test_status_code_error(mock_auth_1_status_code) -> None:
        with pytest.raises(BadHttpStatusCodeError):
            authorization = Authorization()
            authorization.auth()
