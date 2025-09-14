# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QCoreApplication, QObject
from PySide6.QtQml import QmlElement
from PySide6.QtQuick import QQuickWindow

from mpvqc.services import FramelessWindowService, PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyUnresolvedReferences
@QmlElement
class MpvWindowPyObject(QQuickWindow):
    _player: PlayerService = inject.attr(PlayerService)
    _frameless_window: FramelessWindowService = inject.attr(FramelessWindowService)

    def __init__(self):
        super().__init__()
        self._player.init(win_id=self.winId())
        q_app = QCoreApplication.instance()
        q_app.application_ready.connect(lambda: self._on_application_ready())

    def _on_application_ready(self):
        player_properties = QCoreApplication.instance().find_object(QObject, "mpvqcPlayerProperties")
        player_properties.init()

        self._frameless_window.event_filter.set_embedded_player_hwnd(self.winId())
