# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from typing import NewType, assert_never

from PySide6.QtCore import Qt

AccentColor = NewType("AccentColor", str)


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


@dataclass(frozen=True)
class FollowSystem:
    """The UI renders whatever the system says."""


type ColorSchemePreference = FollowSystem | ColorScheme

# Every preference there is, in the order the appearance dialog offers them in.
# Plain values, not shared singletons: preferences compare with ==, never with is.
COLOR_SCHEME_PREFERENCES: tuple[ColorSchemePreference, ...] = (FollowSystem(), Light(), Dark())


def parse_color_scheme_preference(text: str) -> ColorSchemePreference:
    """Read a color scheme preference off a boundary."""
    if text == "system":
        return FollowSystem()
    try:
        return parse_color_scheme(text)
    except ValueError:
        message = f"{text!r} names no color scheme preference"
        raise ValueError(message) from None


def format_color_scheme_preference(preference: ColorSchemePreference) -> str:
    """Write a color scheme preference to a boundary."""
    match preference:
        case FollowSystem():
            return "system"
        case Light() | Dark():
            return format_color_scheme(preference)
        case _:
            assert_never(preference)


def resolve_color_scheme(
    preference: ColorSchemePreference,
    system_color_scheme: Qt.ColorScheme,
) -> ColorScheme:
    match preference:
        case FollowSystem():
            if system_color_scheme is Qt.ColorScheme.Light:
                return Light()
            # Dark also when the system cannot answer: mpvQC's historic default
            return Dark()
        case Light() | Dark():
            return preference
        case _:
            assert_never(preference)


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
