# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import time
from collections.abc import Callable

from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView


class SplashScreen:
    def __init__(self, app: QGuiApplication):
        self._app = app
        self._splash_view: QQuickView | None = None
        self._splash_start_time: float | None = None
        self._min_display_time_ms = 1500

    def show(self) -> None:
        self._splash_view = QQuickView()
        self._splash_view.setFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)
        self._splash_view.setSource(QUrl.fromLocalFile(":/qt/qml/MpvqcSplashScreen.qml"))

        # Center on screen
        screen_geometry = self._app.primaryScreen().geometry()
        x = (screen_geometry.width() - 400) // 2
        y = (screen_geometry.height() - 300) // 2
        self._splash_view.setGeometry(x, y, 400, 300)

        self._splash_view.show()
        self._app.processEvents()
        self._splash_start_time = time.time()

    def close(self, on_closed: Callable = None) -> None:
        if self._splash_view is None:
            if on_closed:
                on_closed()
            return

        elapsed_ms = int(time.time() - self._splash_start_time) * 1000
        remaining_ms = max(0, self._min_display_time_ms - elapsed_ms)

        def _close_splash():
            if self._splash_view is not None:
                self._splash_view.close()
                del self._splash_view
                self._splash_view = None
            if on_closed:
                on_closed()

        if remaining_ms > 0:
            QTimer.singleShot(int(remaining_ms), _close_splash)
        else:
            _close_splash()
