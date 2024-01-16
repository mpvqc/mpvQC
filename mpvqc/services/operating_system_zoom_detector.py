import os
import sys

from PySide6.QtCore import QObject
from PySide6.QtGui import QGuiApplication


def _detect_operating_system_zoom_factor() -> float:
    if sys.platform == 'win32':
        return _figure_out_zoom_factor_on_windows()
    else:
        return _figure_out_zoom_factor_on_linux()


def _figure_out_zoom_factor_on_windows() -> float:
    # todo implement
    return 1.0


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

    def __init__(self):
        super().__init__()
        self._zoom_factor = None
        QGuiApplication.topLevelWindows()[0].screenChanged.connect(_detect_operating_system_zoom_factor)

    @property
    def zoom_factor(self):
        if self._zoom_factor is None:
            self._zoom_factor = _detect_operating_system_zoom_factor()
        return self._zoom_factor
