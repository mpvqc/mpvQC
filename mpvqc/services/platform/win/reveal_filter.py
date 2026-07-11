# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import contextlib
from typing import override

from PySide6.QtCore import QEvent, QObject, Qt, Slot
from PySide6.QtQuick import QQuickItem, QQuickWindow

from .utils import set_window_cloaked, wait_for_next_composition


class WindowRevealFilter(QObject):
    """Keeps a Qt Quick window invisible to the compositor whenever it has no
    valid content on screen. On show, every window stays DWM-cloaked until the
    compositor has consumed its first frame: Windows would otherwise fill the
    gap with an uninitialized white surface. Transient windows (dialogs, message
    boxes: every Quick window except the main one) are cloaked again the moment
    their content is torn out or they start to hide, since Qt dismantles a
    Qt-side-closed popup inside the still visible window and hides it only
    deferred. The main window is left to hide with its native DWM animation.
    Filters application-wide to also cover the native windows Qt creates for
    windowed dialogs."""

    def __init__(self) -> None:
        super().__init__()
        self._main_hwnd: int | None = None
        self._pending: dict[QQuickWindow, int] = {}
        self._transient_hwnds: dict[QObject, int] = {}

    def set_main_window_hwnd(self, hwnd: int) -> None:
        self._main_hwnd = hwnd

    @override
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if isinstance(watched, QQuickWindow) and event.type() == QEvent.Type.Show:
            if not self._is_main_window(watched):
                self._track_transient(watched)
                if not watched.contentItem().childItems():
                    self._conceal_empty_transient(watched)
                    return False
            self._conceal_until_first_frame(watched)
        return False

    def _is_main_window(self, window: QQuickWindow) -> bool:
        return self._main_hwnd is not None and int(window.winId()) == self._main_hwnd

    def _conceal_empty_transient(self, window: QQuickWindow) -> None:
        # A transient window shown without content is mid-teardown; do not arm a
        # reveal, or a stray frame of the emptied window would uncloak it and flash.
        set_window_cloaked(int(window.winId()), cloaked=True)

    def _conceal_until_first_frame(self, window: QQuickWindow) -> None:
        if window in self._pending:
            return

        hwnd = int(window.winId())
        set_window_cloaked(hwnd, cloaked=True)
        self._pending[window] = hwnd
        window.frameSwapped.connect(self._reveal_on_first_frame, Qt.ConnectionType.QueuedConnection)

    @Slot()
    def _reveal_on_first_frame(self) -> None:
        window = self.sender()
        if isinstance(window, QQuickWindow):
            self._reveal(window)

    def _reveal(self, window: QQuickWindow) -> None:
        hwnd = self._pending.pop(window, None)
        if hwnd is None:
            return

        try:
            window.frameSwapped.disconnect(self._reveal_on_first_frame)
        except RuntimeError:
            # The window died before its first frame; nothing left to reveal.
            return

        # frameSwapped only means the frame is queued: uncloaking before the
        # compositor consumed it still flashes the uninitialized surface.
        wait_for_next_composition()
        set_window_cloaked(hwnd, cloaked=False)

    def _track_transient(self, window: QQuickWindow) -> None:
        if window in self._transient_hwnds:
            return

        self._transient_hwnds[window] = int(window.winId())
        window.visibleChanged.connect(self._conceal_on_hide)
        window.contentItem().childrenChanged.connect(self._conceal_on_content_teardown)
        window.destroyed.connect(self._forget_transient)

    @Slot(bool)
    def _conceal_on_hide(self, visible: bool) -> None:
        if visible:
            return

        window = self.sender()
        if not isinstance(window, QQuickWindow):
            return

        hwnd = self._transient_hwnds.get(window)
        if hwnd is None:
            return

        # visibleChanged arrives before the native hide: cloaking now keeps the
        # teardown frames and the DWM hide transition off the screen.
        self._cancel_pending(window)
        set_window_cloaked(hwnd, cloaked=True)

    @Slot()
    def _conceal_on_content_teardown(self) -> None:
        content_item = self.sender()
        if not isinstance(content_item, QQuickItem) or content_item.childItems():
            return

        window = content_item.window()
        if window is None:
            return

        hwnd = self._transient_hwnds.get(window)
        if hwnd is None:
            return

        # Closing a windowed popup Qt-side tears the dialog out of the still
        # visible window and only hides it deferred (finalizeExitTransition
        # reparents the popup item first): cloak the moment the content leaves,
        # before the emptied window can reach the screen.
        self._cancel_pending(window)
        set_window_cloaked(hwnd, cloaked=True)

    @Slot(QObject)
    def _forget_transient(self, window: QObject) -> None:
        self._transient_hwnds.pop(window, None)

    def _cancel_pending(self, window: QQuickWindow) -> None:
        if self._pending.pop(window, None) is None:
            return
        with contextlib.suppress(RuntimeError):
            window.frameSwapped.disconnect(self._reveal_on_first_frame)
