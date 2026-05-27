# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import SettingsService, ThemeService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcAppearanceDialogViewModel(QObject):
    _themes = inject.attr(ThemeService)
    _settings = inject.attr(SettingsService)

    themeIndexChanged = Signal(int)
    colorIndexChanged = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._original_theme_identifier = self._settings.theme_identifier
        self._original_primary_color = self._settings.primary_color
        self._theme_index = self._themes.theme_index()
        self._color_index = self._themes.theme().palette_index(self._settings.primary_color)
        self._settings.theme_identifier_changed.connect(self._on_theme_identifier_changed)

    @Property(int, notify=themeIndexChanged)
    def themeIndex(self) -> int:
        return self._theme_index

    def _set_theme_index(self, value: int) -> None:
        if self._theme_index != value:
            self._theme_index = value
            self.themeIndexChanged.emit(value)

    @Property(int, notify=colorIndexChanged)
    def colorIndex(self) -> int:
        return self._color_index

    def _set_color_index(self, value: int) -> None:
        if self._color_index != value:
            self._color_index = value
            self.colorIndexChanged.emit(value)

    @Slot(str)
    def _on_theme_identifier_changed(self, theme_identifier: str) -> None:
        new_index = self._themes.theme(theme_identifier).palette_index(self._settings.primary_color)
        self._set_color_index(new_index)

    @Slot(str)
    def setTheme(self, theme_identifier: str) -> None:
        new_index = self._themes.theme_index(theme_identifier)
        self._set_theme_index(new_index)
        self._settings.theme_identifier = theme_identifier

    @Slot(str)
    def setPrimaryColor(self, identifier: str) -> None:
        new_index = self._themes.theme().palette_index(identifier)
        self._set_color_index(new_index)
        self._settings.primary_color = identifier

    @Slot()
    def reject(self) -> None:
        self._settings.theme_identifier = self._original_theme_identifier
        self._settings.primary_color = self._original_primary_color
