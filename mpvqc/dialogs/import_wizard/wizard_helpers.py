# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from mpvqc.enums import StepKind
from mpvqc.services.importer import FinishedPlan, errors, session, subtitles, video

from .steps import resolve_session, resolve_subtitles, resolve_video

if TYPE_CHECKING:
    from mpvqc.services.importer import UnfinishedPlan

    from .steps import (
        MpvqcImportWizardSessionStepViewModel,
        MpvqcImportWizardSubtitlesStepViewModel,
        MpvqcImportWizardVideoStepViewModel,
    )


def compute_steps(unfinished_plan: UnfinishedPlan) -> tuple[StepKind, ...]:
    steps: list[StepKind] = []
    if isinstance(unfinished_plan.errors, errors.Present):
        steps.append(StepKind.ERRORS)
    if isinstance(unfinished_plan.session, session.Unresolved):
        steps.append(StepKind.SESSION)
    if isinstance(unfinished_plan.video, video.Unresolved):
        steps.append(StepKind.VIDEO)
    if isinstance(unfinished_plan.subtitles, subtitles.Unresolved):
        steps.append(StepKind.SUBTITLES)
    return tuple(steps)


def has_valid_content(unfinished_plan: UnfinishedPlan) -> bool:
    return (
        bool(unfinished_plan.comments)
        or isinstance(unfinished_plan.video, video.Load)
        or isinstance(unfinished_plan.subtitles, subtitles.Load)
    )


def build_finished_plan(
    unfinished_plan: UnfinishedPlan,
    session_step: MpvqcImportWizardSessionStepViewModel | None,
    video_step: MpvqcImportWizardVideoStepViewModel | None,
    subtitles_step: MpvqcImportWizardSubtitlesStepViewModel | None,
) -> FinishedPlan:
    return FinishedPlan(
        comments=unfinished_plan.comments,
        session=resolve_session(session_step, unfinished_plan.session),
        video=resolve_video(video_step, unfinished_plan.video),
        subtitles=resolve_subtitles(subtitles_step, unfinished_plan.subtitles),
    )
