# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from functools import cache

import inject
from PySide6.QtCore import Signal
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from mpvqc.services import (
    FileStartupService,
    FontLoaderService,
    FramelessWindowService,
    InternationalizationService,
    SettingsService,
)


class MpvqcApplication(QGuiApplication):
    _start_up: FileStartupService = inject.attr(FileStartupService)
    _font_loader: FontLoaderService = inject.attr(FontLoaderService)
    _frameless_window: FramelessWindowService = inject.attr(FramelessWindowService)
    _i18n: InternationalizationService = inject.attr(InternationalizationService)
    _settings: SettingsService = inject.attr(SettingsService)

    application_ready = Signal(name="applicationReady")

    def __init__(self, args):
        super().__init__(args)
        self._engine = QQmlApplicationEngine()

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
        self._settings.languageChanged.connect(self._engine.setUiLanguage)
        self._engine.uiLanguageChanged.connect(self._retranslate)

    def _on_quit(self) -> None:
        del self._engine

    def _retranslate(self):
        language_code = self._engine.uiLanguage()
        self._i18n.retranslate(app=self, language_code=language_code)

    def load_language(self):
        self._engine.setUiLanguage(self._settings.language)

    def start_engine(self):
        self._engine.loadFromModule("app", "MpvqcApplication")

    def notify_ready(self):
        if not self._engine.rootObjects():
            sys.exit(-1)
        self.application_ready.emit()

    def configure_frameless_window(self):
        window = self.topLevelWindows()[0]
        self._frameless_window.configure_for(self, window)

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
