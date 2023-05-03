from __future__ import annotations

import inspect
import logging
from dataclasses import asdict
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

import yt_dlp as youtube_dl

from . import tempdir


_logger = logging.getLogger(__name__)


class YDLLogger:
    def debug(self, msg: str) -> None:
        _logger.debug(msg)

    def warning(self, msg: str) -> None:
        _logger.warning(msg)

    def error(self, msg: str) -> None:
        _logger.warning(msg)


def progress_hook(d):
    if d["status"] == "finished":
        _logger.debug("Done downloading, now converting...")


@dataclass
class YoutubeVideoData:
    fulltitle: str
    channel: str
    channel_id: str
    uploader_id: str
    uploader: str
    duration: int
    duration_string: str
    ext: str
    filesize_approx: int
    format: str
    format_id: str
    format_note: str
    fps: int
    height: int
    description: str = None
    upload_date: str = None
    release_date: str = None
    release_timestamp: int = None
    categories: list[str] = None
    view_count: int = None
    aspect_ratio: float = None
    audio_channels: int = None
    dynamic_range: str = None
    epoch: int = None

    def to_dict(self, compact: bool = True) -> dict[str, Any]:
        dict_repr = asdict(self)
        return (
            {k: v for k, v in dict_repr.items() if v is not None}
            if compact
            else dict_repr
        )

    @classmethod
    def from_dict(cls, **args) -> YoutubeVideoData:
        return cls(
            **{k: v for k, v in args.items() if k in inspect.signature(cls).parameters}
        )


@dataclass
class DownloadResult:
    file_id: str
    file_path: str
    video_data: YoutubeVideoData


def download_youtube(url: str) -> DownloadResult | None:
    unique_id = str(uuid4())

    options = {
        "outtmpl": f"{tempdir.name}/{unique_id}.%(ext)s",
        "logger": YDLLogger(),
        "progress_hooks": [progress_hook],
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        try:
            metadata = ydl.extract_info(url=url, download=True)
        except youtube_dl.utils.DownloadError:
            return None

        return DownloadResult(
            file_id=unique_id,
            file_path=f"{tempdir.name}/{unique_id}.{metadata['ext']}",
            video_data=YoutubeVideoData.from_dict(**metadata),
        )
