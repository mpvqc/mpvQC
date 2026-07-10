# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QWindow

from mpvqc.services.platform.fullscreen import QtFullscreenHandler


@pytest.fixture
def handler() -> QtFullscreenHandler:
    return QtFullscreenHandler()


class RoundTripTestCase(NamedTuple):
    name: str
    initial_states: Qt.WindowState
    expected_states_while_fullscreen: Qt.WindowState


@pytest.mark.parametrize(
    "case",
    [
        RoundTripTestCase(
            "from_normal",
            initial_states=Qt.WindowState.WindowNoState,
            expected_states_while_fullscreen=Qt.WindowState.WindowFullScreen,
        ),
        RoundTripTestCase(
            "from_maximized_keeps_maximized",
            initial_states=Qt.WindowState.WindowMaximized,
            expected_states_while_fullscreen=Qt.WindowState.WindowFullScreen | Qt.WindowState.WindowMaximized,
        ),
    ],
    ids=lambda case: case.name,
)
def test_round_trip(case: RoundTripTestCase, qt_app, handler):
    window = QWindow()
    window.setWindowStates(case.initial_states)

    handler.enter(window)
    assert handler.is_active(window)
    assert window.windowStates() == case.expected_states_while_fullscreen

    handler.exit(window)
    assert not handler.is_active(window)
    assert window.windowStates() == case.initial_states


def test_exit_without_enter_keeps_states(qt_app, handler):
    window = QWindow()
    window.setWindowStates(Qt.WindowState.WindowMaximized)

    handler.exit(window)

    assert not handler.is_active(window)
    assert window.windowStates() == Qt.WindowState.WindowMaximized


def test_repeated_enter_is_idempotent(qt_app, handler):
    window = QWindow()

    handler.enter(window)
    handler.enter(window)

    assert handler.is_active(window)
    assert window.windowStates() == Qt.WindowState.WindowFullScreen
