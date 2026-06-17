# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, override

from PySide6.QtCore import QEvent, QObject
from PySide6.QtGui import QGuiApplication, QRegion

from mpvqc.services.platform.linux import MARGIN_RESIZE_BAND, LinuxEventFilter
from mpvqc.services.platform.linux.window_geometry import apply_wayland_content_margins
from mpvqc.services.platform.window_integration import WindowIntegration

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtGui import QWindow


class _WindowExposeFilter(QObject):
    def __init__(self, window: QWindow, on_mapped: Callable[[], None]) -> None:
        super().__init__()
        self._window = window
        self._on_mapped = on_mapped
        self._was_exposed = False

    @override
    def eventFilter(self, _watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Expose:
            exposed = self._window.isExposed()
            if exposed and not self._was_exposed:
                self._on_mapped()
            self._was_exposed = exposed
        return False


class LinuxWindowIntegration(WindowIntegration):
    def __init__(self) -> None:
        self._window: QWindow | None = None
        self._event_filter: LinuxEventFilter | None = None
        self._expose_filter: _WindowExposeFilter | None = None
        self._margin = 0

    @override
    def configure_for(self, app: QGuiApplication, window: QWindow) -> None:
        self._window = window
        self._event_filter = event_filter = LinuxEventFilter(window, app)
        event_filter.set_resize_margin(self._margin)
        app.installEventFilter(event_filter)

        # The inset and mask need a created, mapped surface, which is not ready
        # at QML-load time. On the first show the inset also does not stick until
        # the surface is actually exposed, so re-assert on show and on expose.
        self._expose_filter = expose_filter = _WindowExposeFilter(window, self._reassert_surface)
        window.installEventFilter(expose_filter)
        window.visibleChanged.connect(self._on_visible_changed)
        window.widthChanged.connect(self._apply_input_mask)
        window.heightChanged.connect(self._apply_input_mask)

    @override
    def set_embedded_player_hwnd(self, win_id: int) -> None:
        pass

    @override
    def apply_content_margins(self, margin: int) -> None:
        self._margin = margin
        if self._event_filter is not None:
            self._event_filter.set_resize_margin(margin)
        self._reassert_surface()

    def _on_visible_changed(self, visible: bool) -> None:
        if visible:
            self._reassert_surface()

    def _reassert_surface(self) -> None:
        self._apply_window_geometry()
        self._apply_input_mask()

    def _apply_window_geometry(self) -> None:
        if self._window is None:
            return

        if QGuiApplication.platformName() == "wayland":
            apply_wayland_content_margins(self._window, self._margin)
            return

        # X11 (platformName "xcb") is NOT supported and is not planned. If it is
        # ever wanted, someone has to implement and maintain that support here.

    def _apply_input_mask(self) -> None:
        # Without a mask the whole padded surface, transparent shadow included,
        # swallows clicks. Restrict input to the content plus the resize band so
        # clicks on the shadow fall through to whatever sits behind the window.
        if self._window is None:
            return

        width = self._window.width()
        height = self._window.height()

        if self._margin <= 0:
            self._window.setMask(QRegion(0, 0, width, height))
            return

        inset = self._margin - MARGIN_RESIZE_BAND
        self._window.setMask(QRegion(inset, inset, width - 2 * inset, height - 2 * inset))
