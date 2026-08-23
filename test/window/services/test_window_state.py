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
    expected: WindowStateSnapshot


@pytest.mark.parametrize(
    "case",
    [
        StateReadTestCase(
            "normal",
            NO_STATE,
            WindowStateSnapshot(is_fullscreen=False, is_maximized=False),
        ),
        StateReadTestCase(
            "maximized",
            MAXIMIZED,
            WindowStateSnapshot(is_fullscreen=False, is_maximized=True),
        ),
        StateReadTestCase(
            "fullscreen",
            FULLSCREEN,
            WindowStateSnapshot(is_fullscreen=True, is_maximized=False),
        ),
        StateReadTestCase(
            "fullscreen_over_maximized",
            FULLSCREEN | MAXIMIZED,
            WindowStateSnapshot(is_fullscreen=True, is_maximized=True),
        ),
        StateReadTestCase(
            "minimized_from_maximized",
            MAXIMIZED | MINIMIZED,
            WindowStateSnapshot(is_fullscreen=False, is_maximized=True),
        ),
    ],
    ids=lambda case: case.name,
)
def test_read_state(case: StateReadTestCase, make_recording_window):
    window = make_recording_window(case.states)
    handler = QtWindowStateHandler()

    assert handler.read_state(window) == case.expected
