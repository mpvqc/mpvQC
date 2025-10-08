# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import SettingsService, ThemeService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcAppearanceDialogViewModel(QObject):
    _themes: ThemeService = inject.attr(ThemeService)
    _settings: SettingsService = inject.attr(SettingsService)

    themeIndexChanged = Signal(int)
    colorIndexChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._original_theme_identifier = self._settings.theme_identifier
        self._original_theme_color_option = self._settings.theme_color_option
        self._theme_index = self._themes.index(self._settings.theme_identifier)
        self._color_index = self._settings.theme_color_option

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
    def setTheme(self, identifier: str) -> None:
        new_index = self._themes.index(identifier)
        self._set_theme_index(new_index)
        self._settings.theme_identifier = identifier

    @Slot(int)
    def setColorOption(self, index: int) -> None:
        self._set_color_index(index)
        self._settings.theme_color_option = index

    @Slot()
    def reject(self):
        self._settings.theme_identifier = self._original_theme_identifier
        self._settings.theme_color_option = self._original_theme_color_option
