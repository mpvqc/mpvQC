# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, assert_never

from mpvqc.enums import ImportFoundVideo

if TYPE_CHECKING:
    from pathlib import Path

    from mpvqc.datamodels import VideoSource
    from mpvqc.services.importer.scanner import ScanResult


@dataclass(frozen=True)
class Load:
    path: Path


@dataclass(frozen=True)
class Skip:
    pass


@dataclass(frozen=True)
class Unresolved:
    candidates: tuple[VideoSource, ...]


type Resolved = Load | Skip
type Concern = Resolved | Unresolved


def resolve(
    scan: ScanResult,
    *,
    setting: ImportFoundVideo,
    any_candidate_loaded: bool,
) -> Concern:
    explicit = tuple(v for v in scan.videos if v.explicitly_provided)
    if explicit:
        return _from_explicit(explicit)
    return _from_scan(scan.videos, setting=setting, already_loaded=any_candidate_loaded)


def _from_explicit(candidates: tuple[VideoSource, ...]) -> Concern:
    if len(candidates) == 1:
        return Load(path=candidates[0].path)
    return Unresolved(candidates=candidates)


def _from_scan(
    candidates: tuple[VideoSource, ...],
    *,
    setting: ImportFoundVideo,
    already_loaded: bool,
) -> Concern:
    if not candidates:
        return Skip()
    if len(candidates) > 1:
        return Unresolved(candidates=candidates)
    if already_loaded:
        return Skip()

    (only,) = candidates
    match setting:
        case ImportFoundVideo.ALWAYS:
            return Load(path=only.path)
        case ImportFoundVideo.ASK_EVERY_TIME:
            return Unresolved(candidates=candidates)
        case ImportFoundVideo.NEVER:
            return Skip()
        case _:
            assert_never(setting)
