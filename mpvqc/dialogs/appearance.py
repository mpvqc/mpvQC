# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from dataclasses import dataclass

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.appearance import AccentColor, ThemeAppearance, ThemeIdentifier
from mpvqc.services import SettingsService, ThemeService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@dataclass(frozen=True)
class AppearanceDialogProps:
    theme_index: int
    accent_color_index: int


def derive_appearance_dialog_props(
    appearance: ThemeAppearance,
    theme_index_for: Callable[[ThemeIdentifier], int],
    accent_color_index_for: Callable[[ThemeIdentifier, AccentColor | None], int],
) -> AppearanceDialogProps:
    return AppearanceDialogProps(
        theme_index=theme_index_for(appearance.theme_identifier),
        accent_color_index=accent_color_index_for(appearance.theme_identifier, appearance.stored_accent),
    )


@QmlElement
class MpvqcAppearanceDialogViewModel(QObject):
    _themes = inject.attr(ThemeService)
    _settings = inject.attr(SettingsService)

    themeIndexChanged = Signal(int)
    accentColorIndexChanged = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._baseline_theme_identifier = self._settings.theme_identifier
        self._baseline_accents = {
            theme.identifier: self._settings.theme_accent_color_for(theme.identifier) for theme in self._themes.themes
        }
        self._appearance = self._settings.theme_appearance
        self._props = self._derive()
        self._settings.theme_appearance_changed.connect(self._fold_appearance)

    def _derive(self) -> AppearanceDialogProps:
        return derive_appearance_dialog_props(self._appearance, self._themes.theme_index, self._accent_color_index_for)

    def _accent_color_index_for(self, theme_identifier: ThemeIdentifier, accent_color: AccentColor | None) -> int:
        return self._themes.theme(theme_identifier).palette_index(accent_color)

    @Slot(ThemeAppearance)
    def _fold_appearance(self, appearance: ThemeAppearance) -> None:
        self._appearance = appearance
        new, old = self._derive(), self._props
        self._props = new
        if new.theme_index != old.theme_index:
            self.themeIndexChanged.emit(new.theme_index)
        if new.accent_color_index != old.accent_color_index:
            self.accentColorIndexChanged.emit(new.accent_color_index)

    @Property(int, notify=themeIndexChanged)
    def themeIndex(self) -> int:
        return self._props.theme_index

    @Property(int, notify=accentColorIndexChanged)
    def accentColorIndex(self) -> int:
        return self._props.accent_color_index

    @Slot(str)
    def setTheme(self, theme_identifier: str) -> None:
        self._settings.theme_identifier = theme_identifier

    @Slot(str)
    def setAccentColor(self, identifier: str) -> None:
        self._settings.set_theme_accent_color(self._appearance.theme_identifier, AccentColor(identifier))

    @Slot()
    def reject(self) -> None:
        self._settings.theme_identifier = self._baseline_theme_identifier
        for theme_identifier, accent_color in self._baseline_accents.items():
            self._settings.set_theme_accent_color(theme_identifier, accent_color)
