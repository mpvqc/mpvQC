# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from typing import NamedTuple

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QWindow

from mpvqc.window.services import QtWindowStateHandler, WindowStateSnapshot

NO_STATE = Qt.WindowState.WindowNoState
MINIMIZED = Qt.WindowState.WindowMinimized
MAXIMIZED = Qt.WindowState.WindowMaximized
FULLSCREEN = Qt.WindowState.WindowFullScreen


class OperationTestCase(NamedTuple):
    name: str
    operation: Callable[[QtWindowStateHandler, QWindow], None]
    initial: Qt.WindowState
    expected: Qt.WindowState


@pytest.mark.parametrize(
    "case",
    [
        OperationTestCase(
            name="minimize_from_normal",
            operation=QtWindowStateHandler.minimize,
            initial=NO_STATE,
            expected=MINIMIZED,
        ),
        OperationTestCase(
            name="minimize_keeps_maximized",
            operation=QtWindowStateHandler.minimize,
            initial=MAXIMIZED,
            expected=MAXIMIZED | MINIMIZED,
        ),
        OperationTestCase(
            name="minimize_keeps_fullscreen",
            operation=QtWindowStateHandler.minimize,
            initial=FULLSCREEN,
            expected=FULLSCREEN | MINIMIZED,
        ),
        OperationTestCase(
            name="maximize_from_normal",
            operation=QtWindowStateHandler.maximize,
            initial=NO_STATE,
            expected=MAXIMIZED,
        ),
        OperationTestCase(
            name="maximize_replaces_minimized",
            operation=QtWindowStateHandler.maximize,
            initial=MINIMIZED,
            expected=MAXIMIZED,
        ),
        OperationTestCase(
            name="show_normal_clears_maximized",
            operation=QtWindowStateHandler.show_normal,
            initial=MAXIMIZED,
            expected=NO_STATE,
        ),
        OperationTestCase(
            name="enter_fullscreen_from_normal",
            operation=QtWindowStateHandler.enter_fullscreen,
            initial=NO_STATE,
            expected=FULLSCREEN,
        ),
        OperationTestCase(
            name="enter_fullscreen_keeps_maximized",
            operation=QtWindowStateHandler.enter_fullscreen,
            initial=MAXIMIZED,
            expected=FULLSCREEN | MAXIMIZED,
        ),
        OperationTestCase(
            name="exit_fullscreen_restores_maximized",
            operation=QtWindowStateHandler.exit_fullscreen,
            initial=FULLSCREEN | MAXIMIZED,
            expected=MAXIMIZED,
        ),
        OperationTestCase(
            name="exit_fullscreen_to_normal",
            operation=QtWindowStateHandler.exit_fullscreen,
            initial=FULLSCREEN,
            expected=NO_STATE,
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
    expected: WindowStateSnapshot


@pytest.mark.parametrize(
    "case",
    [
        StateReadTestCase(
            name="normal",
            states=NO_STATE,
            expected=WindowStateSnapshot(is_fullscreen=False, is_maximized=False),
        ),
        StateReadTestCase(
            name="maximized",
            states=MAXIMIZED,
            expected=WindowStateSnapshot(is_fullscreen=False, is_maximized=True),
        ),
        StateReadTestCase(
            name="fullscreen",
            states=FULLSCREEN,
            expected=WindowStateSnapshot(is_fullscreen=True, is_maximized=False),
        ),
        StateReadTestCase(
            name="fullscreen_over_maximized",
            states=FULLSCREEN | MAXIMIZED,
            expected=WindowStateSnapshot(is_fullscreen=True, is_maximized=True),
        ),
        StateReadTestCase(
            name="minimized_from_maximized",
            states=MAXIMIZED | MINIMIZED,
            expected=WindowStateSnapshot(is_fullscreen=False, is_maximized=True),
        ),
    ],
    ids=lambda case: case.name,
)
def test_read_state(case: StateReadTestCase, make_recording_window):
    window = make_recording_window(case.states)
    handler = QtWindowStateHandler()

    assert handler.read_state(window) == case.expected
