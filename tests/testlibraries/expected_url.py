"""Implements model of expected URL."""
from typing import Dict, Pattern, Union
from urllib.parse import parse_qs, ParseResult


class ExpectedUrl:
    """Model of expected URL."""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        scheme: str,
        netloc: str,
        path: str,
        params: str,
        fragment: str,
        query: Dict[str, Union[str, Pattern[str]]],
    ) -> None:
        self.scheme = scheme
        self.netloc = netloc
        self.path = path
        self.params = params
        self.fragment = fragment
        self.query = query

    def check(self, parse_result_url: ParseResult) -> None:
        """Checks."""
        list_actual = [
            parse_result_url.scheme,
            parse_result_url.netloc,
            parse_result_url.path,
            parse_result_url.params,
            parse_result_url.fragment,
        ]
        list_expected = [
            self.scheme,
            self.netloc,
            self.path,
            self.params,
            self.fragment,
        ]
        for actual, expected in zip(list_actual, list_expected):
            assert actual == expected, "actual = " + actual + ", expected = " + expected
        self.check_url_query(parse_result_url.query)

    def check_url_query(self, query: str) -> None:
        """Checks URL query."""
        parsed_result_query = parse_qs(query)
        for key, expected in self.query.items():
            actual = parsed_result_query[key][0]
            if not isinstance(expected, str):
                assert expected.match(actual), "actual = " + actual + ", expected = " + expected.pattern
            else:
                assert actual == expected, "actual = " + actual + ", expected = " + expected
