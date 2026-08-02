# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.appearance.domain import Dark, FollowSystem, Light, Unknown
from mpvqc.appearance.services import AppearanceSettingsService, ColorSchemeService

SYSTEM = FollowSystem()
LIGHT = Light()
DARK = Dark()
UNKNOWN = Unknown()


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, appearance_settings_service):
    def bind_settings(binder: inject.Binder):
        binder.bind(AppearanceSettingsService, appearance_settings_service)

    common_bindings_with(bind_settings)


@pytest.mark.parametrize(
    ("system_color_scheme", "expected"),
    [
        (LIGHT, LIGHT),
        (DARK, DARK),
        (UNKNOWN, DARK),
    ],
    ids=["light", "dark", "unknown-is-dark"],
)
def test_following_the_system_takes_the_system_answer(make_style_hints, system_color_scheme, expected):
    style_hints = make_style_hints(system_color_scheme)

    service = ColorSchemeService(style_hints)

    assert service.color_scheme == expected
    assert style_hints.calls == ["unset"]


@pytest.mark.parametrize(
    ("preference", "system_color_scheme", "expected", "expected_call"),
    [
        (LIGHT, DARK, LIGHT, "set Light"),
        (LIGHT, UNKNOWN, LIGHT, "set Light"),
        (DARK, LIGHT, DARK, "set Dark"),
        (DARK, UNKNOWN, DARK, "set Dark"),
    ],
    ids=["light-over-dark", "light-over-unknown", "dark-over-light", "dark-over-unknown"],
)
def test_explicit_preference_ignores_the_system_and_pushes_into_qt(
    appearance_settings_service, make_style_hints, preference, system_color_scheme, expected, expected_call
):
    appearance_settings_service.color_scheme_preference = preference
    style_hints = make_style_hints(system_color_scheme)

    service = ColorSchemeService(style_hints)

    assert service.color_scheme == expected
    assert style_hints.calls == [expected_call]


def test_system_flip_publishes_the_new_scheme(make_spy, make_style_hints):
    style_hints = make_style_hints(LIGHT)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.color_scheme_changed)

    style_hints.system_reports(DARK)

    assert spy.count() == 1
    assert spy.at(0, 0) == DARK
    assert service.color_scheme == DARK


def test_system_answer_resolving_to_the_same_scheme_publishes_nothing(make_spy, make_style_hints):
    # the system moves off unknown, but unknown and dark both resolve to dark
    style_hints = make_style_hints(UNKNOWN)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.color_scheme_changed)

    style_hints.system_reports(DARK)

    assert spy.count() == 0
    assert service.color_scheme == DARK


def test_system_flip_under_an_explicit_preference_publishes_nothing(
    appearance_settings_service, make_spy, make_style_hints
):
    appearance_settings_service.color_scheme_preference = LIGHT
    style_hints = make_style_hints(LIGHT)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.color_scheme_changed)

    style_hints.system_reports(DARK)

    assert spy.count() == 0
    assert service.color_scheme == LIGHT


def test_preference_change_to_explicit_pushes_into_qt_and_publishes(
    appearance_settings_service, make_spy, make_style_hints
):
    style_hints = make_style_hints(LIGHT)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.color_scheme_changed)

    appearance_settings_service.color_scheme_preference = DARK

    assert spy.count() == 1
    assert spy.at(0, 0) == DARK
    assert service.color_scheme == DARK
    assert style_hints.calls == ["unset", "set Dark"]


def test_preference_change_back_to_system_unsets_and_follows_again(
    appearance_settings_service, make_spy, make_style_hints
):
    appearance_settings_service.color_scheme_preference = DARK
    style_hints = make_style_hints(LIGHT)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.color_scheme_changed)

    appearance_settings_service.color_scheme_preference = SYSTEM

    assert spy.count() == 1
    assert spy.at(0, 0) == LIGHT
    assert service.color_scheme == LIGHT
    assert style_hints.calls == ["set Dark", "unset"]


def test_preference_change_keeping_the_scheme_pushes_into_qt_but_publishes_nothing(
    appearance_settings_service, make_spy, make_style_hints
):
    style_hints = make_style_hints(DARK)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.color_scheme_changed)

    appearance_settings_service.color_scheme_preference = DARK

    assert spy.count() == 0
    assert service.color_scheme == DARK
    assert style_hints.calls == ["unset", "set Dark"]


def test_following_the_system_survives_a_preference_round_trip(appearance_settings_service, make_spy, make_style_hints):
    style_hints = make_style_hints(LIGHT)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.color_scheme_changed)

    appearance_settings_service.color_scheme_preference = DARK
    appearance_settings_service.color_scheme_preference = SYSTEM
    style_hints.system_reports(DARK)

    assert [spy.at(index, 0) for index in range(spy.count())] == [DARK, LIGHT, DARK]
    assert service.color_scheme == DARK
