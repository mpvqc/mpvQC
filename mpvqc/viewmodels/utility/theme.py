# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlAnonymous, QmlElement

from mpvqc.services import SettingsService, ThemeService
from mpvqc.services.theme import ThemePalette

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlAnonymous
class MpvqcThemePalette(QObject):
    paletteChanged = Signal()

    def __init__(self, parent: QObject | None = None, *, palette: ThemePalette) -> None:
        super().__init__(parent)
        self._palette = palette

    def update(self, palette: ThemePalette) -> None:
        if palette != self._palette:
            self._palette = palette
            self.paletteChanged.emit()

    @Property(str, notify=paletteChanged)
    def background(self) -> str:
        return self._palette.background

    @Property(str, notify=paletteChanged)
    def backgroundAlternate(self) -> str:
        return self._palette.background_alternate

    @Property(str, notify=paletteChanged)
    def foreground(self) -> str:
        return self._palette.foreground

    @Property(str, notify=paletteChanged)
    def foregroundAlternate(self) -> str:
        return self._palette.foreground_alternate

    @Property(str, notify=paletteChanged)
    def control(self) -> str:
        return self._palette.control

    @Property(str, notify=paletteChanged)
    def rowHighlight(self) -> str:
        return self._palette.row_highlight

    @Property(str, notify=paletteChanged)
    def rowHighlightText(self) -> str:
        return self._palette.row_highlight_text

    @Property(str, notify=paletteChanged)
    def rowBase(self) -> str:
        return self._palette.row_base

    @Property(str, notify=paletteChanged)
    def rowBaseText(self) -> str:
        return self._palette.row_base_text

    @Property(str, notify=paletteChanged)
    def rowBaseAlternate(self) -> str:
        return self._palette.row_base_alternate

    @Property(str, notify=paletteChanged)
    def rowBaseAlternateText(self) -> str:
        return self._palette.row_base_alternate_text


@QmlElement
class MpvqcThemeViewModel(QObject):
    _themes = inject.attr(ThemeService)
    _settings = inject.attr(SettingsService)

    themeChanged = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._theme = self._themes.theme()
        self._palette = MpvqcThemePalette(self, palette=self._current_palette)
        self._settings.theme_identifier_changed.connect(self._on_theme_identifier_changed)
        self._settings.primary_color_changed.connect(self._on_primary_color_changed)

    @property
    def _current_palette(self) -> ThemePalette:
        return self._themes.theme().palette_for(self._settings.primary_color)

    @Slot()
    def _on_theme_identifier_changed(self) -> None:
        self._theme = self._themes.theme()
        self._palette.update(self._current_palette)
        self.themeChanged.emit()

    @Slot()
    def _on_primary_color_changed(self) -> None:
        self._palette.update(self._current_palette)

    @Property(bool, notify=themeChanged)
    def isDark(self) -> bool:
        return self._theme.is_dark

    @Property(MpvqcThemePalette, constant=True)
    def palette(self) -> MpvqcThemePalette:
        return self._palette
