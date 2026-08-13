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
    videos = []

    for subtitle in subtitles:
        video = _parse_video_from(subtitle)
        if video is not None:
            videos.append(video)

    return tuple(videos)


def _parse_video_from(subtitle: Path) -> Path | None:
    try:
        references = _parse_video_references(subtitle)
        return _first_existing_video(subtitle, references)
    except Exception:
        logger.exception("Failed to parse video path from subtitle file: %s", subtitle)
        return None


def _parse_video_references(subtitle: Path) -> tuple[Path, ...]:
    match subtitle.suffix.lower():
        case ".ass" | ".ssa":
            return parse_ass_video_references(subtitle.read_text(encoding="utf-8-sig"))
        case _:
            return ()


def _first_existing_video(subtitle: Path, references: tuple[Path, ...]) -> Path | None:
    for reference in references:
        video_path = reference if reference.is_absolute() else subtitle.parent / reference
        resolved_path = video_path.resolve()
        if resolved_path.is_file():
            return resolved_path

    return None


def parse_ass_video_references(content: str) -> tuple[Path, ...]:
    references = []

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line.startswith("Video File:"):
            continue

        video_path = line.split(":", 1)[1].strip()
        if video_path:
            references.append(Path(video_path))

    return tuple(references)
