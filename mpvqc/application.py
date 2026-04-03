# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys
import tempfile
from pathlib import Path

import inject
from PySide6.QtCore import QUrl, Slot
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from mpvqc.services import (
    FileStartupService,
    FontLoaderService,
    FramelessWindowService,
    InternationalizationService,
    MainWindowService,
    SettingsService,
)
from mpvqc.utility import CloseEventFilter


class MpvqcApplication(QGuiApplication):
    _start_up = inject.attr(FileStartupService)
    _font_loader = inject.attr(FontLoaderService)
    _frameless_window = inject.attr(FramelessWindowService)
    _i18n = inject.attr(InternationalizationService)
    _main_window = inject.attr(MainWindowService)
    _settings = inject.attr(SettingsService)

    def __init__(self, args) -> None:
        super().__init__(args)
        self._close_event_filter = CloseEventFilter()
        self._engine = QQmlApplicationEngine()
        self._engine.addImportPath(":/qt/qml/styles")

    def configure(self) -> None:
        icon = QIcon(":/data/icon.svg")
        self.setWindowIcon(icon)

        self._font_loader.load_application_fonts()

        self._start_up.create_missing_directories()
        self._start_up.create_missing_files()

        self.aboutToQuit.connect(self._on_quit)

        language = self._settings.language
        self._i18n.retranslate(app=self, language_code=language)
        self._engine.setUiLanguage(language)

        self._settings.languageChanged.connect(self._on_language_changed)
        self._engine.uiLanguageChanged.connect(self._retranslate)

    @Slot()
    def _on_quit(self) -> None:
        del self._engine

    @Slot(str)
    def _on_language_changed(self, language: str) -> None:
        self._engine.setUiLanguage(language)

    @Slot()
    def _retranslate(self) -> None:
        language_code = self._engine.uiLanguage()
        self._i18n.retranslate(app=self, language_code=language_code)

    def start(self) -> None:
        url = QUrl.fromLocalFile(":/qt/qml/MpvqcApplication.qml")
        self._engine.load(url)

        if not self._engine.rootObjects():
            sys.exit(-1)

        window = self._main_window.window
        self._frameless_window.configure_for(self, window)
        window.installEventFilter(self._close_event_filter)

        remove_nuitka_splash_screen()
        window.setVisible(True)


def remove_nuitka_splash_screen() -> None:
    parent_pid = os.environ.get("NUITKA_ONEFILE_PARENT")
    if parent_pid is None:
        return

    splash_filename = Path(tempfile.gettempdir()) / f"onefile_{parent_pid}_splash_feedback.tmp"

    if splash_filename.exists():
        splash_filename.unlink()
