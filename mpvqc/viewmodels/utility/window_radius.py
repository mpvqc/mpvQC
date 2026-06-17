# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services import MainWindowService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1

_WINDOW_RADIUS = 8


@QmlElement
class MpvqcWindowRadiusViewModel(QObject):
    _main_window = inject.attr(MainWindowService)

    radiusChanged = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._main_window.shadow_margin_changed.connect(self.radiusChanged)

    @Property(int, notify=radiusChanged)
    def radius(self) -> int:
        # Rounded only while we draw our own shadow and the window floats free. The
        # shadow margin is already 0 on Windows, tiling WMs, maximized and fullscreen.
        return _WINDOW_RADIUS if self._main_window.shadow_margin > 0 else 0
