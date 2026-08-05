# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pytest
from PySide6.QtCore import QObject

from mpvqc.importing.domain import SubtitlesLoad, SubtitlesSkip, SubtitlesUnresolved
from mpvqc.importing.viewmodels import build_subtitles_step

SUB_A = Path("/work/a.en.srt")

UNRESOLVED = SubtitlesUnresolved(candidates=(SUB_A,))


@pytest.fixture
def parent(qt_app):
    # Held for the whole test: the step is parented to it, and a collected parent takes the step with it.
    return QObject()


@pytest.fixture
def step(parent):
    step = build_subtitles_step(parent, UNRESOLVED)
    assert step is not None
    return step


def test_build_subtitles_step_only_for_unresolved_concern(parent):
    assert build_subtitles_step(parent, UNRESOLVED) is not None
    assert build_subtitles_step(parent, SubtitlesLoad(paths=(SUB_A,))) is None
    assert build_subtitles_step(parent, SubtitlesSkip()) is None


def test_defaults_to_all_checked(step):
    assert step.resolved == SubtitlesLoad(paths=(SUB_A,))


def test_unchecking_everything_resolves_to_skip(step):
    step.toggleSelectAll()

    assert step.resolved == SubtitlesSkip()
