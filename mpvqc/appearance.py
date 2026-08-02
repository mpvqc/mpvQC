# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from enum import StrEnum
from typing import NewType, assert_never

from PySide6.QtCore import Qt

AccentColor = NewType("AccentColor", str)


class ColorSchemePreference(StrEnum):
    # Declaration order is the order the appearance dialog offers them in
    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"


@dataclass(frozen=True)
class Light:
    """The UI renders light."""


@dataclass(frozen=True)
class Dark:
    """The UI renders dark."""


type ColorScheme = Light | Dark


def parse_color_scheme(text: str) -> ColorScheme:
    """Read a color scheme off a boundary."""
    if text == "light":
        return Light()
    if text == "dark":
        return Dark()
    message = f"{text!r} names no color scheme"
    raise ValueError(message)


def format_color_scheme(color_scheme: ColorScheme) -> str:
    """Write a color scheme to a boundary."""
    match color_scheme:
        case Light():
            return "light"
        case Dark():
            return "dark"
        case _:
            assert_never(color_scheme)


def explicit_color_scheme(preference: ColorSchemePreference) -> ColorScheme | None:
    """The color scheme a preference names, or nothing when it names none."""
    if preference is ColorSchemePreference.LIGHT:
        return Light()
    if preference is ColorSchemePreference.DARK:
        return Dark()
    return None


def resolve_color_scheme(
    preference: ColorSchemePreference,
    system_color_scheme: Qt.ColorScheme,
) -> ColorScheme:
    if preference is ColorSchemePreference.LIGHT:
        return Light()
    if preference is ColorSchemePreference.DARK:
        return Dark()
    if system_color_scheme is Qt.ColorScheme.Light:
        return Light()
    # Dark also when the system cannot answer: mpvQC's historic default
    return Dark()


@dataclass(frozen=True)
class Appearance:
    color_scheme_preference: ColorSchemePreference
    light_accent_color: AccentColor | None
    dark_accent_color: AccentColor | None

    def accent_color_for(self, color_scheme: ColorScheme) -> AccentColor | None:
        match color_scheme:
            case Light():
                return self.light_accent_color
            case Dark():
                return self.dark_accent_color
            case _:
                assert_never(color_scheme)


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
