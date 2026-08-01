# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest
from PySide6.QtCore import Qt

from mpvqc.appearance import ColorSchemePreference, EffectiveColorScheme
from mpvqc.services import ColorSchemeService, SettingsService

LIGHT = EffectiveColorScheme.LIGHT
DARK = EffectiveColorScheme.DARK


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, settings_service):
    def bind_settings(binder: inject.Binder):
        binder.bind(SettingsService, settings_service)

    common_bindings_with(bind_settings)


@pytest.mark.parametrize(
    ("system_color_scheme", "expected"),
    [
        (Qt.ColorScheme.Light, LIGHT),
        (Qt.ColorScheme.Dark, DARK),
        (Qt.ColorScheme.Unknown, DARK),
    ],
)
def test_system_preference_takes_the_system_answer(make_style_hints, system_color_scheme, expected):
    style_hints = make_style_hints(system_color_scheme)

    service = ColorSchemeService(style_hints)

    assert service.effective_color_scheme is expected
    assert style_hints.calls == ["unset"]


@pytest.mark.parametrize(
    ("preference", "system_color_scheme", "expected", "expected_call"),
    [
        (ColorSchemePreference.LIGHT, Qt.ColorScheme.Dark, LIGHT, "set Light"),
        (ColorSchemePreference.LIGHT, Qt.ColorScheme.Unknown, LIGHT, "set Light"),
        (ColorSchemePreference.DARK, Qt.ColorScheme.Light, DARK, "set Dark"),
        (ColorSchemePreference.DARK, Qt.ColorScheme.Unknown, DARK, "set Dark"),
    ],
)
def test_explicit_preference_ignores_the_system_and_pushes_into_qt(
    settings_service, make_style_hints, preference, system_color_scheme, expected, expected_call
):
    settings_service.color_scheme_preference = preference
    style_hints = make_style_hints(system_color_scheme)

    service = ColorSchemeService(style_hints)

    assert service.effective_color_scheme is expected
    assert style_hints.calls == [expected_call]


def test_system_flip_publishes_the_new_scheme(make_spy, make_style_hints):
    style_hints = make_style_hints(Qt.ColorScheme.Light)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.effective_color_scheme_changed)

    style_hints.system_reports(Qt.ColorScheme.Dark)

    assert spy.count() == 1
    assert spy.at(0, 0) is DARK
    assert service.effective_color_scheme is DARK


def test_system_answer_resolving_to_the_same_scheme_publishes_nothing(make_spy, make_style_hints):
    # the system moves off Unknown, which Qt reports, but dark resolves to dark either way
    style_hints = make_style_hints(Qt.ColorScheme.Unknown)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.effective_color_scheme_changed)

    style_hints.system_reports(Qt.ColorScheme.Dark)

    assert spy.count() == 0
    assert service.effective_color_scheme is DARK


def test_system_flip_under_an_explicit_preference_publishes_nothing(settings_service, make_spy, make_style_hints):
    settings_service.color_scheme_preference = ColorSchemePreference.LIGHT
    style_hints = make_style_hints(Qt.ColorScheme.Light)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.effective_color_scheme_changed)

    style_hints.system_reports(Qt.ColorScheme.Dark)

    assert spy.count() == 0
    assert service.effective_color_scheme is LIGHT


def test_preference_change_to_explicit_pushes_into_qt_and_publishes(settings_service, make_spy, make_style_hints):
    style_hints = make_style_hints(Qt.ColorScheme.Light)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.effective_color_scheme_changed)

    settings_service.color_scheme_preference = ColorSchemePreference.DARK

    assert spy.count() == 1
    assert spy.at(0, 0) is DARK
    assert service.effective_color_scheme is DARK
    assert style_hints.calls == ["unset", "set Dark"]


def test_preference_change_back_to_system_unsets_and_follows_again(settings_service, make_spy, make_style_hints):
    settings_service.color_scheme_preference = ColorSchemePreference.DARK
    style_hints = make_style_hints(Qt.ColorScheme.Light)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.effective_color_scheme_changed)

    settings_service.color_scheme_preference = ColorSchemePreference.SYSTEM

    assert spy.count() == 1
    assert spy.at(0, 0) is LIGHT
    assert service.effective_color_scheme is LIGHT
    assert style_hints.calls == ["set Dark", "unset"]


def test_preference_change_keeping_the_scheme_pushes_into_qt_but_publishes_nothing(
    settings_service, make_spy, make_style_hints
):
    style_hints = make_style_hints(Qt.ColorScheme.Dark)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.effective_color_scheme_changed)

    settings_service.color_scheme_preference = ColorSchemePreference.DARK

    assert spy.count() == 0
    assert service.effective_color_scheme is DARK
    assert style_hints.calls == ["unset", "set Dark"]


def test_following_the_system_survives_a_preference_round_trip(settings_service, make_spy, make_style_hints):
    style_hints = make_style_hints(Qt.ColorScheme.Light)
    service = ColorSchemeService(style_hints)
    spy = make_spy(service.effective_color_scheme_changed)

    settings_service.color_scheme_preference = ColorSchemePreference.DARK
    settings_service.color_scheme_preference = ColorSchemePreference.SYSTEM
    style_hints.system_reports(Qt.ColorScheme.Dark)

    assert [spy.at(index, 0) for index in range(spy.count())] == [DARK, LIGHT, DARK]
    assert service.effective_color_scheme is DARK
