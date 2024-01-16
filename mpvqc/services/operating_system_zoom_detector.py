import os
import sys

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QGuiApplication


def _detect_operating_system_zoom_factor() -> float:
    if sys.platform == 'win32':
        return _figure_out_zoom_factor_on_windows()
    else:
        return _figure_out_zoom_factor_on_linux()


def _figure_out_zoom_factor_on_windows() -> float:
    import ctypes
    import win32api

    def currentMonitorHandle():
        hwnd = QGuiApplication.topLevelWindows()[0].winId()
        return ctypes.windll.user32.MonitorFromWindow(ctypes.wintypes.HWND(hwnd), ctypes.wintypes.DWORD(2))

    def monitors_to_dpi_mapping() -> dict[int, int]:
        MDT_EFFECTIVE_DPI = 0

        dpi_x = ctypes.c_uint()
        dpi_y = ctypes.c_uint()

        monitors = {}

        for i, monitor in enumerate(win32api.EnumDisplayMonitors()):
            ctypes.windll.shcore.GetDpiForMonitor(
                monitor[0].handle,
                MDT_EFFECTIVE_DPI,
                ctypes.byref(dpi_x),
                ctypes.byref(dpi_y)
            )
            monitor_handle = int(monitor[0])
            monitors[monitor_handle] = dpi_x.value

        return monitors

    monitor_to_dpi_mapping = monitors_to_dpi_mapping()
    current_monitor = currentMonitorHandle()

    dpi = monitor_to_dpi_mapping[current_monitor]

    return dpi / 96


def _figure_out_zoom_factor_on_linux() -> float:
    # Assume that people who use linux are fine with setting it this way
    # until there's an official way of figuring this out

    default_factor = 1.0

    try:
        factor = os.getenv("MPVQC_VIDEO_SCALING_FACTOR", default_factor)
        return float(factor)
    except:
        return default_factor


class OperatingSystemZoomDetectorService(QObject):
    primaryScreenChanged = QGuiApplication.primaryScreenChanged

    zoom_factor_changed = Signal(float)

    def __init__(self):
        super().__init__()
        self._zoom_factor = None
        QGuiApplication.topLevelWindows()[0].screenChanged.connect(self._invalidate_zoom_factor)

    def _invalidate_zoom_factor(self, *_):
        self._zoom_factor = _detect_operating_system_zoom_factor()
        self.zoom_factor_changed.emit(self._zoom_factor)

    @property
    def zoom_factor(self):
        if self._zoom_factor is None:
            self._invalidate_zoom_factor()
        return self._zoom_factor
