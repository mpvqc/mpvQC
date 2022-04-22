#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys

import inject
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from mpvqc.services import FileStartupService, TranslationService


class MpvqcApplication(QGuiApplication):
    _start_up = inject.attr(FileStartupService)
    _translator = inject.attr(TranslationService)

    def __init__(self, args):
        super().__init__(args)
        self._engine = QQmlApplicationEngine()

    def set_window_icon(self):
        icon = QIcon(':/data/icon.svg')
        self.setWindowIcon(icon)

    def initialize_translator(self):
        self._translator.initialize_with(application=self, engine=self._engine)

    def create_directories(self):
        self._start_up.create_missing_directories()
        self._start_up.create_missing_files()

    def set_up_signals(self):
        self.aboutToQuit.connect(self._on_quit)

    def _on_quit(self) -> None:
        del self._engine

    def set_up_imports(self):
        self._engine.addImportPath(':/qml')

    def start_engine(self):
        self._engine.load(QUrl.fromLocalFile(':/qml/main.qml'))

    def verify(self):
        if not self._engine.rootObjects():
            sys.exit(-1)
