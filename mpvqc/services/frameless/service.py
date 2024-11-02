# Copyright 2024
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys

from PySide6.QtGui import QGuiApplication, QWindow


class FramelessWindowService:
    _event_filter = None

    def __init__(self):
        if sys.platform == "win32":
            from mpvqc.services.frameless.win import WindowsEventFilter

            # We need a reference to this filter as soon as possible
            # Needs to bound to a class variable, else garbage collector will clean up immediately
            self._event_filter = WindowsEventFilter()

    def configure_for(self, app: QGuiApplication, top_lvl_window: QWindow):
        def configure_for_linux():
            from .linux import LinuxEventFilter

            # Needs to bound to a class variable, else garbage collector will clean up immediately
            self._event_filter = LinuxEventFilter(top_lvl_window, app)
            app.installEventFilter(self._event_filter)

        def configure_for_windows():
            from .win import configure_gwl_style, extend_frame_into_client_area

            app.installNativeEventFilter(self._event_filter)

            hwnd_top_lvl = top_lvl_window.winId()
            extend_frame_into_client_area(hwnd_top_lvl)
            configure_gwl_style(hwnd_top_lvl)

        if sys.platform == "win32":
            configure_for_windows()
        elif sys.platform == "linux":
            configure_for_linux()
        else:
            raise ValueError(f"Unsupported platform: {sys.platform}")

    def ignore_events_for(self, hwnd):
        if sys.platform == "win32":
            self._event_filter.ignore_native_events_for(hwnd)
        else:
            raise ValueError(f"Operation not supported on platform: {sys.platform}")
