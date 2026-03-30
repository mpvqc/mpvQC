# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtGui import QGuiApplication, QWindow


class MainWindowService:
    def __init__(self, window: QWindow | None = None) -> None:
        self._window = window

    @property
    def window(self) -> QWindow:
        if self._window is None:
            self._window = window = self._find_window()
            return window
        return self._window

    @staticmethod
    def _find_window() -> QWindow:
        for window in QGuiApplication.topLevelWindows():
            if window.objectName() == "MpvqcMainWindow":
                return window
        msg = "Could not find window with name: MpvqcMainWindow"
        raise ValueError(msg)
