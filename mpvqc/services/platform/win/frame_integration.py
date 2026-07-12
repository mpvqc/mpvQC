# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

import win32con
import win32gui
from PySide6.QtCore import QMargins, Qt

from .event import WindowsEventFilter
from .utils import SM_CXPADDEDBORDER, GetSystemMetricsForDpi, SetWindowPos, get_primary_monitor_dpi

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow


class WindowsFrameIntegration:
    """Keeps the full native window frame and reclaims only the caption strip for
    the QML title bar, via Qt's "_q_windowsCustomMargins". The left/right/bottom
    resize bands stay in the invisible non-client frame outside the content;
    shadows, borders, corners and DWM animations stay native."""

    def __init__(self) -> None:
        self._event_filter = WindowsEventFilter()

    def configure_window(self, app: QGuiApplication, window: QWindow) -> None:
        # Flags and margins are only read at native window creation, which the
        # winId() call below triggers.
        window.setFlags(Qt.WindowType.Window)
        window.setProperty("_q_windowsCustomMargins", QMargins(0, -_caption_inset(), 0, 0))

        hwnd_top_lvl = window.winId()
        self._event_filter.set_top_lvl_hwnd(hwnd_top_lvl)
        app.installNativeEventFilter(self._event_filter)

        _sync_qt_frame_bookkeeping(hwnd_top_lvl)

    def track(self, win_id: int) -> None:
        self._event_filter.set_embedded_player_hwnd(win_id)


def _caption_inset() -> int:
    dpi = get_primary_monitor_dpi()
    border = GetSystemMetricsForDpi(win32con.SM_CYSIZEFRAME, dpi) + GetSystemMetricsForDpi(SM_CXPADDEDBORDER, dpi)
    caption = GetSystemMetricsForDpi(win32con.SM_CYCAPTION, dpi)
    return border + caption


def _sync_qt_frame_bookkeeping(hwnd: int) -> None:
    # Qt corrects its frame margins only on a geometry event, and the Qt Quick
    # scene follows only on a real size change: the initial scene is sized with
    # the stale margins while the QWindow property keeps the requested value.
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width, height = right - left, bottom - top
    flags = win32con.SWP_NOMOVE | win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE
    SetWindowPos(int(hwnd), None, 0, 0, width, height + 1, flags)
    SetWindowPos(int(hwnd), None, 0, 0, width, height, flags)
