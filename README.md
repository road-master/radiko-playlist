# radiko playlist

[![Test](https://github.com/road-master/radiko-playlist/workflows/Test/badge.svg)](https://github.com/road-master/radiko-playlist/actions?query=workflow%3ATest)
[![Test Coverage](https://api.codeclimate.com/v1/badges/32788a087b5e6264eaae/test_coverage)](https://codeclimate.com/github/road-master/radiko-playlist/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/32788a087b5e6264eaae/maintainability)](https://codeclimate.com/github/road-master/radiko-playlist/maintainability)
[![Dependabot](https://flat.badgen.net/github/dependabot/road-master/radiko-playlist?icon=dependabot)](https://github.com/road-master/radiko-playlist/security/dependabot)
[![Python versions](https://img.shields.io/pypi/pyversions/radikoplaylist.svg)](https://pypi.org/project/radikoplaylist)
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Froad-master%2Fradikoplaylist)](https://twitter.com/share?text=radiko%20playlist&url=https://pypi.org/project/radikoplaylist/&hashtags=python)

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

### Record Time Free

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

[ffmpeg]: https://trac.ffmpeg.org/wiki/CompilationGuide
[ffmpeg-python]: https://pypi.org/project/ffmpeg-python/