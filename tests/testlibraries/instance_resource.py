"""Implements instance resources."""
import re
from unittest.mock import MagicMock

import numpy  # type: ignore

from tests.testlibraries.expected_url import ExpectedUrl


# pylint: disable=too-few-public-methods
class InstanceResource:
    """Implements instance resources."""

    URL_RADIKO_AUTH_1 = "https://radiko.jp/v2/api/auth1"
    URL_RADIKO_AUTH_2 = "https://radiko.jp/v2/api/auth2"
    URL_RADIKO_STREAM_PC_HTML_5 = "http://radiko.jp/v3/station/stream/pc_html5/"
    RADIKO_AUTH_TOKEN_EXAMPLE = "HrUNR0zyrGseqvlPl1-khQ"
    RADIKO_KEY_LENGTH_EXAMPLE = "16"
    RADIKO_KEY_OFFSET_EXAMPLE = "16"
    RESPONSE_HEADER_AUTH_1_EXAMPLE = {
        "X-Radiko-AUTHTOKEN": RADIKO_AUTH_TOKEN_EXAMPLE,
        "X-Radiko-KeyLength": RADIKO_KEY_LENGTH_EXAMPLE,
        "X-Radiko-KeyOffset": RADIKO_KEY_OFFSET_EXAMPLE,
    }
    RESPONSE_CONTENT_AUTH_1_EXAMPLE = (
        """
#EXTM3U
#EXT-X-VERSION:6
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=52973,CODECS="mp4a.40.5
https://rpaa.smartstream.ne.jp/medialist?session=Q3fHC9Smzp8x49j9AqicBL
"""
    ).encode("utf-8")
    RESPONSE_CONTENT_MASTER_PLAY_LIST = (
        """
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=52973,CODECS="mp4a.40.5"
https://radiko.jp/v2/api/ts/chunklist/Tt6TRp6b.m3u8
"""
    ).encode("utf-8")
    MOCK_GENERATE_UID = MagicMock(name="generate_uid", return_value="45f59aed8851994d2d5ecc8e7a946018",)
    LIST_STATUS_CODE_ERROR = [
        400,
        403,
        404,
        500,
        502,
        503,
        504,
    ]
    LIST_STATION = [
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
    HEADERS_EXAMPLE = {
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

    @classmethod
    def combination(cls, array_a, array_b):
        return [a + b for b in array_b for a in array_a]

    @classmethod
    def concat(cls, *args):
        print(args)
        transposed_args = [numpy.array([array]).transpose() for array in args]
        print(transposed_args)
        return numpy.concatenate(transposed_args, axis=1).tolist()


class ParameterList:
    @classmethod
    def to_list(cls):
        return [cls.__dict__[station.replace("-", "_")] for station in InstanceResource.LIST_STATION]


class ParameterExpectedPlaylistCreateUrlString(ParameterList):
    """To use for parametrized test."""

    BAYFM78 = "https://c-tf-rpaa.smartstream.ne.jp/tf/playlist.m3u8"
    FMJ = "https://c-tf-rpaa.smartstream.ne.jp/tf/playlist.m3u8"
    FMR = "https://c-tf-rpaa.smartstream.ne.jp/tf/playlist.m3u8"
    FMT = "https://c-tf-rpaa.smartstream.ne.jp/tf/playlist.m3u8"
    HOUSOU_DAIGAKU = "https://radiko.jp/v2/api/ts/playlist.m3u8"
    INT = "https://c-tf-rpaa.smartstream.ne.jp/tf/playlist.m3u8"
    JOAK = "https://radiko.jp/v2/api/ts/playlist.m3u8"
    JOAK_FM = "https://radiko.jp/v2/api/ts/playlist.m3u8"
    JORF = "https://c-tf-rpaa.smartstream.ne.jp/tf/playlist.m3u8"
    LFR = "https://c-tf-rpaa.smartstream.ne.jp/tf/playlist.m3u8"
    NACK5 = "https://c-tf-rpaa.smartstream.ne.jp/tf/playlist.m3u8"
    QRR = "https://c-tf-rpaa.smartstream.ne.jp/tf/playlist.m3u8"
    RN1 = "https://radiko.jp/v2/api/ts/playlist.m3u8"
    RN2 = "https://tf-rpaa.smartstream.ne.jp/tf/playlist.m3u8"
    TBS = "https://c-tf-rpaa.smartstream.ne.jp/tf/playlist.m3u8"
    YFM = "https://c-tf-rpaa.smartstream.ne.jp/tf/playlist.m3u8"


class ParameterExpectedUrl(ParameterList):
    """To use for parametrized test."""

    BAYFM78 = ExpectedUrl(
        "https",
        "c-rpaa.smartstream.ne.jp",
        "/so/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "BAYFM78", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
    FMJ = ExpectedUrl(
        "https",
        "c-rpaa.smartstream.ne.jp",
        "/so/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "FMJ", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
    FMR = ExpectedUrl(
        "https",
        "c-rpaa.smartstream.ne.jp",
        "/so/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "FMR", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
    FMT = ExpectedUrl(
        "https",
        "c-rpaa.smartstream.ne.jp",
        "/so/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "FMT", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
    HOUSOU_DAIGAKU = ExpectedUrl(
        "http",
        "f-radiko.smartstream.ne.jp",
        "/HOUSOU-DAIGAKU/_definst_/simul-stream.stream/playlist.m3u8",
        "",
        "",
        {
            "l": "15",
            "station_id": "HOUSOU-DAIGAKU",
            "type": "b",
            "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST,
        },
    )
    INT = ExpectedUrl(
        "https",
        "c-rpaa.smartstream.ne.jp",
        "/so/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "INT", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
    JOAK = ExpectedUrl(
        "http",
        "c-radiko.smartstream.ne.jp",
        "/JOAK/_definst_/simul-stream.stream/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "JOAK", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
    JOAK_FM = ExpectedUrl(
        "http",
        "c-radiko.smartstream.ne.jp",
        "/JOAK-FM/_definst_/simul-stream.stream/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "JOAK-FM", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
    JORF = ExpectedUrl(
        "https",
        "c-rpaa.smartstream.ne.jp",
        "/so/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "JORF", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
    LFR = ExpectedUrl(
        "https",
        "c-rpaa.smartstream.ne.jp",
        "/so/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "LFR", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
    NACK5 = ExpectedUrl(
        "https",
        "c-rpaa.smartstream.ne.jp",
        "/so/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "NACK5", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
    QRR = ExpectedUrl(
        "https",
        "c-rpaa.smartstream.ne.jp",
        "/so/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "QRR", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
    RN1 = ExpectedUrl(
        "http",
        "f-radiko.smartstream.ne.jp",
        "/RN1/_definst_/simul-stream.stream/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "RN1", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
    RN2 = ExpectedUrl(
        "https",
        "rpaa.smartstream.ne.jp",
        "/so/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "RN2", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
    TBS = ExpectedUrl(
        "https",
        "c-rpaa.smartstream.ne.jp",
        "/so/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "TBS", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
    YFM = ExpectedUrl(
        "https",
        "c-rpaa.smartstream.ne.jp",
        "/so/playlist.m3u8",
        "",
        "",
        {"l": "15", "station_id": "YFM", "type": "b", "lsid": InstanceResource.PATTERN_LSID_LIVE_MASTER_PLAYLIST},
    )
