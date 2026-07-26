# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from typing import NamedTuple

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QWindow

from mpvqc.services.platform.window_state import QtWindowStateHandler

NO_STATE = Qt.WindowState.WindowNoState
MINIMIZED = Qt.WindowState.WindowMinimized
MAXIMIZED = Qt.WindowState.WindowMaximized
FULLSCREEN = Qt.WindowState.WindowFullScreen


class RecordingApplier:
    def __init__(self) -> None:
        self.margins: list[int] = []

    def apply_content_margins(self, margin: int) -> None:
        self.margins.append(margin)


class OperationTestCase(NamedTuple):
    name: str
    operation: Callable[[QtWindowStateHandler, QWindow], None]
    initial: Qt.WindowState
    expected: Qt.WindowState


@pytest.mark.parametrize(
    "case",
    [
        OperationTestCase(
            "minimize_from_normal",
            QtWindowStateHandler.minimize,
            NO_STATE,
            MINIMIZED,
        ),
        OperationTestCase(
            "minimize_keeps_maximized",
            QtWindowStateHandler.minimize,
            MAXIMIZED,
            MAXIMIZED | MINIMIZED,
        ),
        OperationTestCase(
            "minimize_keeps_fullscreen",
            QtWindowStateHandler.minimize,
            FULLSCREEN,
            FULLSCREEN | MINIMIZED,
        ),
        OperationTestCase(
            "maximize_from_normal",
            QtWindowStateHandler.maximize,
            NO_STATE,
            MAXIMIZED,
        ),
        OperationTestCase(
            "maximize_replaces_minimized",
            QtWindowStateHandler.maximize,
            MINIMIZED,
            MAXIMIZED,
        ),
        OperationTestCase(
            "show_normal_clears_maximized",
            QtWindowStateHandler.show_normal,
            MAXIMIZED,
            NO_STATE,
        ),
        OperationTestCase(
            "enter_fullscreen_from_normal",
            QtWindowStateHandler.enter_fullscreen,
            NO_STATE,
            FULLSCREEN,
        ),
        OperationTestCase(
            "enter_fullscreen_keeps_maximized",
            QtWindowStateHandler.enter_fullscreen,
            MAXIMIZED,
            FULLSCREEN | MAXIMIZED,
        ),
        OperationTestCase(
            "exit_fullscreen_restores_maximized",
            QtWindowStateHandler.exit_fullscreen,
            FULLSCREEN | MAXIMIZED,
            MAXIMIZED,
        ),
        OperationTestCase(
            "exit_fullscreen_to_normal",
            QtWindowStateHandler.exit_fullscreen,
            FULLSCREEN,
            NO_STATE,
        ),
    ],
    ids=lambda case: case.name,
)
def test_operations_request_expected_states(case: OperationTestCase, make_recording_window):
    window = make_recording_window(case.initial)
    handler = QtWindowStateHandler()

    case.operation(handler, window)

    assert window.requests == [case.expected]


class StateReadTestCase(NamedTuple):
    name: str
    states: Qt.WindowState
    is_fullscreen: bool
    is_maximized: bool


@pytest.mark.parametrize(
    "case",
    [
        StateReadTestCase("normal", NO_STATE, is_fullscreen=False, is_maximized=False),
        StateReadTestCase("maximized", MAXIMIZED, is_fullscreen=False, is_maximized=True),
        StateReadTestCase("fullscreen", FULLSCREEN, is_fullscreen=True, is_maximized=False),
        StateReadTestCase("fullscreen_over_maximized", FULLSCREEN | MAXIMIZED, is_fullscreen=True, is_maximized=True),
        StateReadTestCase("minimized_from_maximized", MAXIMIZED | MINIMIZED, is_fullscreen=False, is_maximized=True),
    ],
    ids=lambda case: case.name,
)
def test_state_reads(case: StateReadTestCase, make_recording_window):
    window = make_recording_window(case.states)
    handler = QtWindowStateHandler()

    assert handler.is_fullscreen(window) is case.is_fullscreen
    assert handler.is_maximized(window) is case.is_maximized


class ShadowMarginTestCase(NamedTuple):
    name: str
    composed_margin: int
    states: Qt.WindowState
    expected: int


@pytest.mark.parametrize(
    "case",
    [
        ShadowMarginTestCase(
            "composed_margin_defaults_to_zero",
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
    handler = QtWindowStateHandler(shadow_margin=case.composed_margin)

    assert handler.shadow_margin(window) == case.expected


def test_apply_content_margins_forwards_to_applier():
    applier = RecordingApplier()
    handler = QtWindowStateHandler(shadow_margin=88, margins_applier=applier)

    handler.apply_content_margins(42)

    assert applier.margins == [42]


def test_default_applier_accepts_margins():
    QtWindowStateHandler().apply_content_margins(42)
