# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import QDir, Qt, QUrl, Signal, Slot
from PySide6.QtGui import QFontDatabase, QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickWindow

from mpvqc.appdata.services import ApplicationPathsService, prepare_app_data
from mpvqc.build import get_build_info
from mpvqc.i18n.services import I18nSettingsService, InternationalizationService
from mpvqc.shell.services import QuitService
from mpvqc.window.services import MainWindowService

if TYPE_CHECKING:
    from collections.abc import Sequence

_ROOT_QML_URL = "qrc:/qt/qml/MpvqcApplication.qml"


def _load_application_fonts() -> None:
    for entry_info in QDir(":/data/fonts").entryInfoList():
        resource_path = entry_info.filePath()
        if QFontDatabase.addApplicationFont(resource_path) == -1:
            msg = f"Cannot load font from {resource_path}"
            raise ValueError(msg)


class MpvqcApplication(QGuiApplication):
    _paths = inject.attr(ApplicationPathsService)
    _i18n = inject.attr(InternationalizationService)
    _i18n_settings = inject.attr(I18nSettingsService)
    _main_window = inject.attr(MainWindowService)
    _quit = inject.attr(QuitService)

    about_to_show = Signal()
    first_frame_rendered = Signal()

    def __init__(self, arguments: Sequence[str]) -> None:
        super().__init__(arguments)
        self._engine = QQmlApplicationEngine()

    def configure(self) -> None:
        self._set_window_icon()

        _load_application_fonts()

        prepare_app_data(self._paths)

        self.aboutToQuit.connect(self._on_quit)

        language = self._i18n_settings.language
        self._i18n.retranslate(app=self, language_code=language)
        self._engine.setUiLanguage(language)

        self._i18n_settings.language_changed.connect(self._on_language_changed)
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
        self._quit.attach(root_window)

        self._announce_first_frame(root_window)

        self.about_to_show.emit()
        self._main_window.show()

    def _announce_first_frame(self, window: QQuickWindow) -> None:
        # frameSwapped is emitted from the render thread; a queued connection moves delivery to the GUI thread.
        connection_type = Qt.ConnectionType(
            Qt.ConnectionType.QueuedConnection.value | Qt.ConnectionType.SingleShotConnection.value
        )
        window.frameSwapped.connect(self.first_frame_rendered, connection_type)
