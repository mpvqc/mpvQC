# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import platform

from PySide6.QtGui import QGuiApplication, QWindow


class FramelessWindowService:
    """Service for managing frameless window behavior across different platforms."""

    def __init__(self):
        if platform.system() == "Windows":
            self._initialize_windows_filter()

    def _initialize_windows_filter(self) -> None:
        from mpvqc.services.frameless.win import WindowsEventFilter

        # We need a reference to this filter as soon as possible
        # Needs to bound to a class variable, else garbage collector will clean up immediately
        self._event_filter = WindowsEventFilter()

    @property
    def event_filter(self):
        return self._event_filter

    def configure_for(self, app: QGuiApplication, top_lvl_window: QWindow) -> None:
        match platform.system():
            case "Windows":
                self._configure_for_windows(app, top_lvl_window)
            case "Linux":
                self._configure_for_linux(app, top_lvl_window)
            case system:
                msg = f"Cannot configure frameless window on platform: {system}"
                raise ValueError(msg)

    def _configure_for_windows(self, app: QGuiApplication, window: QWindow) -> None:
        from mpvqc.services.frameless.win import (
            configure_gwl_style,
            extend_frame_into_client_area,
            set_outer_window_size,
        )

        hwnd_top_lvl = window.winId()
        self._event_filter.set_top_lvl_hwnd(hwnd_top_lvl)
        app.installNativeEventFilter(self._event_filter)

        extend_frame_into_client_area(hwnd_top_lvl)
        configure_gwl_style(hwnd_top_lvl)
        set_outer_window_size(hwnd_top_lvl, 1280, 720)

    def _configure_for_linux(self, app: QGuiApplication, window: QWindow) -> None:
        from mpvqc.services.frameless.linux import LinuxEventFilter

        self._event_filter = LinuxEventFilter(window, app)
        app.installEventFilter(self._event_filter)
