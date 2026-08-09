# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, override

from PySide6.QtCore import QEvent, QObject, Qt, Signal, Slot
from PySide6.QtGui import QGuiApplication, QRegion

from .resize_filter import RESIZE_BAND_WIDTH, WindowResizeFilter
from .window_geometry import apply_wayland_content_margins

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtGui import QWindow


class WindowExposeFilter(QObject):
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


class SurfaceController(QObject):
    """Keeps the drop shadow margin, the input mask and the resize band in step
    with the window state."""

    drop_shadow_margin_changed = Signal(int)

    def __init__(self, *, drop_shadow_margin: int) -> None:
        super().__init__()
        self._normal_drop_shadow_margin = drop_shadow_margin
        self._window: QWindow | None = None
        self._event_filter: WindowResizeFilter | None = None
        self._expose_filter: WindowExposeFilter | None = None
        self._applied_drop_shadow_margin = 0

    def configure_window(self, app: QGuiApplication, window: QWindow) -> None:
        self._window = window
        self._event_filter = event_filter = WindowResizeFilter(window, app)
        window.installEventFilter(event_filter)

        # The inset and the mask need a mapped surface, and the inset is
        # ignored until it is exposed, so apply both again on show and on
        # expose.
        self._expose_filter = expose_filter = WindowExposeFilter(window, self._reassert_surface)
        window.installEventFilter(expose_filter)
        window.visibleChanged.connect(self._on_visible_changed)
        window.widthChanged.connect(self._apply_input_mask)
        window.heightChanged.connect(self._apply_input_mask)
        window.windowStateChanged.connect(self._sync_drop_shadow_margin)
        window.screenChanged.connect(self._on_screen_changed)

        self._sync_drop_shadow_margin()

    def drop_shadow_margin(self, window: QWindow) -> int:
        states = window.windowStates()
        collapsed = Qt.WindowState.WindowMaximized | Qt.WindowState.WindowFullScreen
        if states & collapsed:
            return 0
        return self._normal_drop_shadow_margin

    def on_drop_shadow_margin_changed(self, callback: Callable[[int], None]) -> None:
        self.drop_shadow_margin_changed.connect(callback)

    @Slot()
    def _sync_drop_shadow_margin(self) -> None:
        if self._window is None:
            return

        margin = self.drop_shadow_margin(self._window)
        if margin == self._applied_drop_shadow_margin:
            return

        self._applied_drop_shadow_margin = margin
        if self._event_filter is not None:
            self._event_filter.set_drop_shadow_margin(margin)
        self._reassert_surface()
        self.drop_shadow_margin_changed.emit(margin)

    @Slot(bool)
    def _on_visible_changed(self, visible: bool) -> None:
        if visible:
            self._reassert_surface()

    @Slot()
    def _on_screen_changed(self) -> None:
        self._reassert_surface()

    def _reassert_surface(self) -> None:
        self._apply_window_geometry()
        self._apply_input_mask()

    def _apply_window_geometry(self) -> None:
        if self._window is None:
            return

        if QGuiApplication.platformName() == "wayland":
            apply_wayland_content_margins(self._window, self._applied_drop_shadow_margin)
            return

        # Someone who cares would need to add X11 (platformName "xcb") support here

    @Slot()
    def _apply_input_mask(self) -> None:
        # Without a mask the transparent shadow swallows clicks. Restrict input
        # to the content plus the resize band so they fall through to whatever
        # sits behind the window.
        if self._window is None:
            return

        width = self._window.width()
        height = self._window.height()

        inset = max(0, self._applied_drop_shadow_margin - RESIZE_BAND_WIDTH)
        self._window.setMask(QRegion(inset, inset, width - 2 * inset, height - 2 * inset))
