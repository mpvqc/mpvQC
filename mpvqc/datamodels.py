# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Comment:
    time: int
    comment_type: str
    comment: str


@dataclass(frozen=True)
class VideoSource:
    path: Path
    explicitly_provided: bool = False
    found_in_document: bool = False
    found_in_subtitle: bool = False


@dataclass(frozen=True)
class SubtitleSource:
    path: Path
    explicitly_provided: bool = False
    found_in_document: bool = False


@dataclass(frozen=True)
class SubtitleImportResult:
    subtitles: tuple[Path, ...]
    existing_videos: tuple[Path, ...]


@dataclass(frozen=True)
class DocumentImportResult:
    valid_documents: tuple[Path, ...]
    invalid_documents: tuple[Path, ...]
    existing_videos: tuple[Path, ...]
    existing_subtitles: tuple[Path, ...]
    comments: tuple[Comment, ...]
