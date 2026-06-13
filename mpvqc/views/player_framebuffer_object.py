# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from threading import Lock
from typing import TYPE_CHECKING, cast, override

import inject
from PySide6.QtCore import QSize, Signal, Slot
from PySide6.QtGui import QGuiApplication, QNativeInterface, QOpenGLContext
from PySide6.QtQml import QmlElement
from PySide6.QtQuick import QQuickFramebufferObject

from mpvqc.services import MainWindowService, PlayerService

if TYPE_CHECKING:
    from types import NoneType

    from mpv import MpvRenderContext
    from PySide6.QtOpenGL import QOpenGLFramebufferObject


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


def get_process_address(_: NoneType, name: bytes) -> int:
    current_gl_context = QOpenGLContext.currentContext()
    if current_gl_context:
        return current_gl_context.getProcAddress(name)
    return 0


def get_display_params() -> dict[str, int]:
    app = QGuiApplication.instance()
    if not isinstance(app, QGuiApplication):
        return {}
    native = app.nativeInterface()
    if native is None:
        return {}
    match QGuiApplication.platformName():
        case "wayland":
            display = cast("QNativeInterface.QWaylandApplication", native).display()
            return {"wl_display": display} if display else {}
        case "xcb":
            display = cast("QNativeInterface.QX11Application", native).display()
            return {"x11_display": display} if display else {}
        case _:
            return {}


@QmlElement
class MpvqcMpvFrameBufferObjectPyObject(QQuickFramebufferObject):
    _player = inject.attr(PlayerService)

    update_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._renderer: Renderer | None = None
        self.update_requested.connect(self.do_update)
        self._player.set_shutdown_hook(self._release)

    @Slot()
    def do_update(self) -> None:
        self.update()

    def _release(self) -> None:
        if self._renderer is not None:
            self._renderer.release()
        self._player.set_shutdown_hook(None)

    @override
    def createRenderer(self) -> QQuickFramebufferObject.Renderer:
        self._renderer = r = Renderer(self)
        return r


class Renderer(QQuickFramebufferObject.Renderer):
    _main_window = inject.attr(MainWindowService)
    _player = inject.attr(PlayerService)

    def __init__(self, parent: MpvqcMpvFrameBufferObjectPyObject) -> None:
        super().__init__()
        self._parent = parent
        self._ctx: MpvRenderContext | None = None
        self._lock = Lock()
        self._main_window.display_zoom_factor_changed.connect(self._on_zoom_factor_changed)

    def _on_zoom_factor_changed(self) -> None:
        self._parent.update_requested.emit()

    @override
    def createFramebufferObject(self, size: QSize) -> QOpenGLFramebufferObject:
        if self._ctx is None:
            self._player.init()
            self._ctx = self._player.create_render_context(
                get_proc_address=get_process_address,
                display_params=get_display_params(),
            )
            self._ctx.update_cb = self._parent.update_requested.emit

        return QQuickFramebufferObject.Renderer.createFramebufferObject(self, size)

    @override
    def render(self) -> None:
        with self._lock:
            if self._ctx is None:
                return

            fbo = self.framebufferObject()
            size = fbo.size()
            self._ctx.render(flip_y=False, opengl_fbo={"w": size.width(), "h": size.height(), "fbo": fbo.handle()})

    def release(self) -> None:
        with self._lock:
            if self._ctx is not None:
                self._ctx.free()
                self._ctx = None
