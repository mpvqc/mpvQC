# mpvQC
#
# Copyright (C) 2022 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
