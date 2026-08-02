# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.appearance import (
    COLOR_SCHEME_PREFERENCES,
    AccentColor,
    Appearance,
    Dark,
    FollowSystem,
    Light,
    Unknown,
    format_color_scheme,
    format_color_scheme_preference,
    parse_color_scheme,
    parse_color_scheme_preference,
    resolve_color_scheme,
)

SYSTEM = FollowSystem()
LIGHT = Light()
DARK = Dark()
UNKNOWN = Unknown()


@pytest.mark.parametrize(
    ("preference", "system_color_scheme", "expected"),
    [
        (LIGHT, LIGHT, LIGHT),
        (LIGHT, DARK, LIGHT),
        (LIGHT, UNKNOWN, LIGHT),
        (DARK, LIGHT, DARK),
        (DARK, DARK, DARK),
        (DARK, UNKNOWN, DARK),
        (SYSTEM, LIGHT, LIGHT),
        (SYSTEM, DARK, DARK),
        (SYSTEM, UNKNOWN, DARK),
    ],
    ids=[
        "light-over-light",
        "light-over-dark",
        "light-over-unknown",
        "dark-over-light",
        "dark-over-dark",
        "dark-over-unknown",
        "system-follows-light",
        "system-follows-dark",
        "system-unknown-is-dark",
    ],
)
def test_resolve_color_scheme(preference, system_color_scheme, expected):
    assert resolve_color_scheme(preference, system_color_scheme) == expected


@pytest.mark.parametrize(("text", "color_scheme"), [("light", LIGHT), ("dark", DARK)])
def test_a_color_scheme_survives_the_round_trip_through_its_boundary_text(text, color_scheme):
    assert parse_color_scheme(text) == color_scheme
    assert format_color_scheme(color_scheme) == text


@pytest.mark.parametrize("text", ["", "system", "Light", "nonsense"])
def test_parsing_text_that_names_no_color_scheme_raises(text):
    with pytest.raises(ValueError, match="color scheme"):
        parse_color_scheme(text)


@pytest.mark.parametrize(("text", "preference"), [("system", SYSTEM), ("light", LIGHT), ("dark", DARK)])
def test_a_preference_survives_the_round_trip_through_its_boundary_text(text, preference):
    assert parse_color_scheme_preference(text) == preference
    assert format_color_scheme_preference(preference) == text


@pytest.mark.parametrize("text", ["", "System", "sepia", "nonsense"])
def test_parsing_text_that_names_no_preference_raises(text):
    with pytest.raises(ValueError, match="color scheme preference"):
        parse_color_scheme_preference(text)


def test_every_preference_is_offered_once_in_dialog_order():
    assert [format_color_scheme_preference(p) for p in COLOR_SCHEME_PREFERENCES] == ["system", "light", "dark"]


@pytest.mark.parametrize(
    ("color_scheme", "expected"),
    [
        (LIGHT, AccentColor("#l1")),
        (DARK, AccentColor("#d1")),
    ],
)
def test_appearance_accent_color_for_reads_the_scheme_entry(color_scheme, expected):
    appearance = Appearance(
        color_scheme_preference=SYSTEM,
        light_accent_color=AccentColor("#l1"),
        dark_accent_color=AccentColor("#d1"),
    )

    assert appearance.accent_color_for(color_scheme) == expected


@pytest.mark.parametrize("color_scheme", [LIGHT, DARK])
def test_appearance_accent_color_for_reports_an_empty_entry(color_scheme):
    appearance = Appearance(
        color_scheme_preference=SYSTEM,
        light_accent_color=None,
        dark_accent_color=None,
    )

    assert appearance.accent_color_for(color_scheme) is None
