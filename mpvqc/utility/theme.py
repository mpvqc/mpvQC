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
class MpvqcThemeBackend(QObject):
    _themes = inject.attr(ThemeService)
    _settings = inject.attr(SettingsService)

    themeChanged = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._theme = self._themes.theme(self._settings.theme_identifier)
        self._palette = self._themes.palette_at(self._settings.theme_identifier, self._settings.theme_color_option)
        self._settings.themeIdentifierChanged.connect(self._on_theme_identifier_changed)
        self._settings.themeColorOptionChanged.connect(self._on_color_option_changed)

    @Slot()
    def _on_theme_identifier_changed(self) -> None:
        self._theme = self._themes.theme(self._settings.theme_identifier)
        self._palette = self._themes.palette_at(self._settings.theme_identifier, self._settings.theme_color_option)
        self.themeChanged.emit()

    @Slot()
    def _on_color_option_changed(self) -> None:
        self._palette = self._themes.palette_at(self._settings.theme_identifier, self._settings.theme_color_option)
        self.themeChanged.emit()

    @Property(bool, notify=themeChanged)
    def isDark(self) -> bool:
        return self._theme.is_dark

    @Property(str, notify=themeChanged)
    def background(self) -> str:
        return self._palette.background

    @Property(str, notify=themeChanged)
    def backgroundAlternate(self) -> str:
        return self._palette.background_alternate

    @Property(str, notify=themeChanged)
    def foreground(self) -> str:
        return self._palette.foreground

    @Property(str, notify=themeChanged)
    def foregroundAlternate(self) -> str:
        return self._palette.foreground_alternate

    @Property(str, notify=themeChanged)
    def control(self) -> str:
        return self._palette.control

    @Property(str, notify=themeChanged)
    def rowHighlight(self) -> str:
        return self._palette.row_highlight

    @Property(str, notify=themeChanged)
    def rowHighlightText(self) -> str:
        return self._palette.row_highlight_text

    @Property(str, notify=themeChanged)
    def rowBase(self) -> str:
        return self._palette.row_base

    @Property(str, notify=themeChanged)
    def rowBaseText(self) -> str:
        return self._palette.row_base_text

    @Property(str, notify=themeChanged)
    def rowBaseAlternate(self) -> str:
        return self._palette.row_base_alternate

    @Property(str, notify=themeChanged)
    def rowBaseAlternateText(self) -> str:
        return self._palette.row_base_alternate_text
