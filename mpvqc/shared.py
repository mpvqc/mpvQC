# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from PySide6.QtCore import QUrl

MILLISECONDS_PER_SECOND: Final = 1000

# The document format caps times at two hour digits
_MAX_SUBSECOND_TIME: Final = ((99 * 3600 + 59 * 60 + 59) * 1000) + 999


@dataclass(frozen=True, slots=True)
class Comment:
    time: int  # milliseconds
    comment_type: str
    comment: str


def format_milliseconds_to_subsecond_string(input_milliseconds: int) -> str:
    clamped = min(input_milliseconds, _MAX_SUBSECOND_TIME)
    seconds, milliseconds = divmod(clamped, MILLISECONDS_PER_SECOND)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def map_url_to_path(url: QUrl) -> Path:
    return Path(url.toLocalFile()).resolve()


def map_urls_to_paths(urls: list[QUrl]) -> list[Path]:
    return [map_url_to_path(url) for url in urls]


def map_path_to_url(path: Path) -> QUrl:
    return QUrl.fromLocalFile(f"{path.resolve()}")


def map_path_to_str(path: Path) -> str:
    return f"{path.resolve()}"
