# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, override

from PySide6.QtCore import QEvent, QObject, QTimer
from PySide6.QtQuick import QQuickWindow

from .utils import set_window_cloaked, wait_for_next_composition

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)

REVEAL_FALLBACK_MS = 1000


class WindowRevealFilter(QObject):
    """Reveals every Qt Quick window only once its first frame has been presented.
    Windows fills the gap between showing a fresh window and the first present
    with an uninitialized white surface, so the window stays DWM-cloaked for that
    gap. Covers the main window and the native popup windows Qt creates for
    dialogs alike, which is why it filters application-wide."""

    def __init__(self) -> None:
        super().__init__()
        self._pending: dict[QQuickWindow, Callable[[], None]] = {}

    @override
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if isinstance(watched, QQuickWindow):
            if event.type() == QEvent.Type.Show:
                self._conceal_until_first_frame(watched)
            elif event.type() == QEvent.Type.Hide:
                self._reveal_pending(watched)
        return False

    def _conceal_until_first_frame(self, window: QQuickWindow) -> None:
        if window in self._pending:
            return

        hwnd = int(window.winId())
        set_window_cloaked(hwnd, cloaked=True)

        def reveal() -> None:
            if self._pending.pop(window, None) is None:
                return
            try:
                window.frameSwapped.disconnect(reveal)
            except RuntimeError:
                # The window died before its first frame; nothing left to reveal.
                return
            # frameSwapped only means the frame is queued: uncloaking before the
            # compositor consumed it still flashes the uninitialized surface.
            wait_for_next_composition()
            set_window_cloaked(hwnd, cloaked=False)

        def reveal_without_frame() -> None:
            if window in self._pending:
                logger.debug("Revealing a window whose first frame never arrived")
                reveal()

        self._pending[window] = reveal
        window.frameSwapped.connect(reveal)

        # If the first frame never arrives, reveal anyway: a stale cloak would
        # leave a window invisible that Qt considers shown.
        QTimer.singleShot(REVEAL_FALLBACK_MS, reveal_without_frame)

    def _reveal_pending(self, window: QQuickWindow) -> None:
        if (reveal := self._pending.get(window)) is not None:
            reveal()
