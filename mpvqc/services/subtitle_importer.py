# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from pathlib import Path


class SubtitleImporterService:
    @dataclass
    class SubtitleImportResult:
        subtitles: list[Path]
        existing_videos: list[Path]

    def read(self, subtitles: list[Path]) -> SubtitleImportResult:
        return self.SubtitleImportResult(
            subtitles=subtitles,
            existing_videos=[],
        )
