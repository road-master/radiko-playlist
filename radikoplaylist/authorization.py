"""Implements authorization for radiko API."""

import base64
from logging import getLogger
from typing import Dict, MutableMapping, Union

from requests import Response

from radikoplaylist.requester import Requester


class Authorization:
    """Authorization for radiko API."""

    ARIA_ID_DEFAULT = "JP13"  # TOKYO
    _AUTH1_URL = "https://radiko.jp/v2/api/auth1"
    _AUTH2_URL = "https://radiko.jp/v2/api/auth2"
    # Value is defined in specification of radiko API
    # @see http://radiko.jp/apps/js/playerCommon.js
    _RADIKO_AUTH_KEY = b"bcd151073c03b352e1ef2fd66c32209da9ca0afa"

    def __init__(self, *, area_id: str = ARIA_ID_DEFAULT) -> None:
        """Key X-Radiko-*** in headers is required in specification of radiko API."""
        self._headers: MutableMapping[str, str | bytes] = {
            "User-Agent": "python3.7",
            "Accept": "*/*",
            "X-Radiko-App": "pc_html5",
            "X-Radiko-App-Version": "0.0.1",
            "X-Radiko-User": "dummy_user",
            "X-Radiko-Device": "pc",
            "X-Radiko-AuthToken": "",
            "X-Radiko-Partialkey": b"",
            "X-Radiko-AreaId": area_id,
        }
        self.logger = getLogger(__name__)

    def auth(self) -> Dict[str, Union[str, bytes]]:
        """Authorizes radiko API and returns authorized HTTP headers."""
        res = Requester.get(Authorization._AUTH1_URL, self._headers)
        self._headers["X-Radiko-AuthToken"] = self._get_auth_token(res)
        # noinspection PyTypeChecker
        self._headers["X-Radiko-Partialkey"] = self._get_partial_key(res)
        res = Requester.get(Authorization._AUTH2_URL, self._headers)
        self.logger.debug("authenticated headers:%s", self._headers)
        self.logger.debug("res.headers:%s", res.headers)
        self.logger.debug("res.content:%s", res.content)
        self._headers["Connection"] = "keep-alive"
        self.logger.debug("headers: %s", self._headers)
        # Mypy's issue:
        #   Incompatible return value type (got "dict[str, str]", expected "dict[str, str | bytes]")
        return self._headers  # type: ignore[return-value]

    @staticmethod
    def _get_auth_token(response: Response) -> str:
        return response.headers["X-Radiko-AUTHTOKEN"]

    @staticmethod
    def _get_partial_key(response: Response) -> bytes:
        """Gets partial key for authorize from HTTP response.

        Algorithm is based on function createPartialkey() in following URL.

        @see
        http://radiko.jp/apps/js/radikoJSPlayer.js
        """
        length = int(response.headers["X-Radiko-KeyLength"])
        offset = int(response.headers["X-Radiko-KeyOffset"])
        return base64.b64encode(Authorization._RADIKO_AUTH_KEY[offset : offset + length])
