# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys
import tempfile
from functools import cache
from pathlib import Path

import inject
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from mpvqc.services import (
    FileStartupService,
    FontLoaderService,
    FramelessWindowService,
    InternationalizationService,
    SettingsService,
)
from mpvqc.utility import CloseEventFilter, get_main_window


class MpvqcApplication(QGuiApplication):
    _start_up: FileStartupService = inject.attr(FileStartupService)
    _font_loader: FontLoaderService = inject.attr(FontLoaderService)
    _frameless_window: FramelessWindowService = inject.attr(FramelessWindowService)
    _i18n: InternationalizationService = inject.attr(InternationalizationService)
    _settings: SettingsService = inject.attr(SettingsService)

    def __init__(self, args):
        super().__init__(args)
        self._close_event_filter = CloseEventFilter()
        self._engine = QQmlApplicationEngine()
        self._engine.addImportPath(":/qt/qml/styles")

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

    def _on_quit(self) -> None:
        del self._engine

    def configure_i18n(self):
        language = self._settings.language
        self._i18n.retranslate(app=self, language_code=language)
        self._engine.setUiLanguage(language)

        self._settings.languageChanged.connect(self._engine.setUiLanguage)
        self._engine.uiLanguageChanged.connect(self._retranslate)

    def _retranslate(self):
        language_code = self._engine.uiLanguage()
        self._i18n.retranslate(app=self, language_code=language_code)

    def start_engine(self):
        url = QUrl.fromLocalFile(":/qt/qml/MpvqcApplication.qml")
        self._engine.load(url)

        if not self._engine.rootObjects():
            sys.exit(-1)

    def configure_window(self):
        window = get_main_window()
        self._frameless_window.configure_for(self, window)
        window.installEventFilter(self._close_event_filter)

    def show(self):
        remove_nuitka_splash_screen()
        get_main_window().setVisible(True)

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


def remove_nuitka_splash_screen() -> None:
    parent_pid = os.environ.get("NUITKA_ONEFILE_PARENT")
    if parent_pid is None:
        return

    splash_filename = Path(tempfile.gettempdir()) / f"onefile_{parent_pid}_splash_feedback.tmp"

    if splash_filename.exists():
        splash_filename.unlink()
