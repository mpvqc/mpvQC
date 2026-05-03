# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import QSize, Signal, Slot
from PySide6.QtGui import QOpenGLContext
from PySide6.QtQml import QmlElement
from PySide6.QtQuick import QQuickFramebufferObject

from mpvqc.services import HostIntegrationService, PlayerService

if TYPE_CHECKING:
    from types import NoneType

    from mpv import MpvRenderContext
    from PySide6.QtOpenGL import QOpenGLFramebufferObject


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


def get_process_address(_: NoneType, name: bytes) -> int:
    current_gl_context = QOpenGLContext.currentContext()
    if current_gl_context:
        return int(current_gl_context.getProcAddress(name))
    return 0


@QmlElement
class MpvqcMpvFrameBufferObjectPyObject(QQuickFramebufferObject):
    update_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.update_requested.connect(self.do_update)

    @Slot()
    def do_update(self) -> None:
        self.update()

    @typing.override
    def createRenderer(self) -> QQuickFramebufferObject.Renderer:
        return Renderer(self)


class Renderer(QQuickFramebufferObject.Renderer):
    _host_integration = inject.attr(HostIntegrationService)
    _player = inject.attr(PlayerService)

    def __init__(self, parent: MpvqcMpvFrameBufferObjectPyObject) -> None:
        super().__init__()
        self._parent = parent
        self._ctx: MpvRenderContext | None = None
        self._host_integration.display_zoom_factor_changed.connect(self._on_zoom_factor_changed)

    def _on_zoom_factor_changed(self) -> None:
        self._parent.update_requested.emit()

    @typing.override
    def createFramebufferObject(self, size: QSize) -> QOpenGLFramebufferObject:
        if self._ctx is None:
            self._player.init()
            self._ctx = self._player.create_render_context(get_proc_address=get_process_address)
            self._ctx.update_cb = self._parent.update_requested.emit

        return QQuickFramebufferObject.Renderer.createFramebufferObject(self, size)

    @typing.override
    def render(self) -> None:
        if self._ctx:
            factor: float = self._host_integration.display_zoom_factor
            rect = self._parent.size()

            width = int(rect.width() * factor)
            height = int(rect.height() * factor)
            fbo = int(self.framebufferObject().handle())

            self._ctx.render(flip_y=False, opengl_fbo={"w": width, "h": height, "fbo": fbo})
