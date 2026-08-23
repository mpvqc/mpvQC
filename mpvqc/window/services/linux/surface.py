# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, override

from PySide6.QtCore import QEvent, QObject, Qt, Signal, Slot
from PySide6.QtGui import QGuiApplication, QRegion

from mpvqc.window.services.surface import NO_OWN_FRAME, SurfaceSnapshot

from .resize_filter import RESIZE_BAND_WIDTH, WindowResizeFilter
from .window_geometry import apply_wayland_content_margins, wayland_window_states

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
    """Keeps the surface, the input mask and the resize band in step with the
    window state."""

    surface_changed = Signal(SurfaceSnapshot)

    def __init__(self, *, drop_shadow_margin: int) -> None:
        super().__init__()
        self._drop_shadow_margin = drop_shadow_margin
        self._window: QWindow | None = None
        self._event_filter: WindowResizeFilter | None = None
        self._expose_filter: WindowExposeFilter | None = None
        self._applied_surface = NO_OWN_FRAME

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
        window.widthChanged.connect(self._on_size_changed)
        window.heightChanged.connect(self._on_size_changed)
        window.windowStateChanged.connect(self._sync_surface)
        window.screenChanged.connect(self._on_screen_changed)

        self._sync_surface()

    def read_surface(self, window: QWindow) -> SurfaceSnapshot:
        states = _applied_window_states(window)
        collapsed = Qt.WindowState.WindowMaximized | Qt.WindowState.WindowFullScreen
        if states & collapsed:
            return NO_OWN_FRAME
        return SurfaceSnapshot(draws_own_frame=True, drop_shadow_margin=self._drop_shadow_margin)

    def on_surface_changed(self, callback: Callable[[SurfaceSnapshot], None]) -> None:
        self.surface_changed.connect(callback)

    @Slot()
    def _sync_surface(self) -> None:
        if self._window is None:
            return

        surface = self.read_surface(self._window)
        if surface == self._applied_surface:
            return

        self._applied_surface = surface
        if self._event_filter is not None:
            self._event_filter.set_drop_shadow_margin(surface.drop_shadow_margin)
        self._reassert_surface()
        self.surface_changed.emit(surface)

    @Slot()
    def _on_size_changed(self) -> None:
        # The resize is the trigger, the state signal only a backstop: the
        # compositor's configure resizes first and reports the state one queued
        # event later. ADR 0021 has the frame-by-frame.
        self._sync_surface()
        self._apply_input_mask()

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
            apply_wayland_content_margins(self._window, self._applied_surface.drop_shadow_margin)
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

        inset = max(0, self._applied_surface.drop_shadow_margin - RESIZE_BAND_WIDTH)
        self._window.setMask(QRegion(inset, inset, width - 2 * inset, height - 2 * inset))


def _applied_window_states(window: QWindow) -> Qt.WindowState:
    # QWindow::windowStates still answers the old states during the compositor's
    # resize; the platform window already holds the ones the configure applied.
    if QGuiApplication.platformName() == "wayland":
        states = wayland_window_states(window)
        if states is not None:
            return states
    return window.windowStates()
