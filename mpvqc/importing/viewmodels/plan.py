# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from mpvqc.importing.domain import FinishedPlan

from .steps import resolve_session, resolve_subtitles, resolve_video

if TYPE_CHECKING:
    from mpvqc.importing.domain import UnfinishedPlan

    from .steps import (
        MpvqcImportWizardSessionStepViewModel,
        MpvqcImportWizardSubtitlesStepViewModel,
        MpvqcImportWizardVideoStepViewModel,
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
