"""Implements model of expected URL."""

from dataclasses import asdict, dataclass
from typing import Dict, Iterator, Pattern, Union
from urllib.parse import parse_qs, ParseResult


@dataclass
class ExpectedUrlProperties:
    """Model of expected URL properties."""

    scheme: str
    netloc: str
    path: str
    params: str
    fragment: str

    def __iter__(self) -> Iterator[str]:
        return iter(asdict(self).values())

    def assert_parse_result_url(self, parse_result_url: ParseResult) -> None:
        """Checks."""
        list_actual = [
            parse_result_url.scheme,
            parse_result_url.netloc,
            parse_result_url.path,
            parse_result_url.params,
            parse_result_url.fragment,
        ]
        for actual, expected in zip(list_actual, self):
            assert actual == expected, "actual = " + actual + ", expected = " + expected


class ExpectedUrl:
    """Model of expected URL."""

    # Reason: ParseResult has 5 attributes
    def __init__(  # pylint: disable=too-many-arguments too-many-positional-arguments
        self,
        expected_url_properties: ExpectedUrlProperties,
        query: Dict[str, Union[str, Pattern[str]]],
    ) -> None:
        self.expected_url_properties = expected_url_properties
        self.query = query

    def check(self, parse_result_url: ParseResult) -> None:
        """Checks."""
        self.expected_url_properties.assert_parse_result_url(parse_result_url)
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
