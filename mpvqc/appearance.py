# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from enum import StrEnum
from typing import NewType

from PySide6.QtCore import Qt

ThemeIdentifier = NewType("ThemeIdentifier", str)
AccentColor = NewType("AccentColor", str)


class ColorSchemePreference(StrEnum):
    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"


class EffectiveColorScheme(StrEnum):
    LIGHT = "light"
    DARK = "dark"


def resolve_color_scheme(
    preference: ColorSchemePreference,
    system_color_scheme: Qt.ColorScheme,
) -> EffectiveColorScheme:
    if preference is ColorSchemePreference.LIGHT:
        return EffectiveColorScheme.LIGHT
    if preference is ColorSchemePreference.DARK:
        return EffectiveColorScheme.DARK
    if system_color_scheme is Qt.ColorScheme.Light:
        return EffectiveColorScheme.LIGHT
    # Dark also when the system cannot answer: mpvQC's historic default
    return EffectiveColorScheme.DARK


@dataclass(frozen=True)
class Appearance:
    color_scheme_preference: ColorSchemePreference
    light_accent_color: AccentColor | None
    dark_accent_color: AccentColor | None

    def accent_color_for(self, color_scheme: EffectiveColorScheme) -> AccentColor | None:
        if color_scheme is EffectiveColorScheme.LIGHT:
            return self.light_accent_color
        return self.dark_accent_color


@dataclass(frozen=True)
class ThemeAppearance:
    theme_identifier: ThemeIdentifier
    stored_accent: AccentColor | None


@dataclass(frozen=True)
class Palette:
    accent_color: AccentColor
    background: str
    foreground: str
    hint: str
    accent: str
    separator: str
    error: str
    error_text: str
    header_background: str
    popup_background: str
    popup_text: str
    menu_background: str
    dialog_background: str
    section_card: str
    tooltip_background: str
    tooltip_text: str
    row_base: str
    row_base_text: str
    row_stripe: str
    row_stripe_text: str
    row_selected: str
    row_selected_text: str
