# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from mpvqc.importing.domain import SUBTITLE_WITH_VIDEO_REFERENCE_EXTENSIONS, parse_video_references

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

logger = logging.getLogger(__name__)


def find_videos_in_subtitles(subtitles: Sequence[Path]) -> tuple[Path, ...]:
    return tuple(video for subtitle in subtitles if (video := _parse_video_from(subtitle)) is not None)


def _parse_video_from(subtitle: Path) -> Path | None:
    if subtitle.suffix.lower() not in SUBTITLE_WITH_VIDEO_REFERENCE_EXTENSIONS:
        return None

    try:
        return _find_existing_video_reference(subtitle)
    except Exception:
        logger.exception("Failed to parse video path from subtitle file: %s", subtitle)
        return None


def _find_existing_video_reference(subtitle: Path) -> Path | None:
    content = subtitle.read_text(encoding="utf-8-sig")

    for reference in parse_video_references(content):
        video_path = reference if reference.is_absolute() else subtitle.parent / reference
        resolved_path = video_path.resolve()
        if resolved_path.is_file():
            return resolved_path

    return None
