# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING, NamedTuple

import pytest
from PySide6.QtCore import Qt

from mpvqc.services.platform.linux.surface import SurfaceController
from mpvqc.services.platform.surface import NoSurfaceHandler

if TYPE_CHECKING:
    from mpvqc.services.platform.surface import SurfaceHandler

NO_STATE = Qt.WindowState.WindowNoState
MINIMIZED = Qt.WindowState.WindowMinimized
MAXIMIZED = Qt.WindowState.WindowMaximized
FULLSCREEN = Qt.WindowState.WindowFullScreen


class ShadowMarginTestCase(NamedTuple):
    name: str
    composed_margin: int
    states: Qt.WindowState
    expected: int


@pytest.mark.parametrize(
    "case",
    [
        ShadowMarginTestCase(
            "zero_composed_margin_reads_zero",
            composed_margin=0,
            states=NO_STATE,
            expected=0,
        ),
        ShadowMarginTestCase(
            "normal_uses_composed_margin",
            composed_margin=88,
            states=NO_STATE,
            expected=88,
        ),
        ShadowMarginTestCase(
            "maximized_collapses_margin",
            composed_margin=88,
            states=MAXIMIZED,
            expected=0,
        ),
        ShadowMarginTestCase(
            "fullscreen_collapses_margin",
            composed_margin=88,
            states=FULLSCREEN,
            expected=0,
        ),
        ShadowMarginTestCase(
            "minimized_from_maximized_stays_collapsed",
            composed_margin=88,
            states=MAXIMIZED | MINIMIZED,
            expected=0,
        ),
        ShadowMarginTestCase(
            "minimized_from_normal_keeps_margin",
            composed_margin=88,
            states=MINIMIZED,
            expected=88,
        ),
    ],
    ids=lambda case: case.name,
)
def test_shadow_margin(case: ShadowMarginTestCase, make_recording_window):
    window = make_recording_window(case.states)
    handler: SurfaceHandler = SurfaceController(shadow_margin=case.composed_margin)

    assert handler.shadow_margin(window) == case.expected


def test_no_surface_handler_reads_zero_in_every_state(make_recording_window):
    handler: SurfaceHandler = NoSurfaceHandler()

    for states in (NO_STATE, MINIMIZED, MAXIMIZED, FULLSCREEN):
        assert handler.shadow_margin(make_recording_window(states)) == 0

    handler.apply_content_margins(88)
    assert handler.shadow_margin(make_recording_window(NO_STATE)) == 0
