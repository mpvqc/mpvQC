# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from mpvqc.services.importer.concerns import video

if TYPE_CHECKING:
    from pathlib import Path

    from mpvqc.datamodels import SubtitleSource
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
    return _from_scan(scan.subtitles, video_concern)


def _from_explicit(candidates: tuple[SubtitleSource, ...]) -> Concern:
    return Load(paths=tuple(c.path for c in candidates))


def _from_scan(candidates: tuple[SubtitleSource, ...], video_concern: video.Concern) -> Concern:
    if isinstance(video_concern, video.Unresolved) and candidates:
        return Unresolved(candidates=tuple(c.path for c in candidates))
    if isinstance(video_concern, video.Skip) or not candidates:
        return Skip()
    return Load(paths=tuple(c.path for c in candidates))
