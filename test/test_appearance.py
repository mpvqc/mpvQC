# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from PySide6.QtCore import Qt

from mpvqc.appearance import (
    AccentColor,
    Appearance,
    ColorSchemePreference,
    EffectiveColorScheme,
    resolve_color_scheme,
)

LIGHT = EffectiveColorScheme.LIGHT
DARK = EffectiveColorScheme.DARK


@pytest.mark.parametrize(
    ("preference", "system_color_scheme", "expected"),
    [
        (ColorSchemePreference.LIGHT, Qt.ColorScheme.Light, LIGHT),
        (ColorSchemePreference.LIGHT, Qt.ColorScheme.Dark, LIGHT),
        (ColorSchemePreference.LIGHT, Qt.ColorScheme.Unknown, LIGHT),
        (ColorSchemePreference.DARK, Qt.ColorScheme.Light, DARK),
        (ColorSchemePreference.DARK, Qt.ColorScheme.Dark, DARK),
        (ColorSchemePreference.DARK, Qt.ColorScheme.Unknown, DARK),
        (ColorSchemePreference.SYSTEM, Qt.ColorScheme.Light, LIGHT),
        (ColorSchemePreference.SYSTEM, Qt.ColorScheme.Dark, DARK),
        (ColorSchemePreference.SYSTEM, Qt.ColorScheme.Unknown, DARK),
    ],
)
def test_resolve_color_scheme(preference, system_color_scheme, expected):
    assert resolve_color_scheme(preference, system_color_scheme) is expected


@pytest.mark.parametrize(
    ("color_scheme", "expected"),
    [
        (LIGHT, AccentColor("#l1")),
        (DARK, AccentColor("#d1")),
    ],
)
def test_appearance_accent_color_for_reads_the_scheme_entry(color_scheme, expected):
    appearance = Appearance(
        color_scheme_preference=ColorSchemePreference.SYSTEM,
        light_accent_color=AccentColor("#l1"),
        dark_accent_color=AccentColor("#d1"),
    )

    assert appearance.accent_color_for(color_scheme) == expected


@pytest.mark.parametrize("color_scheme", [LIGHT, DARK])
def test_appearance_accent_color_for_reports_an_empty_entry(color_scheme):
    appearance = Appearance(
        color_scheme_preference=ColorSchemePreference.SYSTEM,
        light_accent_color=None,
        dark_accent_color=None,
    )

    assert appearance.accent_color_for(color_scheme) is None
