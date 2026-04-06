# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from pathlib import Path
from typing import Final


@dataclass(frozen=True)
class Comment:
    time: int
    comment_type: str
    comment: str


@dataclass(frozen=True)
class VideoSource:
    path: Path
    from_document: bool
    from_subtitle: bool


@dataclass(frozen=True)
class SubtitleImportResult:
    subtitles: tuple[Path, ...]
    existing_videos: tuple[Path, ...]


NO_SUBTITLE_IMPORT: Final[SubtitleImportResult] = SubtitleImportResult(
    subtitles=(),
    existing_videos=(),
)


@dataclass(frozen=True)
class DocumentImportResult:
    valid_documents: tuple[Path, ...]
    invalid_documents: tuple[Path, ...]
    existing_videos: tuple[Path, ...]
    existing_subtitles: tuple[Path, ...]
    comments: tuple[Comment, ...]


NO_DOCUMENT_IMPORT: Final[DocumentImportResult] = DocumentImportResult(
    valid_documents=(),
    invalid_documents=(),
    existing_videos=(),
    existing_subtitles=(),
    comments=(),
)
