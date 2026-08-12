# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, assert_never

from PySide6.QtCore import QObject, Signal

from .preferences import AccentColor, AppearancePreference, NoPreference
from .schemes import (
    Dark,
    Light,
    format_color_scheme,
    format_color_scheme_preference,
    parse_color_scheme_preference_or_default,
)

if TYPE_CHECKING:
    from PySide6.QtCore import QSettings

    from .preferences import AccentColorPreference
    from .schemes import ColorScheme, ColorSchemePreference

_COLOR_SCHEME_PREFERENCE_KEY = "Appearance/colorSchemePreference"

_LIGHT = Light()
_DARK = Dark()


def _accent_color_key(color_scheme: ColorScheme) -> str:
    return f"Appearance/accentColor/{format_color_scheme(color_scheme)}"


class AppearanceSettingsService(QObject):
    appearance_preference_changed = Signal(AppearancePreference)

    def __init__(self, qsettings: QSettings, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._qsettings = qsettings

    @property
    def appearance_preference(self) -> AppearancePreference:
        return AppearancePreference(
            color_scheme_preference=self.color_scheme_preference,
            light_accent_color_preference=self._accent_color_preference_for(_LIGHT),
            dark_accent_color_preference=self._accent_color_preference_for(_DARK),
        )

    @property
    def color_scheme_preference(self) -> ColorSchemePreference:
        stored = self._qsettings.value(_COLOR_SCHEME_PREFERENCE_KEY, type=str)
        return parse_color_scheme_preference_or_default(stored if isinstance(stored, str) else None)

    @color_scheme_preference.setter
    def color_scheme_preference(self, preference: ColorSchemePreference) -> None:
        if self.color_scheme_preference == preference:
            return
        self._store_color_scheme_preference(preference)
        self.appearance_preference_changed.emit(self.appearance_preference)

    def set_accent_color_preference(self, color_scheme: ColorScheme, preference: AccentColorPreference) -> None:
        if self._accent_color_preference_for(color_scheme) == preference:
            return
        self._store_accent_color_preference(color_scheme, preference)
        self.appearance_preference_changed.emit(self.appearance_preference)

    def restore(self, appearance_preference: AppearancePreference) -> None:
        if self.appearance_preference == appearance_preference:
            return
        self._store_color_scheme_preference(appearance_preference.color_scheme_preference)
        self._store_accent_color_preference(_LIGHT, appearance_preference.light_accent_color_preference)
        self._store_accent_color_preference(_DARK, appearance_preference.dark_accent_color_preference)
        self.appearance_preference_changed.emit(self.appearance_preference)

    def _accent_color_preference_for(self, color_scheme: ColorScheme) -> AccentColorPreference:
        key = _accent_color_key(color_scheme)
        if self._qsettings.contains(key):
            value = self._qsettings.value(key, type=str)
            if isinstance(value, str):
                return AccentColor(value)
        return NoPreference()

    def _store_color_scheme_preference(self, preference: ColorSchemePreference) -> None:
        self._qsettings.setValue(_COLOR_SCHEME_PREFERENCE_KEY, format_color_scheme_preference(preference))

    def _store_accent_color_preference(self, color_scheme: ColorScheme, preference: AccentColorPreference) -> None:
        key = _accent_color_key(color_scheme)
        match preference:
            case NoPreference():
                self._qsettings.remove(key)
            case AccentColor():
                self._qsettings.setValue(key, preference.identifier)
            case _:
                assert_never(preference)
