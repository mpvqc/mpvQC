#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import inject
from PySide6.QtCore import QSize
from PySide6.QtOpenGL import QOpenGLFramebufferObject
from PySide6.QtQuick import QQuickFramebufferObject

from .address_proc_getter import GetProcAddressGetter
from .mpv import OpenGlCbGetProcAddrFn, MpvRenderContext


class PlayerRenderer(QQuickFramebufferObject.Renderer):
    """"""

    def __init__(self, parent):
        super(PlayerRenderer, self).__init__()
        self._parent = parent
        self._get_proc_address_resolver = OpenGlCbGetProcAddrFn(GetProcAddressGetter().wrap)
        self._ctx = None

        from mpvqc.services.player import PlayerService
        self._player_service = inject.instance(PlayerService)

    def createFramebufferObject(self, size: QSize) -> QOpenGLFramebufferObject:
        if self._ctx is None:
            self._ctx = MpvRenderContext(
                self._player_service.mpv,
                api_type='opengl',
                opengl_init_params={'get_proc_address': self._get_proc_address_resolver}
            )
            self._ctx.update_cb = self._parent.sig_on_update.emit

        return QQuickFramebufferObject.Renderer.createFramebufferObject(self, size)

    def render(self):
        if self._ctx:
            factor = self._parent.scale()
            rect = self._parent.size()

            width = int(rect.width() * factor)
            height = int(rect.height() * factor)
            fbo = int(self.framebufferObject().handle())

            self._ctx.render(flip_y=False, opengl_fbo={'w': width, 'h': height, 'fbo': fbo})
