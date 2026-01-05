"""To unify error check and logging process."""

from __future__ import annotations

from logging import getLogger
from typing import Mapping

import requests
from requests import Response
from requests import Timeout

from radikoplaylist.exceptions import BadHttpStatusCodeError
from radikoplaylist.exceptions import HttpRequestTimeoutError


class Requester:
    """To unify error check and logging process."""

    HTTP_STATUS_CODE_OK = 200

    @staticmethod
    def get(url: str, headers: Mapping[str, str | bytes]) -> Response:
        """Get request with error check and logging process."""
        logger = getLogger(__name__)
        try:
            res = requests.get(url=url, headers=headers, timeout=5.0)
        except Timeout as error:
            logger.warning("failed in %s.", url)
            logger.warning("Request Timeout")
            logger.warning(error)
            raise HttpRequestTimeoutError("failed in " + url + ".") from error
        if res.status_code != Requester.HTTP_STATUS_CODE_OK:
            logger.warning("failed in %s.", url)
            logger.warning("status_code:%s", res.status_code)
            logger.warning("content:%s", res.content)
            raise BadHttpStatusCodeError("failed in " + url + ".")
        logger.debug("auth in %s is success.", url)
        return res
