# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import ctypes

import win32api

from mpvqc.utility import get_main_window

from .types import DEFAULT_WINDOW_BUTTON_PREFERENCE, OsBackend, WindowButtonPreference


class WindowsBackend(OsBackend):
    def get_display_zoom_factor(self) -> float:
        def current_monitor_handle():
            hwnd = get_main_window().winId()
            return ctypes.windll.user32.MonitorFromWindow(ctypes.wintypes.HWND(hwnd), ctypes.wintypes.DWORD(2))

        def monitors_to_dpi_mapping() -> dict[int, int]:
            MDT_EFFECTIVE_DPI = 0

            dpi_x = ctypes.c_uint()
            dpi_y = ctypes.c_uint()

            monitors = {}

            for i, monitor in enumerate(win32api.EnumDisplayMonitors()):
                ctypes.windll.shcore.GetDpiForMonitor(
                    monitor[0].handle, MDT_EFFECTIVE_DPI, ctypes.byref(dpi_x), ctypes.byref(dpi_y)
                )
                monitor_handle = int(monitor[0])
                monitors[monitor_handle] = dpi_x.value

            return monitors

        monitor_to_dpi_mapping = monitors_to_dpi_mapping()
        current_monitor = current_monitor_handle()

        dpi = monitor_to_dpi_mapping[current_monitor]

        return dpi / 96

    def get_window_button_preference(self) -> WindowButtonPreference:
        return DEFAULT_WINDOW_BUTTON_PREFERENCE
