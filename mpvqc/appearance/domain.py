# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from typing import assert_never


@dataclass(frozen=True)
class AccentColor:
    identifier: str


@dataclass(frozen=True)
class NoPreference:
    pass


type AccentColorPreference = NoPreference | AccentColor


@dataclass(frozen=True)
class Light:
    pass


@dataclass(frozen=True)
class Dark:
    pass


type ColorScheme = Light | Dark


@dataclass(frozen=True)
class FollowSystem:
    pass


type ColorSchemePreference = FollowSystem | ColorScheme

# The order the appearance dialog offers the preferences in: the index is the dialog's selected index.
COLOR_SCHEME_PREFERENCES: tuple[ColorSchemePreference, ...] = (FollowSystem(), Light(), Dark())


@dataclass(frozen=True)
class Unknown:
    pass


type SystemColorScheme = ColorScheme | Unknown


def parse_color_scheme(text: str) -> ColorScheme:
    if text == "light":
        return Light()
    if text == "dark":
        return Dark()
    message = f"{text!r} names no color scheme"
    raise ValueError(message)


def format_color_scheme(color_scheme: ColorScheme) -> str:
    match color_scheme:
        case Light():
            return "light"
        case Dark():
            return "dark"
        case _:
            assert_never(color_scheme)


def parse_color_scheme_preference(text: str) -> ColorSchemePreference:
    if text == "system":
        return FollowSystem()
    try:
        return parse_color_scheme(text)
    except ValueError:
        message = f"{text!r} names no color scheme preference"
        raise ValueError(message) from None


def parse_color_scheme_preference_or_default(text: str | None) -> ColorSchemePreference:
    try:
        return parse_color_scheme_preference(text or "")
    except ValueError:
        return default_color_scheme_preference()


def default_color_scheme_preference() -> ColorSchemePreference:
    return FollowSystem()


def format_color_scheme_preference(preference: ColorSchemePreference) -> str:
    match preference:
        case FollowSystem():
            return "system"
        case Light() | Dark():
            return format_color_scheme(preference)
        case _:
            assert_never(preference)


def resolve_color_scheme(
    preference: ColorSchemePreference,
    system_color_scheme: SystemColorScheme,
) -> ColorScheme:
    match preference:
        case FollowSystem():
            match system_color_scheme:
                case Light() | Dark():
                    return system_color_scheme
                case Unknown():
                    return Dark()  # mpvQC's historic default
                case _:
                    assert_never(system_color_scheme)
        case Light() | Dark():
            return preference
        case _:
            assert_never(preference)


@dataclass(frozen=True)
class AppearancePreference:
    color_scheme_preference: ColorSchemePreference
    light_accent_color_preference: AccentColorPreference
    dark_accent_color_preference: AccentColorPreference

    def accent_color_preference_for(self, color_scheme: ColorScheme) -> AccentColorPreference:
        match color_scheme:
            case Light():
                return self.light_accent_color_preference
            case Dark():
                return self.dark_accent_color_preference
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
