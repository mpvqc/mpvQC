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


import ctypes


class GetProcAddressGetter:
    """ fixme: Class gets obsolete once https://bugreports.qt.io/browse/PYSIDE-971 gets fixed """

    def __init__(self):
        self._func = self._find_platform_wrapper()

    def _find_platform_wrapper(self):
        try:
            from OpenGL import WGL
            return self._wgl_impl
        except AttributeError:
            pass
        try:
            from OpenGL import GLX
            return self._glx_impl
        except AttributeError:
            pass
        try:
            from OpenGL import EGL
            return self._egl_impl
        except AttributeError:
            pass
        try:
            from OpenGL import GLUT
            return self._glut_impl
        except AttributeError:
            pass
        raise NotImplementedError("Platform not supported. Supported platforms are: WGL, GLX, EGL, and GLUT")

    def wrap(self, _, name: bytes):
        address = self._func(name)
        return ctypes.cast(address, ctypes.c_void_p).value

    @staticmethod
    def _wgl_impl(name: bytes):
        from OpenGL import WGL
        return WGL.wglGetProcAddress(name)

    @staticmethod
    def _glx_impl(name: bytes):
        from OpenGL import GLX
        return GLX.glXGetProcAddress(name.decode("utf-8"))

    @staticmethod
    def _egl_impl(name: bytes):
        from OpenGL import EGL
        return EGL.eglGetProcAddress(name.decode("utf-8"))

    @staticmethod
    def _glut_impl(name: bytes):
        from OpenGL import GLUT
        return GLUT.glutGetProcAddress(name.decode("utf-8"))
