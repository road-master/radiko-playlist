"""Implements getting process URL to create playlist."""
from typing import cast, Mapping, Union

from defusedxml import ElementTree

from radikoplaylist.requester import Requester


class PlaylistCreateUrlGetter:
    """Implements getting process URL to create playlist."""

    @staticmethod
    def get(station_id: str, headers: Mapping[str, Union[str, bytes]], is_time_free: bool) -> str:
        url = "http://radiko.jp/v3/station/stream/pc_html5/" + station_id + ".xml"
        response = Requester.get(url, headers)
        return PlaylistCreateUrlGetter.get_playlist_create_url(response.text, is_time_free)

    @staticmethod
    def get_playlist_create_url(string_xml: str, is_time_free: bool) -> str:
        """Parses XML and extract target URL to create playlist."""
        root = ElementTree.fromstring(string_xml, forbid_dtd=True)
        list_url = root.findall(".//url[@areafree='1']")
        list_filtered_url = [url for url in list_url if url.attrib["timefree"] == str(int(is_time_free))]
        url = list_filtered_url[0]
        element = url.find("./playlist_create_url")
        return cast(str, element.text)
