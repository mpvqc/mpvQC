# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from PySide6.QtCore import QObject

from mpvqc.importing.domain import (
    SessionMerge,
    SessionReplace,
    SubtitlesLoad,
    SubtitlesSkip,
    VideoLoad,
    VideoSkip,
)
from mpvqc.importing.enums import MpvqcImportWizardSessionMode
from mpvqc.importing.viewmodels import (
    MpvqcImportWizardSessionStepViewModel,
    MpvqcImportWizardSubtitlesStepViewModel,
    MpvqcImportWizardVideoStepViewModel,
)
from test.importing.plans import (
    SUB_A,
    UNRESOLVED_SESSION,
    UNRESOLVED_SUBTITLES,
    UNRESOLVED_VIDEO,
    VIDEO_A,
)

SessionMode = MpvqcImportWizardSessionMode.SessionMode


@pytest.fixture
def parent(qt_app):
    # Held for the whole test: the step is parented to it, and a collected parent takes the step with it.
    return QObject()


@pytest.fixture
def session_step(parent):
    return MpvqcImportWizardSessionStepViewModel(parent, UNRESOLVED_SESSION)


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
    return MpvqcImportWizardVideoStepViewModel(parent, UNRESOLVED_VIDEO)


def test_defaults_to_the_first_candidate(video_step):
    assert video_step.resolved == VideoLoad(path=VIDEO_A)


def test_selecting_the_skip_entry_resolves_to_skip(video_step):
    skip_index = video_step.candidates.rowCount() - 1

    video_step.selectedIndex = skip_index

    assert video_step.resolved == VideoSkip()


@pytest.fixture
def subtitles_step(parent):
    return MpvqcImportWizardSubtitlesStepViewModel(parent, UNRESOLVED_SUBTITLES)


def test_defaults_to_all_checked(subtitles_step):
    assert subtitles_step.resolved == SubtitlesLoad(paths=(SUB_A,))


def test_unchecking_everything_resolves_to_skip(subtitles_step):
    subtitles_step.toggleSelectAll()

    assert subtitles_step.resolved == SubtitlesSkip()
