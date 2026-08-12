# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from typing import assert_never

from .schemes import ColorScheme, ColorSchemePreference, Dark, Light


@dataclass(frozen=True)
class AccentColor:
    identifier: str


@dataclass(frozen=True)
class NoPreference:
    pass


type AccentColorPreference = NoPreference | AccentColor


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
