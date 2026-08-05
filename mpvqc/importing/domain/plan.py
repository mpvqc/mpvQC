# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .concerns import errors, session, subtitles, video

if TYPE_CHECKING:
    from mpvqc.datamodels import Comment

    from .scan import ScanResult
    from .settings import ImportFoundVideo


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
