# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from typing import override

import pytest
from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QBitmap, QPolygon, QRegion, QWindow


class RecordingWindow(QWindow):
    """Stores window states and masks itself so requests never reach the OS."""

    def __init__(self, states: Qt.WindowState) -> None:
        super().__init__()
        self._states = states
        self.requests: list[object] = []
        self.masks: list[QBitmap | QPolygon | QRect | QRegion] = []
        self.win_id_calls = 0

    @override
    def windowStates(self) -> Qt.WindowState:
        return self._states

    @override
    def setWindowStates(self, states: Qt.WindowState) -> None:
        self.requests.append(states)
        self._states = states
        self.windowStateChanged.emit(states)

    @override
    def showMinimized(self) -> None:
        self.requests.append("showMinimized")

    @override
    def setMask(self, region: QBitmap | QPolygon | QRect | QRegion) -> None:
        self.masks.append(region)

    @override
    def winId(self) -> int:
        self.win_id_calls += 1
        return 0


@pytest.fixture
def make_recording_window(qt_app) -> Callable[..., RecordingWindow]:
    def make(states: Qt.WindowState = Qt.WindowState.WindowNoState) -> RecordingWindow:
        return RecordingWindow(states)

    return make
