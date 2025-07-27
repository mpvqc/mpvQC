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

import sys
from functools import cache

import inject
from PySide6.QtCore import QUrl, Signal
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from mpvqc.services import FileStartupService, FontLoaderService, FramelessWindowService, InternationalizationService


class MpvqcApplication(QGuiApplication):
    _start_up: FileStartupService = inject.attr(FileStartupService)
    _font_loader: FontLoaderService = inject.attr(FontLoaderService)
    _frameless_window: FramelessWindowService = inject.attr(FramelessWindowService)
    _i18n: InternationalizationService = inject.attr(InternationalizationService)

    application_ready = Signal(name="applicationReady")

    def __init__(self, args):
        super().__init__(args)
        self._engine = QQmlApplicationEngine()

    @cache
    def find_object(self, object_type, name: str):
        root = self._engine.rootObjects()
        if not root:
            msg = "Cannot find root object in QQmlApplicationEngine"
            raise ValueError(msg)
        obj = root[0].findChild(object_type, name)
        if not obj:
            msg = f"Cannot find {object_type} with name '{name}'"
            raise ValueError(msg)
        return obj

    def set_window_icon(self):
        icon = QIcon(":/data/icon.svg")
        self.setWindowIcon(icon)

    def load_application_fonts(self):
        self._font_loader.load_application_fonts()

    def create_directories(self):
        self._start_up.create_missing_directories()
        self._start_up.create_missing_files()

    def set_up_signals(self):
        self.aboutToQuit.connect(self._on_quit)
        self._engine.uiLanguageChanged.connect(self._retranslate)

    def _on_quit(self) -> None:
        del self._engine

    def _retranslate(self):
        language_code = self._engine.uiLanguage()
        self._i18n.retranslate(app=self, language_code=language_code)

    def start_engine(self):
        url = QUrl.fromLocalFile(":/qt/qml/Main.qml")
        self._engine.load(url)

    def notify_ready(self):
        if not self._engine.rootObjects():
            sys.exit(-1)
        self.application_ready.emit()

    def configure_frameless_window(self):
        window = self.topLevelWindows()[0]
        self._frameless_window.configure_for(self, window)
