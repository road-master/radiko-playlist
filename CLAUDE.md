# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **radikoplaylist**, a lightweight Python library for interacting with the radiko API (Japanese internet radio service). The library retrieves media playlist URLs and builds HTTP headers required to access radiko's HLS streams for both live radio and time-free (recorded) content.

The library handles radiko's authentication flow and filters available streaming URLs to ensure compatibility with FFmpeg.

## Development Commands

### Package Management
This project uses `uv` for dependency management. All commands should be run with `uv run` prefix.

### Testing
```bash
# Run fast tests (excludes @pytest.mark.slow tests)
uv run invoke test

# Run all tests including slow ones
uv run invoke test.all

# Run with coverage report
uv run invoke test.coverage

# Run a single test file
uv run pytest tests/test_master_playlist_client.py

# Run a specific test
uv run pytest tests/test_master_playlist_client.py::test_name
```

### Linting
```bash
# Fast linting (xenon, ruff, bandit, dodgy, flake8, pydocstyle)
uv run invoke lint

# Deep linting (mypy, pylint, semgrep) - slower but more thorough
uv run invoke lint.deep

# Individual linters
uv run invoke lint.mypy
uv run invoke lint.pylint
uv run invoke lint.ruff
uv run invoke lint.flake8
uv run invoke lint.bandit
```

### Code Formatting
```bash
# Format code with docformatter, isort, autoflake, and black
uv run invoke style
```

### Building
```bash
# Build source and wheel packages
uv run invoke dist
```

### Cleanup
```bash
# Clean all artifacts
uv run invoke clean

# Clean specific artifacts
uv run invoke clean.python
uv run invoke clean.tests
uv run invoke clean.dist
```

## Architecture

### Request Flow

The library follows a multi-step authentication and URL retrieval flow:

1. **Authorization** ([authorization.py](radikoplaylist/authorization.py))
   - Performs two-stage auth with radiko API (auth1 → auth2)
   - Extracts auth token and creates partial key from radiko's auth key
   - Returns headers containing `X-Radiko-AuthToken`, `X-Radiko-Partialkey`, and `X-Radiko-AreaId`

2. **Playlist Create URL Discovery** ([playlist_create_url_getter.py](radikoplaylist/playlist_create_url_getter.py))
   - Fetches station XML metadata from `https://radiko.jp/v3/station/stream/pc_html5/{station_id}.xml`
   - Parses XML to find `playlist_create_url` elements
   - Filters URLs based on:
     - Area-free availability (`areafree='1'`)
     - Time-free mode (`timefree` attribute: "0" for live, "1" for time-free)
     - FFmpeg compatibility (excludes certain CDN hosts that FFmpeg can't handle)
   - For time-free: prioritizes `radiko.jp` hosts (fastest) via exception-based control flow
   - Three implementations: `LivePlaylistCreateUrlGetter`, `TimeFreePlaylistCreateUrlGetter`, and `TimeFree30DayPlaylistCreateUrlGetter`
   - Note: Both 7-day and 30-day timefree use the same XML filtering (`timefree='1'`); the distinction is in the query parameter (`type=b` vs `type=c`)

3. **Master Playlist Retrieval** ([master_playlist_client.py](radikoplaylist/master_playlist_client.py))
   - Builds request URL using `MasterPlaylistRequest` subclasses
   - Requests the playlist and parses m3u8 format
   - Returns `MasterPlaylist` object containing media playlist URL and auth headers

### Request Models

Three request types inherit from `MasterPlaylistRequest` ([master_playlist_request.py](radikoplaylist/master_playlist_request.py)):

- **LiveMasterPlaylistRequest**: For live radio streams
  - Query params: `station_id`, `l=15`, `lsid` (fixed UID), `type=b`

- **TimeFreeMasterPlaylistRequest**: For recorded content (7-day window)
  - Requires `start_at` and `end_at` timestamps (format: `YYYYMMDDHHmmss` as integer)
  - Generates MD5-based UID from random value + JST timestamp
  - Query params include: `station_id`, `start_at`, `ft`, `end_at`, `to`, `l=15`, `lsid`, `type=b`
  - Available for programs within the past 7 days

- **TimeFree30DayMasterPlaylistRequest**: For recorded content (30-day window)
  - Same signature as `TimeFreeMasterPlaylistRequest` (`station_id`, `start_at`, `end_at`)
  - Uses `type=c` instead of `type=b` to signal 30-day access
  - Available for programs within the past 30 days (may require premium radiko account)
  - Uses same XML endpoints and URL filtering as 7-day variant
  - The distinction between 7-day and 30-day is made solely via the `type` query parameter

### Public API

The main entry point is `MasterPlaylistClient.get()` which:
- Takes a `MasterPlaylistRequest` (Live, TimeFree, or TimeFree30Day variant)
- Optionally takes `area_id` (defaults to "JP13" for Tokyo)
- Optionally takes `radiko_session` (required for 30-day timefree with premium accounts)
- Returns a `MasterPlaylist` object with:
  - `media_playlist_url`: The HLS playlist URL to pass to FFmpeg
  - `headers`: The authenticated headers dictionary

#### Premium Account Authentication (30-Day Timefree)

For 30-day timefree access, you need a radiko premium account session cookie:

1. Log in to radiko.jp in your browser with your premium account
2. Get the `radiko_session` cookie value from your browser's developer tools
3. Pass it to `MasterPlaylistClient.get()`:

```python
from radikoplaylist.master_playlist_request import TimeFree30DayMasterPlaylistRequest
from radikoplaylist.master_playlist_client import MasterPlaylistClient

request = TimeFree30DayMasterPlaylistRequest(
    station_id="JOAK",
    start_at=20200518215700,
    end_at=20200518220000
)

# Pass your radiko premium session cookie
playlist = MasterPlaylistClient.get(
    request,
    area_id="JP13",
    radiko_session="your_radiko_session_cookie_value_here"
)
```

Without the `radiko_session` parameter, the library uses the standard free account authentication which only supports 7-day timefree access.

**Note:** The library performs the standard auth1/auth2 flow regardless of whether a cookie is provided. The `radiko_session` cookie is added to the headers in addition to the standard authentication tokens, which enables access to premium features like 30-day timefree.

### URL Filtering Logic

The library contains complex URL filtering to work around FFmpeg compatibility issues:

- **Unsupported hosts** (defined in `UrlChecker`): `c-rpaa.smartstream.ne.jp`, `si-c-radiko.smartstream.ne.jp`, `si-f-radiko.smartstream.ne.jp`
- **Time-free specific unsupported**: `tf-c-rpaa-radiko.smartstream.ne.jp`, `tf-f-rpaa-radiko.smartstream.ne.jp`, `rpaa.smartstream.ne.jp`
- **Preferred host** for time-free: `radiko.jp` (detected via `is_fastest_host_to_download()` and returned immediately using exception-based control flow)

## Code Quality Standards

This project enforces strict code quality:

- **Type checking**: mypy with `strict = true`
- **Line length**: 119 characters (Black, flake8, pylint, ruff)
- **Import sorting**: isort with trailing commas and grid wrapping
- **Security**: bandit, semgrep, dlint
- **Complexity**: radon, xenon, cohesion
- **Style**: Black, pydocstyle (Google convention), hacking, pylint
- **Docstrings**: Minimum length 7 characters; Google style markers added to pydocstyle

## Important Implementation Notes

### Security Considerations
- Uses `defusedxml` for XML parsing to prevent XXE attacks
- MD5 is used in time-free UID generation because radiko.jp's JavaScript still uses MD5 (see `master_playlist_request.py:94`)
- The `_RADIKO_AUTH_KEY` is a public constant defined in radiko's client-side JavaScript

### Testing
- Tests use `requests-mock` to mock HTTP requests and prevent slow tests
- Test resources are in `tests/testresources/`
- Uses `pytest-resource-path` for accessing test resources

### Type Hints
- All code is fully type-hinted (enforced by mypy strict mode)
- `m3u8` library lacks type stubs, so it's ignored in mypy config
- The package includes `py.typed` marker for PEP 561 compliance
