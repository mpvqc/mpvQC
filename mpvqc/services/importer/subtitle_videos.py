# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


def find_videos_in_subtitles(subtitles: Sequence[Path]) -> tuple[Path, ...]:
    return tuple(video for subtitle in subtitles if (video := _parse_video_from(subtitle)) is not None)


def _parse_video_from(subtitle: Path) -> Path | None:
    try:
        match subtitle.suffix.lower():
            case ".ass" | ".ssa":
                return _parse_video_in_ass_ssa(subtitle)
    except Exception:
        logger.exception("Failed to parse video path from subtitle file: %s", subtitle)
    return None


def _parse_video_in_ass_ssa(subtitle: Path) -> Path | None:
    with subtitle.open("r", encoding="utf-8-sig") as file:
        for raw_line in file:
            line = raw_line.strip()

            if not line.startswith("Video File:"):
                continue

            video_path_str = line.split(":", 1)[1].strip()
            if not video_path_str:
                continue

            video_path = Path(video_path_str)
            if not video_path.is_absolute():
                video_path = subtitle.parent / video_path

            resolved_path = video_path.resolve()
            if resolved_path.is_file():
                return resolved_path

        return None
