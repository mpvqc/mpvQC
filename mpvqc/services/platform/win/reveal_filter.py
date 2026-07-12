# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import contextlib
from functools import partial
from typing import TYPE_CHECKING, override

from PySide6.QtCore import QEvent, QObject, Qt, Slot
from PySide6.QtQuick import QQuickItem, QQuickWindow

from .native import set_window_cloaked
from .utils import wait_for_next_composition

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtGui import QGuiApplication, QWindow


class _FirstFrameGate(QObject):
    """Receives one show cycle's frameSwapped delivery. Unparented on purpose:
    the pending map holds the only reference, so dropping it destroys the gate
    synchronously and Qt sweeps any queued metacall still aimed at it — a stale
    frame notification from a previous show cycle can never trigger this
    cycle's reveal."""

    def __init__(self, on_first_frame: Callable[[], None]) -> None:
        super().__init__()
        self._on_first_frame = on_first_frame

    @Slot()
    def notify(self) -> None:
        self._on_first_frame()


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
        self._pending: dict[QQuickWindow, tuple[int, _FirstFrameGate]] = {}
        self._transient_hwnds: dict[QObject, int] = {}

    def install(self, app: QGuiApplication, main_window: QWindow) -> None:
        self._main_hwnd = int(main_window.winId())
        app.installEventFilter(self)

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

        gate = _FirstFrameGate(partial(self._reveal, window))
        self._pending[window] = (hwnd, gate)
        window.frameSwapped.connect(gate.notify, Qt.ConnectionType.QueuedConnection)

    def _reveal(self, window: QQuickWindow) -> None:
        entry = self._pending.pop(window, None)
        if entry is None:
            return

        hwnd, gate = entry
        try:
            window.frameSwapped.disconnect(gate.notify)
        except RuntimeError:
            # The window died before its first frame; nothing left to reveal.
            return

        # frameSwapped only means the frame is queued: give the compositor one
        # composition pass to consume it before uncloaking. One pass usually
        # suffices, but nothing guarantees it.
        wait_for_next_composition()
        set_window_cloaked(hwnd, cloaked=False)

    def _track_transient(self, window: QQuickWindow) -> None:
        if window in self._transient_hwnds:
            return

        self._transient_hwnds[window] = int(window.winId())
        window.visibleChanged.connect(self._conceal_on_hide)
        window.contentItem().childrenChanged.connect(self._conceal_on_content_teardown)
        # destroyed delivers a fresh wrapper typed as plain QObject, which never
        # matches the tracked key; bind the tracked wrapper at connect time.
        window.destroyed.connect(partial(self._forget_transient, window))

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

    def _forget_transient(self, window: QQuickWindow, _deleted: QObject | None = None) -> None:
        self._transient_hwnds.pop(window, None)
        self._pending.pop(window, None)

    def _cancel_pending(self, window: QQuickWindow) -> None:
        entry = self._pending.pop(window, None)
        if entry is None:
            return

        _hwnd, gate = entry
        with contextlib.suppress(RuntimeError):
            window.frameSwapped.disconnect(gate.notify)
        # Dropping the last reference destroys the gate here, synchronously,
        # which sweeps any stale queued frameSwapped delivery.
