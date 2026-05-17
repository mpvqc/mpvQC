# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from mpvqc.services.importer.concerns import video

if TYPE_CHECKING:
    from pathlib import Path

    from mpvqc.datamodels import SubtitleSource, VideoSource
    from mpvqc.services.importer.scanner import ScanResult


@dataclass(frozen=True)
class Load:
    paths: tuple[Path, ...]


@dataclass(frozen=True)
class Skip:
    pass


@dataclass(frozen=True)
class Unresolved:
    candidates: tuple[Path, ...]


Resolved = Load | Skip
Concern = Resolved | Unresolved


def resolve(scan: ScanResult, video_concern: video.Concern) -> Concern:
    explicit = tuple(s for s in scan.subtitles if s.explicitly_provided)
    if explicit:
        return _from_explicit(explicit)
    return _from_scan(scan, video_concern)


def _from_explicit(candidates: tuple[SubtitleSource, ...]) -> Concern:
    return Load(paths=tuple(c.path for c in candidates))


def _from_scan(scan: ScanResult, video_concern: video.Concern) -> Concern:
    candidates = scan.subtitles
    if isinstance(video_concern, video.Skip) or not candidates:
        return Skip()
    if isinstance(video_concern, video.Unresolved):
        return Unresolved(candidates=tuple(c.path for c in candidates))
    if _explicit_video_overrides_doc(scan.videos):
        return Unresolved(candidates=tuple(c.path for c in candidates))
    return Load(paths=tuple(c.path for c in candidates))


def _explicit_video_overrides_doc(videos: tuple[VideoSource, ...]) -> bool:
    explicit_paths = {v.path for v in videos if v.explicitly_provided}
    if not explicit_paths:
        return False
    doc_paths = {v.path for v in videos if v.found_in_document}
    return explicit_paths.isdisjoint(doc_paths)
