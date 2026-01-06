# radiko playlist

[![Test](https://github.com/road-master/radiko-playlist/workflows/Test/badge.svg)](https://github.com/road-master/radiko-playlist/actions?query=workflow%3ATest)
[![CodeQL](https://github.com/road-master/radiko-playlist/workflows/CodeQL/badge.svg)](https://github.com/road-master/radiko-playlist/actions?query=workflow%3ACodeQL)
[![Code Coverage](https://qlty.sh/gh/road-master/projects/radiko-playlist/coverage.svg)](https://qlty.sh/gh/road-master/projects/radiko-playlist)
[![Maintainability](https://qlty.sh/gh/road-master/projects/radiko-playlist/maintainability.svg)](https://qlty.sh/gh/road-master/projects/radiko-playlist)
[![Dependabot](https://flat.badgen.net/github/dependabot/road-master/radiko-playlist?icon=dependabot)](https://github.com/road-master/radiko-playlist/security/dependabot)
[![Python versions](https://img.shields.io/pypi/pyversions/radikoplaylist.svg)](https://pypi.org/project/radikoplaylist)
[![X URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Froad-master%2Fradikoplaylist)](https://x.com/intent/post?text=radiko%20playlist&url=https%3A%2F%2Fpypi.org%2Fproject%2Fradikoplaylist%2F&hashtags=python)

Accesses to radiko API, gets media playlist URL and built header for HTTP request to its URL.

## Features

This is light weight library for interacting with radiko API to get information to access to media playlist.
We can find various usages by integrating with other libraries.

## Example

Following example requires additional installations:

- [ffmpeg]
- [ffmpeg-python]

### Record Live

```python
import time

import ffmpeg

from radikoplaylist import MasterPlaylistClient, LiveMasterPlaylistRequest

master_playlist_request = LiveMasterPlaylistRequest("FMT")
master_playlist = MasterPlaylistClient.get(master_playlist_request, area_id="JP13")

stream = ffmpeg.input(
    master_playlist.media_playlist_url,
    headers=master_playlist.headers,
    copytb='1'
)
stream = ffmpeg.output(stream, "./record.m4a", f='mp4', c='copy')

# @see https://github.com/kkroening/ffmpeg-python/issues/162#issuecomment-571820244
popen = stream.run_async(pipe_stdin=True)
recording_minute = 30
time.sleep(recording_minute * 60)
popen.communicate(str.encode("q"))
time.sleep(3)
popen.terminate()
```

### Record Time Free (7-Day)

```python
import ffmpeg

from radikoplaylist import MasterPlaylistClient, TimeFreeMasterPlaylistRequest

master_playlist_request = TimeFreeMasterPlaylistRequest(
    "NACK5", 20200529210000, 20200529230000
)
master_playlist = MasterPlaylistClient.get(master_playlist_request, area_id="JP13")

stream = ffmpeg.input(
    master_playlist.media_playlist_url,
    headers=master_playlist.headers,
    copytb='1'
)
stream = ffmpeg.output(stream, "./record.m4a", f='mp4', c='copy')
ffmpeg.run(stream)
```

### Record Time Free (30-Day)

For accessing programs within the past 30 days, you need a radiko premium account.
First, log in to [radiko.jp] in your browser, then get the `radiko_session` cookie value from your browser's developer tools.

```python
import ffmpeg

from radikoplaylist import MasterPlaylistClient, TimeFree30DayMasterPlaylistRequest

master_playlist_request = TimeFree30DayMasterPlaylistRequest(
    "802", 20251214220000, 20251214223000
)
master_playlist = MasterPlaylistClient.get(
    master_playlist_request,
    area_id="JP13",
    radiko_session="your_radiko_session_value_from_cookie_here"
)

stream = ffmpeg.input(
    master_playlist.media_playlist_url,
    headers=master_playlist.headers,
    copytb='1'
)
stream = ffmpeg.output(stream, "./record.m4a", f='mp4', c='copy')
ffmpeg.run(stream)
```

[ffmpeg]: https://trac.ffmpeg.org/wiki/CompilationGuide
[ffmpeg-python]: https://pypi.org/project/ffmpeg-python/
[radiko.jp]: https://radiko.jp/