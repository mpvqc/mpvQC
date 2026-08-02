# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, assert_never

import inject
from PySide6.QtCore import Property, QAbstractItemModel, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.appearance.domain import (
    COLOR_SCHEME_PREFERENCES,
    AccentColor,
    AppearancePreference,
    Dark,
    FollowSystem,
    Light,
    parse_color_scheme_preference,
)
from mpvqc.appearance.models import MpvqcAccentColorModel
from mpvqc.appearance.services import AppearanceSettingsService, PaletteCatalogService

if TYPE_CHECKING:
    from collections.abc import Callable

    from mpvqc.appearance.domain import ColorScheme
    from mpvqc.appearance.services import PaletteFamily

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1

LIGHT = Light()
DARK = Dark()


@dataclass(frozen=True)
class AppearanceDialogInputs:
    appearance_preference: AppearancePreference


@dataclass(frozen=True)
class AppearanceDialogProps:
    color_scheme_preference_index: int
    accent_color_index: int
    accent_color_section_visible: bool


def derive_appearance_dialog_props(
    inputs: AppearanceDialogInputs,
    palette_family_for: Callable[[ColorScheme], PaletteFamily],
) -> AppearanceDialogProps:
    appearance_preference = inputs.appearance_preference
    color_scheme_preference = appearance_preference.color_scheme_preference
    preference_index = COLOR_SCHEME_PREFERENCES.index(color_scheme_preference)

    match color_scheme_preference:
        case FollowSystem():
            return AppearanceDialogProps(
                color_scheme_preference_index=preference_index,
                accent_color_index=-1,
                accent_color_section_visible=False,
            )
        case Light() | Dark():
            family = palette_family_for(color_scheme_preference)
            return AppearanceDialogProps(
                color_scheme_preference_index=preference_index,
                accent_color_index=family.palette_index_of(appearance_preference),
                accent_color_section_visible=True,
            )
        case _:
            assert_never(color_scheme_preference)


@QmlElement
class MpvqcAppearanceDialogViewModel(QObject):
    _catalog = inject.attr(PaletteCatalogService)
    _settings = inject.attr(AppearanceSettingsService)

    colorSchemePreferenceIndexChanged = Signal(int)
    accentColorIndexChanged = Signal(int)
    accentColorSectionVisibleChanged = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._inputs = AppearanceDialogInputs(appearance_preference=self._settings.appearance_preference)
        self._baseline = self._inputs.appearance_preference
        self._props = self._derive()

        self._accent_colors = MpvqcAccentColorModel(self)
        self._accent_colors.set_preference(self._inputs.appearance_preference.color_scheme_preference)

        self._settings.appearance_preference_changed.connect(self._fold_appearance_preference)

    def _derive(self) -> AppearanceDialogProps:
        return derive_appearance_dialog_props(self._inputs, self._catalog.palette_family_for)

    @Slot(AppearancePreference)
    def _fold_appearance_preference(self, value: AppearancePreference) -> None:
        self._update(replace(self._inputs, appearance_preference=value))

    def _update(self, inputs: AppearanceDialogInputs) -> None:
        self._inputs = inputs
        new, old = self._derive(), self._props
        if new == old:
            return
        self._props = new
        # Safe behind the guard above: one index means one color scheme preference.
        self._accent_colors.set_preference(inputs.appearance_preference.color_scheme_preference)
        if new.color_scheme_preference_index != old.color_scheme_preference_index:
            self.colorSchemePreferenceIndexChanged.emit(new.color_scheme_preference_index)
        if new.accent_color_index != old.accent_color_index:
            self.accentColorIndexChanged.emit(new.accent_color_index)
        if new.accent_color_section_visible != old.accent_color_section_visible:
            self.accentColorSectionVisibleChanged.emit(new.accent_color_section_visible)

    @Property(int, notify=colorSchemePreferenceIndexChanged)
    def colorSchemePreferenceIndex(self) -> int:
        return self._props.color_scheme_preference_index

    @Property(int, notify=accentColorIndexChanged)
    def accentColorIndex(self) -> int:
        return self._props.accent_color_index

    @Property(bool, notify=accentColorSectionVisibleChanged)
    def accentColorSectionVisible(self) -> bool:
        return self._props.accent_color_section_visible

    @Property(QAbstractItemModel, constant=True, final=True)
    def accentColorModel(self) -> MpvqcAccentColorModel:
        return self._accent_colors

    @Slot(str)
    def setColorSchemePreference(self, preference: str) -> None:
        self._settings.color_scheme_preference = parse_color_scheme_preference(preference)

    @Slot(str)
    def setAccentColor(self, accent_color: str) -> None:
        color_scheme_preference = self._inputs.appearance_preference.color_scheme_preference
        match color_scheme_preference:
            case FollowSystem():
                return
            case Light() | Dark():
                self._settings.set_accent_color_preference(color_scheme_preference, AccentColor(accent_color))
            case _:
                assert_never(color_scheme_preference)

    @Slot()
    def reject(self) -> None:
        self._settings.color_scheme_preference = self._baseline.color_scheme_preference
        self._settings.set_accent_color_preference(LIGHT, self._baseline.light_accent_color_preference)
        self._settings.set_accent_color_preference(DARK, self._baseline.dark_accent_color_preference)
