# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from mpvqc.datamodels import Comment, VideoSource
from mpvqc.services.importer import UnfinishedPlan
from mpvqc.services.importer.concerns import errors, session, subtitles, video
from testqml.injections import TEMP_ROOT

if TYPE_CHECKING:
    from pathlib import Path

_FIXTURE_ROOT = TEMP_ROOT / "wizard-fixtures"


def _path(name: str) -> Path:
    return _FIXTURE_ROOT / name


def video_choice() -> UnfinishedPlan:
    return UnfinishedPlan(
        comments=(),
        errors=errors.Absent(),
        session=session.Merge(),
        video=video.Unresolved(
            candidates=(
                VideoSource(path=_path("a.mp4"), explicitly_provided=True),
                VideoSource(path=_path("b.mp4"), explicitly_provided=True),
            )
        ),
        subtitles=subtitles.Skip(),
    )


def all_steps() -> UnfinishedPlan:
    return UnfinishedPlan(
        comments=(Comment(time=0, comment_type="Translation", comment="incoming"),),
        errors=errors.Unresolved(invalid_documents=(_path("broken.qc"),)),
        session=session.Unresolved(incoming_comment_count=5),
        video=video.Unresolved(
            candidates=(
                VideoSource(path=_path("a.mp4"), explicitly_provided=True),
                VideoSource(path=_path("b.mp4"), explicitly_provided=True),
            )
        ),
        subtitles=subtitles.Unresolved(candidates=(_path("track.srt"),)),
    )


def subtitles_only() -> UnfinishedPlan:
    return UnfinishedPlan(
        comments=(),
        errors=errors.Absent(),
        session=session.Merge(),
        video=video.Skip(),
        subtitles=subtitles.Unresolved(
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
        errors=errors.Unresolved(invalid_documents=(_path("broken.qc"),)),
        session=session.Merge(),
        video=video.Skip(),
        subtitles=subtitles.Skip(),
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
