# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, assert_never

from .errors import ErrorsAbsent, resolve_errors
from .session import SessionMerge, SessionReplace, SessionUnresolved, resolve_session
from .subtitles import SubtitlesLoad, SubtitlesSkip, SubtitlesUnresolved, resolve_subtitles
from .video import VideoLoad, VideoSkip, VideoUnresolved, resolve_video

if TYPE_CHECKING:
    from mpvqc.datamodels import Comment

    from .errors import ImportErrors
    from .scan import ScanResult
    from .session import SessionConcern, SessionResolved
    from .subtitles import SubtitlesConcern, SubtitlesResolved
    from .video import LoadFoundVideo, VideoConcern, VideoResolved


@dataclass(frozen=True)
class FinishedPlan:
    comments: tuple[Comment, ...]
    session: SessionResolved
    video: VideoResolved
    subtitles: SubtitlesResolved


@dataclass(frozen=True)
class UnfinishedPlan:
    comments: tuple[Comment, ...]
    session: SessionConcern
    video: VideoConcern
    subtitles: SubtitlesConcern
    errors: ImportErrors


def make_plan(
    scan_result: ScanResult,
    *,
    found_video_setting: LoadFoundVideo,
    has_existing_comments: bool,
    any_candidate_loaded: bool,
) -> FinishedPlan | UnfinishedPlan:
    errors_outcome = resolve_errors(scan_result)
    session_outcome = resolve_session(scan_result, has_existing_comments=has_existing_comments)
    video_outcome = resolve_video(scan_result, setting=found_video_setting, any_candidate_loaded=any_candidate_loaded)
    subtitles_outcome = resolve_subtitles(scan_result, video_concern=video_outcome)

    match (errors_outcome, session_outcome, video_outcome, subtitles_outcome):
        case (
            ErrorsAbsent(),
            SessionMerge() as s,
            VideoLoad() | VideoSkip() as v,
            SubtitlesLoad() | SubtitlesSkip() as sub,
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


def finish_plan(
    plan: UnfinishedPlan,
    *,
    session: SessionResolved | None = None,
    video: VideoResolved | None = None,
    subtitles: SubtitlesResolved | None = None,
) -> FinishedPlan:
    return FinishedPlan(
        comments=plan.comments,
        session=_finish_session(plan.session, session),
        video=_finish_video(plan.video, video),
        subtitles=_finish_subtitles(plan.subtitles, subtitles),
    )


def _finish_session(concern: SessionConcern, answer: SessionResolved | None) -> SessionResolved:
    match concern:
        case SessionMerge() | SessionReplace():
            return concern
        case SessionUnresolved():
            return _require_answer(answer)
        case _:
            assert_never(concern)


def _finish_video(concern: VideoConcern, answer: VideoResolved | None) -> VideoResolved:
    match concern:
        case VideoLoad() | VideoSkip():
            return concern
        case VideoUnresolved():
            return _require_answer(answer)
        case _:
            assert_never(concern)


def _finish_subtitles(concern: SubtitlesConcern, answer: SubtitlesResolved | None) -> SubtitlesResolved:
    match concern:
        case SubtitlesLoad() | SubtitlesSkip():
            return concern
        case SubtitlesUnresolved():
            return _require_answer(answer)
        case _:
            assert_never(concern)


def _require_answer[T](answer: T | None) -> T:
    if answer is None:
        msg = "cannot finish a plan while a concern is unresolved"
        raise RuntimeError(msg)
    return answer
