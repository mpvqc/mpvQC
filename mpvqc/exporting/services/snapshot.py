# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

    from mpvqc.shared import Comment


@dataclass(frozen=True)
class ExportSnapshot:
    captured_at: datetime
    write_header_date: bool
    write_header_generator: bool
    write_header_nickname: bool
    write_header_video_path: bool
    write_header_subtitles: bool
    nickname: str | None
    video_path: str | None
    external_subtitles: tuple[str, ...]
    generator: str
    comments: tuple[Comment, ...]
