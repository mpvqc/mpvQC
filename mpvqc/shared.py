# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterable
from dataclasses import dataclass
from math import ceil
from pathlib import Path
from typing import Final

from PySide6.QtCore import QUrl
from PySide6.QtGui import QFontMetricsF

MILLISECONDS_PER_SECOND: Final = 1000
SECONDS_PER_HOUR: Final = 3600

# The document format caps times at two hour digits
_MAX_SUBSECOND_TIME: Final = ((99 * SECONDS_PER_HOUR + 59 * 60 + 59) * 1000) + 999


@dataclass(frozen=True, slots=True)
class Comment:
    time: int  # milliseconds
    comment_type: str
    comment: str


def needs_long_format(seconds: float) -> bool:
    return seconds >= SECONDS_PER_HOUR


def format_time_to_string(input_seconds: float, *, long_format: bool) -> str:
    hours, remainder = divmod(input_seconds, SECONDS_PER_HOUR)
    minutes, seconds = divmod(remainder, 60)
    if long_format:
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

    return f"{int(minutes):02d}:{int(seconds):02d}"


def format_milliseconds_to_string(input_milliseconds: int, *, long_format: bool) -> str:
    seconds = input_milliseconds // MILLISECONDS_PER_SECOND
    return format_time_to_string(seconds, long_format=long_format)


def format_milliseconds_to_subsecond_string(input_milliseconds: int) -> str:
    clamped = min(input_milliseconds, _MAX_SUBSECOND_TIME)
    seconds, milliseconds = divmod(clamped, MILLISECONDS_PER_SECOND)
    hours, remainder = divmod(seconds, SECONDS_PER_HOUR)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def calculate_label_width(texts: Iterable[str], metrics: QFontMetricsF) -> int:
    return ceil(max((metrics.horizontalAdvance(text) for text in texts), default=0))


def map_url_to_path(url: QUrl) -> Path:
    return Path(url.toLocalFile()).resolve()


def map_urls_to_paths(urls: list[QUrl]) -> list[Path]:
    return [map_url_to_path(url) for url in urls]


def map_path_to_url(path: Path) -> QUrl:
    return QUrl.fromLocalFile(f"{path.resolve()}")


def map_path_to_str(path: Path) -> str:
    return f"{path.resolve()}"
