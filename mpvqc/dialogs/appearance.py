# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from dataclasses import dataclass
from typing import assert_never

import inject
from PySide6.QtCore import Property, QAbstractItemModel, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.appearance import (
    COLOR_SCHEME_PREFERENCES,
    AccentColor,
    AccentColorPreference,
    Appearance,
    ColorScheme,
    Dark,
    FollowSystem,
    Light,
    parse_color_scheme_preference,
)
from mpvqc.models import MpvqcAccentColorModel
from mpvqc.services import PaletteCatalogService, SettingsService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1

LIGHT = Light()
DARK = Dark()


@dataclass(frozen=True)
class AppearanceDialogProps:
    color_scheme_preference_index: int
    accent_color_index: int
    accent_section_visible: bool
    accent_section_color_scheme: ColorScheme | None


def derive_appearance_dialog_props(
    appearance: Appearance,
    accent_color_index_for: Callable[[ColorScheme, AccentColorPreference], int],
) -> AppearanceDialogProps:
    preference = appearance.color_scheme_preference
    preference_index = COLOR_SCHEME_PREFERENCES.index(preference)

    match preference:
        case FollowSystem():
            return AppearanceDialogProps(
                color_scheme_preference_index=preference_index,
                accent_color_index=-1,
                accent_section_visible=False,
                accent_section_color_scheme=None,
            )
        case Light() | Dark():
            return AppearanceDialogProps(
                color_scheme_preference_index=preference_index,
                accent_color_index=accent_color_index_for(preference, appearance.accent_color_for(preference)),
                accent_section_visible=True,
                accent_section_color_scheme=preference,
            )
        case _:
            assert_never(preference)


@QmlElement
class MpvqcAppearanceDialogViewModel(QObject):
    _catalog = inject.attr(PaletteCatalogService)
    _settings = inject.attr(SettingsService)

    colorSchemePreferenceIndexChanged = Signal(int)
    accentColorIndexChanged = Signal(int)
    accentSectionVisibleChanged = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._appearance = self._settings.appearance
        self._baseline = self._appearance
        self._props = self._derive()
        self._accent_colors = MpvqcAccentColorModel(self)
        self._accent_colors.set_color_scheme(self._props.accent_section_color_scheme)
        self._settings.appearance_changed.connect(self._fold_appearance)

    def _derive(self) -> AppearanceDialogProps:
        return derive_appearance_dialog_props(self._appearance, self._accent_color_index_for)

    def _accent_color_index_for(self, color_scheme: ColorScheme, accent_color: AccentColorPreference) -> int:
        return self._catalog.palette_family_for(color_scheme).palette_index(accent_color)

    @Slot(Appearance)
    def _fold_appearance(self, appearance: Appearance) -> None:
        self._appearance = appearance
        new, old = self._derive(), self._props
        self._props = new
        self._accent_colors.set_color_scheme(new.accent_section_color_scheme)
        if new.color_scheme_preference_index != old.color_scheme_preference_index:
            self.colorSchemePreferenceIndexChanged.emit(new.color_scheme_preference_index)
        if new.accent_color_index != old.accent_color_index:
            self.accentColorIndexChanged.emit(new.accent_color_index)
        if new.accent_section_visible != old.accent_section_visible:
            self.accentSectionVisibleChanged.emit(new.accent_section_visible)

    @Property(int, notify=colorSchemePreferenceIndexChanged)
    def colorSchemePreferenceIndex(self) -> int:
        return self._props.color_scheme_preference_index

    @Property(int, notify=accentColorIndexChanged)
    def accentColorIndex(self) -> int:
        return self._props.accent_color_index

    @Property(bool, notify=accentSectionVisibleChanged)
    def accentSectionVisible(self) -> bool:
        return self._props.accent_section_visible

    @Property(QAbstractItemModel, constant=True, final=True)
    def accentColorModel(self) -> MpvqcAccentColorModel:
        return self._accent_colors

    @Slot(str)
    def setColorSchemePreference(self, preference: str) -> None:
        self._settings.color_scheme_preference = parse_color_scheme_preference(preference)

    @Slot(str)
    def setAccentColor(self, accent_color: str) -> None:
        color_scheme = self._props.accent_section_color_scheme
        if color_scheme is None:
            return
        self._settings.set_accent_color(color_scheme, AccentColor(accent_color))

    @Slot()
    def reject(self) -> None:
        self._settings.color_scheme_preference = self._baseline.color_scheme_preference
        self._settings.set_accent_color(LIGHT, self._baseline.light_accent_color)
        self._settings.set_accent_color(DARK, self._baseline.dark_accent_color)
