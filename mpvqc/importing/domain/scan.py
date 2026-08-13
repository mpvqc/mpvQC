# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from mpvqc.shared import Comment


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


class DocumentRejectionReason(Enum):
    INVALID = auto()
    UNSUPPORTED_VERSION = auto()


@dataclass(frozen=True)
class RejectedDocument:
    path: Path
    reason: DocumentRejectionReason


@dataclass(frozen=True)
class ScanResult:
    videos: tuple[VideoSource, ...]
    subtitles: tuple[SubtitleSource, ...]
    comments: tuple[Comment, ...]
    rejected_documents: tuple[RejectedDocument, ...]
