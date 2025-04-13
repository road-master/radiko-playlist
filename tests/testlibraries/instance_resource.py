"""Implements instance resources."""

from logging import getLogger
import re
from typing import Any, cast, ClassVar, Dict, List, TypeVar, Union
from unittest.mock import MagicMock

import numpy as np

from tests.testlibraries.expected_url import ExpectedUrl, ExpectedUrlProperties

A = TypeVar("A")
B = TypeVar("B")


# pylint: disable=too-few-public-methods
class InstanceResource:
    """Implements instance resources."""

    URL_RADIKO_AUTH_1 = "https://radiko.jp/v2/api/auth1"
    URL_RADIKO_AUTH_2 = "https://radiko.jp/v2/api/auth2"
    URL_RADIKO_STREAM_PC_HTML_5 = "https://radiko.jp/v3/station/stream/pc_html5/"
    # Reason: This is not hardcoded password
    RADIKO_AUTH_TOKEN_EXAMPLE = "HrUNR0zyrGseqvlPl1-khQ"  # noqa: S105 # nosec: B105
    RADIKO_KEY_LENGTH_EXAMPLE = "16"
    RADIKO_KEY_OFFSET_EXAMPLE = "16"
    RESPONSE_HEADER_AUTH_1_EXAMPLE: ClassVar[Dict[str, str]] = {
        "X-Radiko-AUTHTOKEN": RADIKO_AUTH_TOKEN_EXAMPLE,
        "X-Radiko-KeyLength": RADIKO_KEY_LENGTH_EXAMPLE,
        "X-Radiko-KeyOffset": RADIKO_KEY_OFFSET_EXAMPLE,
    }
    RESPONSE_CONTENT_AUTH_1_EXAMPLE = b"""
#EXTM3U
#EXT-X-VERSION:6
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=52973,CODECS="mp4a.40.5
https://rpaa.smartstream.ne.jp/medialist?session=Q3fHC9Smzp8x49j9AqicBL
"""
    RESPONSE_CONTENT_MASTER_PLAY_LIST = b"""
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=52973,CODECS="mp4a.40.5"
https://radiko.jp/v2/api/ts/chunklist/Tt6TRp6b.m3u8
"""
    MOCK_GENERATE_UID = MagicMock(
        name="generate_uid",
        return_value="45f59aed8851994d2d5ecc8e7a946018",
    )
    LIST_STATUS_CODE_ERROR: ClassVar[List[int]] = [
        400,
        403,
        404,
        500,
        502,
        503,
        504,
    ]
    LIST_STATION: ClassVar[List[str]] = [
        "BAYFM78",
        "FMJ",
        "FMR",
        "FMT",
        "HOUSOU-DAIGAKU",
        "INT",
        "JOAK",
        "JOAK-FM",
        "JORF",
        "LFR",
        "NACK5",
        "QRR",
        "RN1",
        "RN2",
        "TBS",
        "YFM",
    ]
    HEADERS_EXAMPLE: ClassVar[Dict[str, Union[str, bytes]]] = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "User-Agent": "python3.7",
        "X-Radiko-App": "pc_html5",
        "X-Radiko-App-Version": "0.0.1",
        "X-Radiko-AreaId": "JP13",
        "X-Radiko-AuthToken": "HrUNR0zyrGseqvlPl1-khQ",
        "X-Radiko-Device": "pc",
        "X-Radiko-Partialkey": b"ZTFlZjJmZDY2YzMyMjA5ZA==",
        "X-Radiko-User": "dummy_user",
    }
    PATTERN_LSID_LIVE_MASTER_PLAYLIST = re.compile(r"^[a-fA-F0-9]{38}$")
    PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST = re.compile(r"^[a-fA-F0-9]{32}$")

    @staticmethod
    def combination(array_a: List[List[A]], array_b: List[List[B]]) -> List[List[Union[A, B]]]:
        return [cast("List[Union[A, B]]", a + b) for b in array_b for a in array_a]

    @staticmethod
    def concat(*args: List[str]) -> List[List[str]]:
        logger = getLogger(__name__)
        logger.debug(args)
        transposed_args = [np.array([array]).transpose() for array in args]
        logger.debug(transposed_args)
        return cast("List[List[str]]", np.concatenate(transposed_args, axis=1).tolist())


class ParameterList:
    @classmethod
    def to_list(cls) -> List[Any]:
        return [cls.__dict__[station.replace("-", "_")] for station in InstanceResource.LIST_STATION]


class ParameterExpectedLivePlaylistCreateUrlString(ParameterList):
    """To use for parametrized test."""

    BAYFM78 = "https://c-radiko.smartstream.ne.jp/BAYFM78/_definst_/simul-stream.stream/playlist.m3u8"
    FMJ = "https://c-radiko.smartstream.ne.jp/FMJ/_definst_/simul-stream.stream/playlist.m3u8"
    FMR = "https://c-radiko.smartstream.ne.jp/FMT/_definst_/simul-stream.stream/playlist.m3u8"
    FMT = "https://c-radiko.smartstream.ne.jp/FMT/_definst_/simul-stream.stream/playlist.m3u8"
    HOUSOU_DAIGAKU = "https://f-radiko.smartstream.ne.jp/HOUSOU-DAIGAKU/_definst_/simul-stream.stream/playlist.m3u8"
    INT = "https://c-radiko.smartstream.ne.jp/INT/_definst_/simul-stream.stream/playlist.m3u8"
    JOAK = "https://c-radiko.smartstream.ne.jp/JOAK/_definst_/simul-stream.stream/playlist.m3u8"
    JOAK_FM = "https://c-radiko.smartstream.ne.jp/JOAK-FM/_definst_/simul-stream.stream/playlist.m3u8"
    JORF = "https://c-radiko.smartstream.ne.jp/JORF/_definst_/simul-stream.stream/playlist.m3u8"
    LFR = "https://c-radiko.smartstream.ne.jp/LFR/_definst_/simul-stream.stream/playlist.m3u8"
    NACK5 = "https://c-radiko.smartstream.ne.jp/NACK5/_definst_/simul-stream.stream/playlist.m3u8"
    QRR = "https://c-radiko.smartstream.ne.jp/QRR/_definst_/simul-stream.stream/playlist.m3u8"
    RN1 = "https://f-radiko.smartstream.ne.jp/RN1/_definst_/simul-stream.stream/playlist.m3u8"
    RN2 = "https://f-radiko.smartstream.ne.jp/RN2/_definst_/simul-stream.stream/playlist.m3u8"
    TBS = "https://c-radiko.smartstream.ne.jp/TBS/_definst_/simul-stream.stream/playlist.m3u8"
    YFM = "https://c-radiko.smartstream.ne.jp/YFM/_definst_/simul-stream.stream/playlist.m3u8"


class ParameterExpectedLiveUrl(ParameterList):
    """To use for parametrized test."""

    BAYFM78 = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "c-radiko.smartstream.ne.jp",
            "/BAYFM78/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "BAYFM78",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    FMJ = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "c-radiko.smartstream.ne.jp",
            "/FMJ/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "FMJ",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    FMR = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "c-radiko.smartstream.ne.jp",
            "/FMT/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "FMR",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    FMT = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "c-radiko.smartstream.ne.jp",
            "/FMT/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "FMT",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    HOUSOU_DAIGAKU = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "f-radiko.smartstream.ne.jp",
            "/HOUSOU-DAIGAKU/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "HOUSOU-DAIGAKU",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    INT = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "c-radiko.smartstream.ne.jp",
            "/INT/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "INT",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    JOAK = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "c-radiko.smartstream.ne.jp",
            "/JOAK/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "JOAK",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    JOAK_FM = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "c-radiko.smartstream.ne.jp",
            "/JOAK-FM/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "JOAK-FM",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    JORF = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "c-radiko.smartstream.ne.jp",
            "/JORF/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "JORF",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    LFR = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "c-radiko.smartstream.ne.jp",
            "/LFR/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "LFR",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    NACK5 = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "c-radiko.smartstream.ne.jp",
            "/NACK5/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "NACK5",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    QRR = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "c-radiko.smartstream.ne.jp",
            "/QRR/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "QRR",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    RN1 = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "f-radiko.smartstream.ne.jp",
            "/RN1/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "RN1",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    RN2 = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "f-radiko.smartstream.ne.jp",
            "/RN2/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "RN2",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    TBS = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "c-radiko.smartstream.ne.jp",
            "/TBS/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "TBS",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    YFM = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "c-radiko.smartstream.ne.jp",
            "/YFM/_definst_/simul-stream.stream/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "YFM",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )


class ParameterExpectedTimeFreeUrl(ParameterList):
    """To use for parametrized test."""

    BAYFM78 = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "BAYFM78",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    FMJ = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "FMJ",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    FMR = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "FMR",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    FMT = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "FMT",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    HOUSOU_DAIGAKU = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "HOUSOU-DAIGAKU",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    INT = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "INT",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    JOAK = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "JOAK",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    JOAK_FM = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "JOAK-FM",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    JORF = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "JORF",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    LFR = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "LFR",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    NACK5 = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "NACK5",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    QRR = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "QRR",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    RN1 = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "RN1",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    RN2 = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "RN2",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    TBS = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "TBS",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
    YFM = ExpectedUrl(
        ExpectedUrlProperties(
            "https",
            "radiko.jp",
            "/v2/api/ts/playlist.m3u8",
            "",
            "",
        ),
        {
            "l": "15",
            "station_id": "YFM",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_TIME_FREE_MASTER_PLAYLIST,
        },
    )
