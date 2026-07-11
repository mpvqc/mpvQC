# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from ctypes import windll
from typing import TYPE_CHECKING

import win32con
import win32gui
from PySide6.QtCore import QMargins, Qt

from .event import WindowsEventFilter
from .reveal_filter import WindowRevealFilter
from .utils import SM_CXPADDEDBORDER, set_window_transitions_enabled

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow


class WindowsFrameIntegration:
    """Keeps the full native window frame and reclaims only the caption strip for
    the QML title bar, via Qt's "_q_windowsCustomMargins". The left/right/bottom
    resize bands stay in the invisible non-client frame outside the content;
    shadows, borders, corners and DWM animations stay native."""

    def __init__(self) -> None:
        self._event_filter = WindowsEventFilter()
        self._reveal_filter = WindowRevealFilter()

    def configure_window(self, app: QGuiApplication, window: QWindow) -> None:
        # Flags and margins are only read at native window creation, which the
        # winId() call below triggers.
        window.setFlags(Qt.WindowType.Window)
        window.setProperty("_q_windowsCustomMargins", QMargins(0, -_caption_inset(), 0, 0))

        hwnd_top_lvl = window.winId()
        self._event_filter.set_top_lvl_hwnd(hwnd_top_lvl)
        self._reveal_filter.set_main_window_hwnd(int(hwnd_top_lvl))
        app.installNativeEventFilter(self._event_filter)
        app.installEventFilter(self._reveal_filter)

        _sync_qt_frame_bookkeeping(hwnd_top_lvl)

    def track(self, win_id: int) -> None:
        self._event_filter.set_embedded_player_hwnd(win_id)
        # The embedded player lives inside the QML scene like a child item; DWM
        # must not animate it as an independent top-level window.
        set_window_transitions_enabled(win_id, enabled=False)


def _caption_inset() -> int:
    dpi = windll.user32.GetDpiForSystem()
    border = windll.user32.GetSystemMetricsForDpi(win32con.SM_CYSIZEFRAME, dpi) + windll.user32.GetSystemMetricsForDpi(
        SM_CXPADDEDBORDER, dpi
    )
    caption = windll.user32.GetSystemMetricsForDpi(win32con.SM_CYCAPTION, dpi)
    return border + caption


def _sync_qt_frame_bookkeeping(hwnd) -> None:
    # Qt corrects its frame margins only on a geometry event, and the Qt Quick
    # scene follows only on a real size change: the initial scene is sized with
    # the stale margins while the QWindow property keeps the requested value.
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width, height = right - left, bottom - top
    flags = win32con.SWP_NOMOVE | win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE
    windll.user32.SetWindowPos(int(hwnd), None, 0, 0, width, height + 1, flags)
    windll.user32.SetWindowPos(int(hwnd), None, 0, 0, width, height, flags)
