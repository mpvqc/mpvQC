# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest

from mpvqc.appearance.services import (
    COLOR_SCHEME_PREFERENCES,
    ColorScheme,
    ColorSchemePreference,
    Dark,
    FollowSystem,
    Light,
    SystemColorScheme,
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


class ResolveCase(NamedTuple):
    name: str
    preference: ColorSchemePreference
    system_color_scheme: SystemColorScheme
    expected: ColorScheme


@pytest.mark.parametrize(
    "case",
    [
        ResolveCase(
            name="light-over-light",
            preference=LIGHT,
            system_color_scheme=LIGHT,
            expected=LIGHT,
        ),
        ResolveCase(
            name="light-over-dark",
            preference=LIGHT,
            system_color_scheme=DARK,
            expected=LIGHT,
        ),
        ResolveCase(
            name="light-over-unknown",
            preference=LIGHT,
            system_color_scheme=UNKNOWN,
            expected=LIGHT,
        ),
        ResolveCase(
            name="dark-over-light",
            preference=DARK,
            system_color_scheme=LIGHT,
            expected=DARK,
        ),
        ResolveCase(
            name="dark-over-dark",
            preference=DARK,
            system_color_scheme=DARK,
            expected=DARK,
        ),
        ResolveCase(
            name="dark-over-unknown",
            preference=DARK,
            system_color_scheme=UNKNOWN,
            expected=DARK,
        ),
        ResolveCase(
            name="system-follows-light",
            preference=SYSTEM,
            system_color_scheme=LIGHT,
            expected=LIGHT,
        ),
        ResolveCase(
            name="system-follows-dark",
            preference=SYSTEM,
            system_color_scheme=DARK,
            expected=DARK,
        ),
        ResolveCase(
            name="system-unknown-is-light",
            preference=SYSTEM,
            system_color_scheme=UNKNOWN,
            expected=LIGHT,
        ),
    ],
    ids=lambda case: case.name,
)
def test_resolve_color_scheme(case: ResolveCase):
    assert resolve_color_scheme(case.preference, case.system_color_scheme) == case.expected


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
