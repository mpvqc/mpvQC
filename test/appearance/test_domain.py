# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.appearance.domain import (
    COLOR_SCHEME_PREFERENCES,
    AccentColor,
    AppearancePreference,
    Dark,
    FollowSystem,
    Light,
    Unknown,
    default_color_scheme_preference,
    format_color_scheme,
    format_color_scheme_preference,
    parse_color_scheme,
    parse_color_scheme_preference,
    parse_color_scheme_preference_or_default,
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
        (SYSTEM, UNKNOWN, LIGHT),
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
        "system-unknown-is-light",
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


def test_the_default_preference_follows_the_system():
    assert default_color_scheme_preference() == SYSTEM


@pytest.mark.parametrize(("text", "preference"), [("system", SYSTEM), ("light", LIGHT), ("dark", DARK)])
def test_stored_text_naming_a_preference_parses_to_it(text, preference):
    assert parse_color_scheme_preference_or_default(text) == preference


@pytest.mark.parametrize("text", [None, "", "System", "sepia", "nonsense"])
def test_stored_text_naming_no_preference_falls_back_to_the_default(text):
    assert parse_color_scheme_preference_or_default(text) == default_color_scheme_preference()


def test_every_preference_is_offered_once_in_dialog_order():
    assert [format_color_scheme_preference(p) for p in COLOR_SCHEME_PREFERENCES] == ["system", "light", "dark"]


@pytest.mark.parametrize(
    ("color_scheme", "expected"),
    [
        (LIGHT, AccentColor("#l1")),
        (DARK, AccentColor("#d1")),
    ],
)
def test_appearance_preference_reads_the_accent_color_preference_of_the_asked_scheme(color_scheme, expected):
    appearance_preference = AppearancePreference(
        color_scheme_preference=SYSTEM,
        light_accent_color_preference=AccentColor("#l1"),
        dark_accent_color_preference=AccentColor("#d1"),
    )

    assert appearance_preference.accent_color_preference_for(color_scheme) == expected
