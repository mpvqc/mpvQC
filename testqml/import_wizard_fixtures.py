# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from mpvqc.importing.domain import (
    DocumentRejectionReason,
    ErrorsAbsent,
    ErrorsPresent,
    RejectedDocument,
    SessionMerge,
    SessionUnresolved,
    SubtitlesSkip,
    SubtitlesUnresolved,
    UnfinishedPlan,
    VideoSkip,
    VideoSource,
    VideoUnresolved,
)
from mpvqc.shared import Comment
from testqml.injections import TEMP_ROOT

if TYPE_CHECKING:
    from pathlib import Path

_FIXTURE_ROOT = TEMP_ROOT / "wizard-fixtures"


def _path(name: str) -> Path:
    return _FIXTURE_ROOT / name


def video_choice() -> UnfinishedPlan:
    return UnfinishedPlan(
        comments=(),
        errors=ErrorsAbsent(),
        session=SessionMerge(),
        video=VideoUnresolved(
            candidates=(
                VideoSource(path=_path("a.mp4"), explicitly_provided=True),
                VideoSource(path=_path("b.mp4"), explicitly_provided=True),
            )
        ),
        subtitles=SubtitlesSkip(),
    )


def all_steps() -> UnfinishedPlan:
    return UnfinishedPlan(
        comments=(Comment(time=0, comment_type="Translation", comment="incoming"),),
        errors=ErrorsPresent(
            rejected_documents=(RejectedDocument(_path("broken.qc"), DocumentRejectionReason.INVALID),)
        ),
        session=SessionUnresolved(incoming_comment_count=5),
        video=VideoUnresolved(
            candidates=(
                VideoSource(path=_path("a.mp4"), explicitly_provided=True),
                VideoSource(path=_path("b.mp4"), explicitly_provided=True),
            )
        ),
        subtitles=SubtitlesUnresolved(candidates=(_path("track.srt"),)),
    )


def subtitles_only() -> UnfinishedPlan:
    return UnfinishedPlan(
        comments=(),
        errors=ErrorsAbsent(),
        session=SessionMerge(),
        video=VideoSkip(),
        subtitles=SubtitlesUnresolved(
            candidates=(
                _path("a.srt"),
                _path("b.srt"),
                _path("c.srt"),
            )
        ),
    )


def errors_only() -> UnfinishedPlan:
    return UnfinishedPlan(
        comments=(),
        errors=ErrorsPresent(
            rejected_documents=(
                RejectedDocument(_path("broken.qc"), DocumentRejectionReason.INVALID),
                RejectedDocument(_path("future.json"), DocumentRejectionReason.UNSUPPORTED_VERSION),
            )
        ),
        session=SessionMerge(),
        video=VideoSkip(),
        subtitles=SubtitlesSkip(),
    )


SCENARIOS = {
    "video-choice": video_choice,
    "all-steps": all_steps,
    "subtitles-only": subtitles_only,
    "errors-only": errors_only,
}


def build(scenario: str) -> UnfinishedPlan:
    factory = SCENARIOS.get(scenario)
    if factory is None:
        msg = f"Unknown wizard test scenario: {scenario}"
        raise ValueError(msg)
    return factory()
