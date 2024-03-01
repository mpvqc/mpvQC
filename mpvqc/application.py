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
from PySide6.QtCore import QUrl, QTranslator, QLocale, QLibraryInfo
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from mpvqc.services import FileStartupService, FontLoaderService


class MpvqcApplication(QGuiApplication):
    _start_up: FileStartupService = inject.attr(FileStartupService)
    _font_loader: FontLoaderService = inject.attr(FontLoaderService)

    def __init__(self, args):
        super().__init__(args)
        self._engine = QQmlApplicationEngine()
        self._translator_mpvqc = QTranslator()
        self._translator_qt = QTranslator()

    @cache
    def find_object(self, object_type, name: str):
        root = self._engine.rootObjects()
        assert root, "Cannot find root object in QQmlApplicationEngine"
        obj = root[0].findChild(object_type, name)
        assert obj, f"Cannot find {object_type} with name '{name}'"
        return obj

    def set_window_icon(self):
        icon = QIcon(':/data/icon.svg')
        self.setWindowIcon(icon)

    def load_application_fonts(self):
        self._font_loader.load_application_fonts()

    def create_directories(self):
        self._start_up.create_missing_directories()
        self._start_up.create_missing_files()

    def _change_language(self, target_locale: str) -> None:
        self._engine.setUiLanguage(target_locale)
        self._retranslate()

    def set_up_signals(self):
        self.aboutToQuit.connect(self._on_quit)
        self._engine.uiLanguageChanged.connect(self._retranslate)

    def _on_quit(self) -> None:
        del self._engine

    def _retranslate(self):
        self.removeTranslator(self._translator_qt)
        self.removeTranslator(self._translator_mpvqc)

        identifier = self._engine.uiLanguage()
        locale = QLocale(identifier)

        self._translator_qt.load(locale, "qtbase", "_", QLibraryInfo.location(QLibraryInfo.TranslationsPath))
        self._translator_mpvqc.load(f':/i18n/{identifier}.qm')

        self.installTranslator(self._translator_qt)
        self.installTranslator(self._translator_mpvqc)

        self.setLayoutDirection(locale.textDirection())

    def set_up_imports(self):
        self._engine.addImportPath(':/qml')

    def install_window_event_filter(self):
        if sys.platform == 'win32':
            from mpvqc.framelesswindow.win import WindowsEventFilter
            self._event_filter = WindowsEventFilter(border_width=6)
            self.installNativeEventFilter(self._event_filter)
        elif sys.platform == 'linux':
            from mpvqc.framelesswindow.linux import LinuxEventFilter
            self._event_filter = LinuxEventFilter(border_width=6)
            self.installEventFilter(self._event_filter)

    def start_engine(self):
        self._engine.load(QUrl.fromLocalFile(':/qml/main.qml'))

    def add_window_effects(self):
        if sys.platform == 'win32':
            hwnd = self.topLevelWindows()[0].winId()
            from mpvqc.framelesswindow.win import WindowsWindowEffect
            self._effects = WindowsWindowEffect()
            self._effects.addShadowEffect(hwnd)
            self._effects.addWindowAnimation(hwnd)

    def verify(self):
        if not self._engine.rootObjects():
            sys.exit(-1)
