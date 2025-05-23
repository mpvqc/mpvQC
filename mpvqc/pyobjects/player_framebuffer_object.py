# mpvQC
#
# Copyright (C) 2022 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import inject
from mpv import MpvGlGetProcAddressFn, MpvRenderContext
from PySide6.QtCore import QCoreApplication, QObject, QSize, Signal, Slot
from PySide6.QtGui import QOpenGLContext
from PySide6.QtOpenGL import QOpenGLFramebufferObject
from PySide6.QtQml import QmlElement
from PySide6.QtQuick import QQuickFramebufferObject

from mpvqc.services import OperatingSystemZoomDetectorService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


def get_process_address(_, name):
    current_gl_context = QOpenGLContext.currentContext()
    if current_gl_context:
        return int(current_gl_context.getProcAddress(name))
    return 0


@QmlElement
class MpvqcMpvFrameBufferObjectPyObject(QQuickFramebufferObject):
    sig_on_update = Signal()

    def __init__(self):
        super().__init__()
        self.sig_on_update.connect(self.do_update)

    @Slot()
    def do_update(self):
        self.update()

    def createRenderer(self) -> QQuickFramebufferObject.Renderer:
        return Renderer(self)


class Renderer(QQuickFramebufferObject.Renderer):
    _zoom_detector_service = inject.attr(OperatingSystemZoomDetectorService)

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self._get_proc_address_resolver = MpvGlGetProcAddressFn(get_process_address)
        self._ctx = None

        self._zoom_detector_service.zoom_factor_changed.connect(lambda _: self._parent.sig_on_update.emit())

    def createFramebufferObject(self, size: QSize) -> QOpenGLFramebufferObject:
        if self._ctx is None:
            from mpvqc.services.player import PlayerService

            player = inject.instance(PlayerService)
            player.init()

            player_properties = QCoreApplication.instance().find_object(QObject, "mpvqcPlayerProperties")
            player_properties.init()

            self._ctx = MpvRenderContext(
                mpv=player.mpv,
                api_type="opengl",
                opengl_init_params={"get_proc_address": self._get_proc_address_resolver},
            )
            self._ctx.update_cb = self._parent.sig_on_update.emit

        return QQuickFramebufferObject.Renderer.createFramebufferObject(self, size)

    def render(self):
        if self._ctx:
            factor: float = self._zoom_detector_service.zoom_factor
            rect = self._parent.size()

            width = int(rect.width() * factor)
            height = int(rect.height() * factor)
            fbo = int(self.framebufferObject().handle())

            self._ctx.render(flip_y=False, opengl_fbo={"w": width, "h": height, "fbo": fbo})
