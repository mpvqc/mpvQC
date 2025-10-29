# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import cache

from PySide6.QtGui import QGuiApplication, QWindow


@cache
def get_main_window() -> QWindow:
    for window in QGuiApplication.topLevelWindows():
        if window.objectName() == "MpvqcMainWindow":
            return window

    msg = "Could not find window with name: MpvqcMainWindow"
    raise ValueError(msg)
