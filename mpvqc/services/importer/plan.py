# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .concerns import errors, session, subtitles, video
from .scanner import scan

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from pathlib import Path

    from mpvqc.datamodels import Comment
    from mpvqc.enums import ImportFoundVideo

    from .scanner import ScanResult


@dataclass(frozen=True)
class FinishedPlan:
    comments: tuple[Comment, ...]
    session: session.Resolved
    video: video.Resolved
    subtitles: subtitles.Resolved


@dataclass(frozen=True)
class UnfinishedPlan:
    comments: tuple[Comment, ...]
    session: session.Concern
    video: video.Concern
    subtitles: subtitles.Concern
    errors: errors.Concern


def plan_import(
    document_paths: list[Path],
    video_paths: list[Path],
    subtitle_paths: list[Path],
    *,
    found_video_setting: ImportFoundVideo,
    has_existing_comments: bool,
    is_any_candidate_loaded: Callable[[Iterable[Path]], bool],
) -> FinishedPlan | UnfinishedPlan:
    scan_result = scan(document_paths, video_paths, subtitle_paths)
    return make_plan(
        scan_result,
        found_video_setting=found_video_setting,
        has_existing_comments=has_existing_comments,
        any_candidate_loaded=is_any_candidate_loaded(v.path for v in scan_result.videos),
    )


def make_plan(
    scan_result: ScanResult,
    *,
    found_video_setting: ImportFoundVideo,
    has_existing_comments: bool,
    any_candidate_loaded: bool,
) -> FinishedPlan | UnfinishedPlan:
    errors_outcome = errors.resolve(scan_result)
    session_outcome = session.resolve(scan_result, has_existing_comments=has_existing_comments)
    video_outcome = video.resolve(scan_result, setting=found_video_setting, any_candidate_loaded=any_candidate_loaded)
    subtitles_outcome = subtitles.resolve(scan_result, video_concern=video_outcome)

    match (errors_outcome, session_outcome, video_outcome, subtitles_outcome):
        case (
            errors.Absent(),
            session.Merge() as s,
            video.Load() | video.Skip() as v,
            subtitles.Load() | subtitles.Skip() as sub,
        ):
            return FinishedPlan(comments=scan_result.comments, session=s, video=v, subtitles=sub)
        case _:
            return UnfinishedPlan(
                comments=scan_result.comments,
                session=session_outcome,
                video=video_outcome,
                subtitles=subtitles_outcome,
                errors=errors_outcome,
            )
