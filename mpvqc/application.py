# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import Qt, QUrl, Signal, Slot
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickWindow

from mpvqc.build import get_build_info
from mpvqc.close_event_filter import CloseEventFilter
from mpvqc.services import (
    FileStartupService,
    FontLoaderService,
    InternationalizationService,
    SettingsService,
)
from mpvqc.window.services import MainWindowService

if TYPE_CHECKING:
    from collections.abc import Sequence

_ROOT_QML_URL = "qrc:/qt/qml/MpvqcApplication.qml"


class MpvqcApplication(QGuiApplication):
    _start_up = inject.attr(FileStartupService)
    _font_loader = inject.attr(FontLoaderService)
    _i18n = inject.attr(InternationalizationService)
    _main_window = inject.attr(MainWindowService)
    _settings = inject.attr(SettingsService)

    about_to_show = Signal()
    first_frame_rendered = Signal()

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
        icon = QIcon.fromTheme(get_build_info().app_id, QIcon(":/data/icon.svg"))
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
        self._engine.load(QUrl(_ROOT_QML_URL))

        root_objects = self._engine.rootObjects()
        if not root_objects:
            sys.exit(-1)

        root_window = root_objects[0]
        if not isinstance(root_window, QQuickWindow):
            sys.exit(-1)

        self._main_window.initialize(root_window)
        self._main_window.install_event_filter(self._close_event_filter)

        self._announce_first_frame(root_window)

        self.about_to_show.emit()
        self._main_window.show()

    def _announce_first_frame(self, window: QQuickWindow) -> None:
        # frameSwapped is emitted from the render thread; a queued connection moves delivery to the GUI thread.
        connection_type = Qt.ConnectionType(
            Qt.ConnectionType.QueuedConnection.value | Qt.ConnectionType.SingleShotConnection.value
        )
        window.frameSwapped.connect(self.first_frame_rendered, connection_type)
