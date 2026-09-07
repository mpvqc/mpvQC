# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import inject
import pytest

from mpvqc.appearance.services import (
    AppearanceSettingsService,
    ColorScheme,
    ColorSchemePreference,
    ColorSchemeService,
    Dark,
    FollowSystem,
    Light,
    SystemColorScheme,
    Unknown,
)

SYSTEM = FollowSystem()
LIGHT = Light()
DARK = Dark()
UNKNOWN = Unknown()


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, appearance_settings_service):
    def bind_settings(binder: inject.Binder):
        binder.bind(AppearanceSettingsService, appearance_settings_service)

    common_bindings_with(bind_settings)


class SystemAnswerCase(NamedTuple):
    name: str
    system_color_scheme: SystemColorScheme
    expected: ColorScheme


@pytest.mark.parametrize(
    "case",
    [
        SystemAnswerCase(name="light", system_color_scheme=LIGHT, expected=LIGHT),
        SystemAnswerCase(name="dark", system_color_scheme=DARK, expected=DARK),
        SystemAnswerCase(name="unknown-is-light", system_color_scheme=UNKNOWN, expected=LIGHT),
    ],
    ids=lambda case: case.name,
)
def test_following_the_system_takes_the_system_answer(make_style_hints, case: SystemAnswerCase):
    style_hints = make_style_hints(case.system_color_scheme)

    service = ColorSchemeService(style_hints)

    assert service.color_scheme == case.expected
    assert style_hints.calls == ["unset"]


class ExplicitPreferenceCase(NamedTuple):
    name: str
    preference: ColorSchemePreference
    system_color_scheme: SystemColorScheme
    expected: ColorScheme
    expected_call: str


@pytest.mark.parametrize(
    "case",
    [
        ExplicitPreferenceCase(
            name="light-over-dark",
            preference=LIGHT,
            system_color_scheme=DARK,
            expected=LIGHT,
            expected_call="set Light",
        ),
        ExplicitPreferenceCase(
            name="light-over-unknown",
            preference=LIGHT,
            system_color_scheme=UNKNOWN,
            expected=LIGHT,
            expected_call="set Light",
        ),
        ExplicitPreferenceCase(
            name="dark-over-light",
            preference=DARK,
            system_color_scheme=LIGHT,
            expected=DARK,
            expected_call="set Dark",
        ),
        ExplicitPreferenceCase(
            name="dark-over-unknown",
            preference=DARK,
            system_color_scheme=UNKNOWN,
            expected=DARK,
            expected_call="set Dark",
        ),
    ],
    ids=lambda case: case.name,
)
def test_explicit_preference_ignores_the_system_and_pushes_into_qt(
    appearance_settings_service, make_style_hints, case: ExplicitPreferenceCase
):
    appearance_settings_service.color_scheme_preference = case.preference
    style_hints = make_style_hints(case.system_color_scheme)

    service = ColorSchemeService(style_hints)

    assert service.color_scheme == case.expected
    assert style_hints.calls == [case.expected_call]


class SystemFlipCase(NamedTuple):
    name: str
    starts_at: SystemColorScheme
    flips_to: SystemColorScheme
    expected: ColorScheme


@pytest.mark.parametrize(
    "case",
    [
        SystemFlipCase(name="light-to-dark", starts_at=LIGHT, flips_to=DARK, expected=DARK),
        SystemFlipCase(name="dark-to-unknown-is-light", starts_at=DARK, flips_to=UNKNOWN, expected=LIGHT),
    ],
    ids=lambda case: case.name,
)
def test_system_flip_publishes_the_new_scheme(make_spy, make_style_hints, case: SystemFlipCase):
    style_hints = make_style_hints(case.starts_at)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.color_scheme_changed)

    style_hints.system_reports(case.flips_to)

    assert spy.count() == 1
    assert spy.at(0, 0) == case.expected
    assert service.color_scheme == case.expected


def test_system_answer_resolving_to_the_same_scheme_publishes_nothing(make_spy, make_style_hints):
    style_hints = make_style_hints(UNKNOWN)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.color_scheme_changed)

    style_hints.system_reports(LIGHT)

    assert spy.count() == 0
    assert service.color_scheme == LIGHT


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
