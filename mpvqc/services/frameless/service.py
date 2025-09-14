# Copyright 2024
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

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

    @property
    def event_filter(self):
        return self._event_filter

    def configure_for(self, app: QGuiApplication, top_lvl_window: QWindow):
        def configure_for_linux():
            from .linux import LinuxEventFilter

            # Needs to bound to a class variable, else garbage collector will clean up immediately
            self._event_filter = LinuxEventFilter(top_lvl_window, app)
            app.installEventFilter(self._event_filter)

        def configure_for_windows():
            hwnd_top_lvl = top_lvl_window.winId()
            self._event_filter.set_top_lvl_hwnd(hwnd_top_lvl)

            app.installNativeEventFilter(self._event_filter)

            from .win import configure_gwl_style, extend_frame_into_client_area, set_outer_window_size

            extend_frame_into_client_area(hwnd_top_lvl)
            configure_gwl_style(hwnd_top_lvl)
            set_outer_window_size(hwnd_top_lvl, 1280, 720)

        if sys.platform == "win32":
            configure_for_windows()
        elif sys.platform == "linux":
            configure_for_linux()
        else:
            msg = f"Unsupported platform: {sys.platform}"
            raise ValueError(msg)
