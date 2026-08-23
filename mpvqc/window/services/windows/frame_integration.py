# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QMargins, Qt

from .event import WindowsEventFilter
from .native import (
    get_caption_height_for_dpi,
    get_primary_monitor_dpi,
    get_resize_border_thickness_for_dpi,
    get_window_rect,
    resize_window,
)

if TYPE_CHECKING:
    from PySide6.QtGui import QGuiApplication, QWindow


class WindowsFrameIntegration:
    def __init__(self) -> None:
        self._event_filter = WindowsEventFilter()

    def configure_window(self, app: QGuiApplication, window: QWindow) -> None:
        # Flags and margins are only read at native window creation, which the
        # winId() call below triggers.
        window.setFlags(Qt.WindowType.Window)
        window.setProperty("_q_windowsCustomMargins", QMargins(0, -_caption_inset(), 0, 0))

        hwnd_top_level = window.winId()
        self._event_filter.set_top_level_hwnd(hwnd_top_level)
        app.installNativeEventFilter(self._event_filter)

        _sync_qt_frame_bookkeeping(hwnd_top_level)

    def track(self, win_id: int) -> None:
        self._event_filter.set_embedded_player_hwnd(win_id)


def _caption_inset() -> int:
    dpi = get_primary_monitor_dpi()
    border = get_resize_border_thickness_for_dpi(dpi, horizontal=False)
    caption = get_caption_height_for_dpi(dpi)
    return border + caption


def _sync_qt_frame_bookkeeping(hwnd: int) -> None:
    # Qt corrects its frame margins only on a geometry event, and the scene
    # resizes only on a real size change, so the first scene would keep the
    # stale margins. One pixel out and back settles both.
    rect = get_window_rect(hwnd)
    if rect is None:
        return

    left, top, right, bottom = rect
    width, height = right - left, bottom - top
    resize_window(hwnd, width, height + 1)
    resize_window(hwnd, width, height)
