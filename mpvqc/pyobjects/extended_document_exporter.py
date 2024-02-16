#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


from pathlib import Path

import inject
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement
from PySide6.QtWidgets import QApplication

from mpvqc.services import SettingsService, PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcExtendedDocumentExporterPyObject(QObject):
    _settings: SettingsService = inject.attr(SettingsService)
    _player: PlayerService = inject.attr(PlayerService)

    @Slot(list, result=str)
    def create_file_content(self, comments: list) -> str:
        for comment in comments:
            print("py: comment", comment)

        print("py: writeHeaderDate:", self._settings.writeHeaderDate)
        print("py: writeHeaderGenerator:", self._settings.writeHeaderGenerator)
        print("py: writeHeaderVideoPath:", self._settings.writeHeaderVideoPath)
        print("py: writeHeaderNickname:", self._settings.writeHeaderNickname)

        print("py: nickname:", self._settings.nickname)
        print("py: generator:", f"{QApplication.applicationName()} {QApplication.applicationVersion()}")
        print("py: video:", Path(self._player.mpv.path) if self._player.mpv.path else "")

        return 'return value'
