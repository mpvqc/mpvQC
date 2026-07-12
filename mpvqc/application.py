# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import QUrl, Slot
from PySide6.QtGui import QGuiApplication, QIcon, QWindow
from PySide6.QtQml import QQmlApplicationEngine

from mpvqc.close_event_filter import CloseEventFilter
from mpvqc.services import (
    BuildInfoService,
    FileStartupService,
    FontLoaderService,
    InternationalizationService,
    MainWindowService,
    PlatformService,
    SettingsService,
)

if TYPE_CHECKING:
    from collections.abc import Sequence


class MpvqcApplication(QGuiApplication):
    _build_info = inject.attr(BuildInfoService)
    _start_up = inject.attr(FileStartupService)
    _font_loader = inject.attr(FontLoaderService)
    _i18n = inject.attr(InternationalizationService)
    _main_window = inject.attr(MainWindowService)
    _platform = inject.attr(PlatformService)
    _settings = inject.attr(SettingsService)

    def __init__(self, arguments: Sequence[str]) -> None:
        super().__init__(arguments)
        self._close_event_filter = CloseEventFilter()
        self._engine = QQmlApplicationEngine()

    def configure(self) -> None:
        self._set_window_icon()

        self._font_loader.load_application_fonts()

        self._start_up.create_missing_directories()
        self._start_up.create_missing_files()

        self.aboutToQuit.connect(self._on_quit)

        language = self._settings.language
        self._i18n.retranslate(app=self, language_code=language)
        self._engine.setUiLanguage(language)

        self._settings.language_changed.connect(self._on_language_changed)
        self._engine.uiLanguageChanged.connect(self._retranslate)

    def _set_window_icon(self) -> None:
        # On some desktop environments, providing the icon via theme makes them prefer the SVG over a rasterized snapshot.
        # Falls back to the bundled file where the theme lookup misses (non-Linux, dev runs).
        icon = QIcon.fromTheme(self._build_info.app_id, QIcon(":/data/icon.svg"))
        self.setWindowIcon(icon)

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
        url = QUrl(self._platform.root_qml_url)
        self._engine.load(url)

        root_objects = self._engine.rootObjects()
        if not root_objects:
            sys.exit(-1)

        root_window = root_objects[0]
        if not isinstance(root_window, QWindow):
            sys.exit(-1)

        self._main_window.initialize(root_window)
        self._main_window.install_event_filter(self._close_event_filter)

        remove_nuitka_splash_screen()
        self._main_window.show()


def remove_nuitka_splash_screen() -> None:
    parent_pid = os.environ.get("NUITKA_ONEFILE_PARENT")
    if parent_pid is None:
        return

    splash_filename = Path(tempfile.gettempdir()) / f"onefile_{parent_pid}_splash_feedback.tmp"

    if splash_filename.exists():
        splash_filename.unlink()
