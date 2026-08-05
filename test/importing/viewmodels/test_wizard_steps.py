# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pytest
from PySide6.QtCore import QObject

from mpvqc.importing.domain import (
    DocumentRejectionReason,
    ErrorsAbsent,
    ErrorsPresent,
    RejectedDocument,
    SessionMerge,
    SessionReplace,
    SessionUnresolved,
    SubtitlesLoad,
    SubtitlesSkip,
    SubtitlesUnresolved,
    VideoLoad,
    VideoSkip,
    VideoSource,
    VideoUnresolved,
)
from mpvqc.importing.enums import MpvqcImportWizardSessionMode
from mpvqc.importing.viewmodels import (
    MpvqcImportWizardErrorsStepViewModel,
    MpvqcImportWizardSessionStepViewModel,
    MpvqcImportWizardSubtitlesStepViewModel,
    MpvqcImportWizardVideoStepViewModel,
)

SessionMode = MpvqcImportWizardSessionMode.SessionMode

REJECTED = (
    RejectedDocument(Path("/work/broken.qc"), DocumentRejectionReason.INVALID),
    RejectedDocument(Path("/work/future.json"), DocumentRejectionReason.UNSUPPORTED_VERSION),
)

SESSION_UNRESOLVED = SessionUnresolved(incoming_comment_count=3)

VIDEO_A = Path("/movies/a.mp4")
VID_A_DOC = VideoSource(path=VIDEO_A, found_in_document=True)
VIDEO_UNRESOLVED = VideoUnresolved(candidates=(VID_A_DOC,))

SUB_A = Path("/work/a.en.srt")
SUBTITLES_UNRESOLVED = SubtitlesUnresolved(candidates=(SUB_A,))


@pytest.fixture
def parent(qt_app):
    # Held for the whole test: the step is parented to it, and a collected parent takes the step with it.
    return QObject()


def test_build_errors_step_only_for_present_errors(parent):
    assert MpvqcImportWizardErrorsStepViewModel.build(parent, ErrorsPresent(rejected_documents=REJECTED)) is not None
    assert MpvqcImportWizardErrorsStepViewModel.build(parent, ErrorsAbsent()) is None


@pytest.fixture
def session_step(parent):
    step = MpvqcImportWizardSessionStepViewModel.build(parent, SESSION_UNRESOLVED)
    assert step is not None
    return step


def test_build_session_step_only_for_unresolved_concern(parent):
    assert MpvqcImportWizardSessionStepViewModel.build(parent, SESSION_UNRESOLVED) is not None
    assert MpvqcImportWizardSessionStepViewModel.build(parent, SessionMerge()) is None
    assert MpvqcImportWizardSessionStepViewModel.build(parent, SessionReplace()) is None


def test_defaults_to_merge(session_step):
    assert session_step.resolved == SessionMerge()
    assert session_step.property("mode") == SessionMode.MERGE.value


def test_setting_mode_from_qml_resolves_to_the_domain_variant(session_step, make_spy):
    spy = make_spy(session_step.modeChanged)

    session_step.setProperty("mode", SessionMode.REPLACE.value)

    assert session_step.resolved == SessionReplace()
    assert spy.count() == 1
    assert spy.at(0, 0) == SessionMode.REPLACE.value


def test_setting_the_domain_variant_updates_the_qml_mode(session_step, make_spy):
    spy = make_spy(session_step.modeChanged)

    session_step.resolved = SessionReplace()

    assert session_step.property("mode") == SessionMode.REPLACE.value
    assert spy.count() == 1
    assert spy.at(0, 0) == SessionMode.REPLACE.value


def test_setting_the_same_mode_twice_stays_quiet(session_step, make_spy):
    spy = make_spy(session_step.modeChanged)

    session_step.setProperty("mode", SessionMode.MERGE.value)

    assert spy.count() == 0


def test_an_unknown_mode_leaves_the_step_untouched(session_step, make_spy):
    # Starts from Replace so a silent fall back to the Merge default cannot pass for "untouched"
    session_step.resolved = SessionReplace()
    spy = make_spy(session_step.modeChanged)

    session_step.setProperty("mode", 99)

    assert session_step.resolved == SessionReplace()
    assert spy.count() == 0


@pytest.fixture
def video_step(parent):
    step = MpvqcImportWizardVideoStepViewModel.build(parent, VIDEO_UNRESOLVED)
    assert step is not None
    return step


def test_build_video_step_only_for_unresolved_concern(parent):
    assert MpvqcImportWizardVideoStepViewModel.build(parent, VIDEO_UNRESOLVED) is not None
    assert MpvqcImportWizardVideoStepViewModel.build(parent, VideoLoad(path=VIDEO_A)) is None
    assert MpvqcImportWizardVideoStepViewModel.build(parent, VideoSkip()) is None


def test_defaults_to_the_first_candidate(video_step):
    assert video_step.resolved == VideoLoad(path=VIDEO_A)


def test_selecting_the_skip_entry_resolves_to_skip(video_step):
    skip_index = video_step.candidates.rowCount() - 1

    video_step.selectedIndex = skip_index

    assert video_step.resolved == VideoSkip()


@pytest.fixture
def subtitles_step(parent):
    step = MpvqcImportWizardSubtitlesStepViewModel.build(parent, SUBTITLES_UNRESOLVED)
    assert step is not None
    return step


def test_build_subtitles_step_only_for_unresolved_concern(parent):
    assert MpvqcImportWizardSubtitlesStepViewModel.build(parent, SUBTITLES_UNRESOLVED) is not None
    assert MpvqcImportWizardSubtitlesStepViewModel.build(parent, SubtitlesLoad(paths=(SUB_A,))) is None
    assert MpvqcImportWizardSubtitlesStepViewModel.build(parent, SubtitlesSkip()) is None


def test_defaults_to_all_checked(subtitles_step):
    assert subtitles_step.resolved == SubtitlesLoad(paths=(SUB_A,))


def test_unchecking_everything_resolves_to_skip(subtitles_step):
    subtitles_step.toggleSelectAll()

    assert subtitles_step.resolved == SubtitlesSkip()
