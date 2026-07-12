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
    border = get_resize_border_thickness_for_dpi(dpi, horizontal=False)
    caption = get_caption_height_for_dpi(dpi)
    return border + caption


def _sync_qt_frame_bookkeeping(hwnd: int) -> None:
    # Qt corrects its frame margins only when a geometry event arrives, and the
    # Qt Quick scene resizes only on a real size change. Without this, the first
    # scene keeps the stale margins even though the QWindow property already
    # holds the new value. Resizing by one pixel and back forces both to update.
    rect = get_window_rect(int(hwnd))
    if rect is None:
        return

    left, top, right, bottom = rect
    width, height = right - left, bottom - top
    resize_window(int(hwnd), width, height + 1)
    resize_window(int(hwnd), width, height)
