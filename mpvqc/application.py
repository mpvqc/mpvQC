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

import sys

import inject
from PySide6.QtCore import QUrl, QTranslator, QLocale
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from mpvqc.services import FileStartupService


class MpvqcApplication(QGuiApplication):
    _start_up = inject.attr(FileStartupService)

    def __init__(self, args):
        super().__init__(args)
        self._engine = QQmlApplicationEngine()
        self._translator = QTranslator()

    def set_window_icon(self):
        icon = QIcon(':/data/icon.svg')
        self.setWindowIcon(icon)

    def set_up_internationalization(self):
        self.installTranslator(self._translator)

    def create_directories(self):
        self._start_up.create_missing_directories()
        self._start_up.create_missing_files()

    def set_up_signals(self):
        self.aboutToQuit.connect(self._on_quit)
        self._engine.uiLanguageChanged.connect(self._retranslate)

    def _on_quit(self) -> None:
        del self._engine

    def _retranslate(self):
        locale = QLocale(self._engine.uiLanguage())
        self._translator.load(f':/i18n/{locale.name()}.qm')
        self.setLayoutDirection(locale.textDirection())

    def set_up_imports(self):
        self._engine.addImportPath(':/qml')

    def start_engine(self):
        self._engine.load(QUrl.fromLocalFile(':/qml/main.qml'))

    def verify(self):
        if not self._engine.rootObjects():
            sys.exit(-1)
