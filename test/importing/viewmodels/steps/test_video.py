# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pytest
from PySide6.QtCore import QObject

from mpvqc.importing.domain import VideoLoad, VideoSkip, VideoSource, VideoUnresolved
from mpvqc.importing.viewmodels import build_video_step

VIDEO_A = Path("/movies/a.mp4")
VID_A_DOC = VideoSource(path=VIDEO_A, found_in_document=True)

UNRESOLVED = VideoUnresolved(candidates=(VID_A_DOC,))


@pytest.fixture
def parent(qt_app):
    # Held for the whole test: the step is parented to it, and a collected parent takes the step with it.
    return QObject()


@pytest.fixture
def step(parent):
    step = build_video_step(parent, UNRESOLVED)
    assert step is not None
    return step


def test_build_video_step_only_for_unresolved_concern(parent):
    assert build_video_step(parent, UNRESOLVED) is not None
    assert build_video_step(parent, VideoLoad(path=VIDEO_A)) is None
    assert build_video_step(parent, VideoSkip()) is None


def test_defaults_to_the_first_candidate(step):
    assert step.resolved == VideoLoad(path=VIDEO_A)


def test_selecting_the_skip_entry_resolves_to_skip(step):
    skip_index = step.candidates.rowCount() - 1

    step.selectedIndex = skip_index

    assert step.resolved == VideoSkip()
