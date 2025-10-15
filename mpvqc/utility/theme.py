# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services import SettingsService, ThemeService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcThemeBackend(QObject):
    _themes: ThemeService = inject.attr(ThemeService)
    _settings: SettingsService = inject.attr(SettingsService)

    themeChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings.themeIdentifierChanged.connect(self.themeChanged)
        self._settings.themeColorOptionChanged.connect(self.themeChanged)

    @Property(bool, notify=themeChanged)
    def isDark(self) -> bool:
        previews = self._themes.previews
        theme_id = self._settings.theme_identifier
        for theme in previews:
            if theme["identifier"] == theme_id:
                return theme["isDark"]
        return False

    @Property(str, notify=themeChanged)
    def background(self) -> str:
        return self._get_current_color("background")

    @Property(str, notify=themeChanged)
    def foreground(self) -> str:
        return self._get_current_color("foreground")

    @Property(str, notify=themeChanged)
    def control(self) -> str:
        return self._get_current_color("control")

    @Property(str, notify=themeChanged)
    def rowHighlight(self) -> str:
        return self._get_current_color("rowHighlight")

    @Property(str, notify=themeChanged)
    def rowHighlightText(self) -> str:
        return self._get_current_color("rowHighlightText")

    @Property(str, notify=themeChanged)
    def rowBase(self) -> str:
        return self._get_current_color("rowBase")

    @Property(str, notify=themeChanged)
    def rowBaseText(self) -> str:
        return self._get_current_color("rowBaseText")

    @Property(str, notify=themeChanged)
    def rowBaseAlternate(self) -> str:
        return self._get_current_color("rowBaseAlternate")

    @Property(str, notify=themeChanged)
    def rowBaseAlternateText(self) -> str:
        return self._get_current_color("rowBaseAlternateText")

    def _get_current_color(self, color_key: str) -> str:
        theme_id = self._settings.theme_identifier
        color_option = self._settings.theme_color_option
        palettes = self._themes.palette(theme_id)

        if 0 <= color_option < len(palettes):
            return palettes[color_option].get(color_key, "transparent")
        return "transparent"
