# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlAnonymous, QmlElement

from mpvqc.services import SettingsService, ThemePalette, ThemeService

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
    def foreground(self) -> str:
        return self._palette.foreground

    @Property(str, notify=paletteChanged)
    def hint(self) -> str:
        return self._palette.hint

    @Property(str, notify=paletteChanged)
    def accent(self) -> str:
        return self._palette.accent

    @Property(str, notify=paletteChanged)
    def separator(self) -> str:
        return self._palette.separator

    @Property(str, notify=paletteChanged)
    def error(self) -> str:
        return self._palette.error

    @Property(str, notify=paletteChanged)
    def errorText(self) -> str:
        return self._palette.error_text

    @Property(str, notify=paletteChanged)
    def headerBackground(self) -> str:
        return self._palette.header_background

    @Property(str, notify=paletteChanged)
    def popupBackground(self) -> str:
        return self._palette.popup_background

    @Property(str, notify=paletteChanged)
    def popupText(self) -> str:
        return self._palette.popup_text

    @Property(str, notify=paletteChanged)
    def menuBackground(self) -> str:
        return self._palette.menu_background

    @Property(str, notify=paletteChanged)
    def dialogBackground(self) -> str:
        return self._palette.dialog_background

    @Property(str, notify=paletteChanged)
    def tooltipBackground(self) -> str:
        return self._palette.tooltip_background

    @Property(str, notify=paletteChanged)
    def tooltipText(self) -> str:
        return self._palette.tooltip_text

    @Property(str, notify=paletteChanged)
    def rowBase(self) -> str:
        return self._palette.row_base

    @Property(str, notify=paletteChanged)
    def rowBaseText(self) -> str:
        return self._palette.row_base_text

    @Property(str, notify=paletteChanged)
    def rowStripe(self) -> str:
        return self._palette.row_stripe

    @Property(str, notify=paletteChanged)
    def rowStripeText(self) -> str:
        return self._palette.row_stripe_text

    @Property(str, notify=paletteChanged)
    def rowSelected(self) -> str:
        return self._palette.row_selected

    @Property(str, notify=paletteChanged)
    def rowSelectedText(self) -> str:
        return self._palette.row_selected_text


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
