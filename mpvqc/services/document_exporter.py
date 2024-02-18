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

from pathlib import Path
from typing import Optional

import inject
from PySide6.QtGui import QGuiApplication, QStandardItemModel
from PySide6.QtWidgets import QApplication

from .player import PlayerService
from .settings import SettingsService


def _find_comment_model_in_object_tree():
    engine = QGuiApplication.instance().engine
    assert engine, "Cannot find QQmlApplicationEngine in QGuiApplication.instance()"
    root = engine.rootObjects()
    assert root, "Cannot find root object in QQmlApplicationEngine"
    model = root[0].findChild(QStandardItemModel, "mpvqcCommentModel")
    assert model, "Cannot find comment model in root object"
    return model


class DocumentExporterService:
    _settings: SettingsService = inject.attr(SettingsService)
    _player: PlayerService = inject.attr(PlayerService)

    def __init__(self):
        from mpvqc.pyobjects import MpvqcCommentModelPyObject
        self._comment_model: Optional[MpvqcCommentModelPyObject] = None

    @property
    def _comments(self):
        if self._comment_model is None:
            self._comment_model = _find_comment_model_in_object_tree()
        return self._comment_model.comments()

    def write(self) -> str:
        for comment in self._comments:
            print("py: comment", comment)

        print("py: writeHeaderDate:", self._settings.writeHeaderDate)
        print("py: writeHeaderGenerator:", self._settings.writeHeaderGenerator)
        print("py: writeHeaderVideoPath:", self._settings.writeHeaderVideoPath)
        print("py: writeHeaderNickname:", self._settings.writeHeaderNickname)

        print("py: nickname:", self._settings.nickname)
        print("py: generator:", f"{QApplication.applicationName()} {QApplication.applicationVersion()}")
        print("py: video:", Path(self._player.mpv.path) if self._player.mpv.path else "")

        return 'return value'
