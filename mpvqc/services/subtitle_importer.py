# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from pathlib import Path

from loguru import logger


class SubtitleImporterService:
    @dataclass
    class SubtitleImportResult:
        subtitles: list[Path]
        existing_videos: list[Path]

    def read(self, subtitles: list[Path]) -> SubtitleImportResult:
        existing_videos = []

        for subtitle in subtitles:
            if video := parse_video_from(subtitle):
                existing_videos.append(video)  # noqa: PERF401

        return self.SubtitleImportResult(
            subtitles=subtitles,
            existing_videos=existing_videos,
        )


def parse_video_from(subtitle: Path) -> Path | None:
    try:
        match subtitle.suffix.lower():
            case ".ass" | ".ssa":
                return parse_video_in_ass_ssa(subtitle)
    except Exception:
        logger.exception("Failed to parse video path from subtitle file: {}", subtitle)
    return None


def parse_video_in_ass_ssa(subtitle: Path) -> Path | None:
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
