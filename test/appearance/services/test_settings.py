# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.appearance.services import (
    AccentColor,
    AppearancePreference,
    Dark,
    FollowSystem,
    Light,
    NoPreference,
)

SYSTEM = FollowSystem()
LIGHT = Light()
DARK = Dark()
NO_PREFERENCE = NoPreference()


def test_color_scheme_preference_defaults_to_system(appearance_settings_service):
    assert appearance_settings_service.color_scheme_preference == SYSTEM


@pytest.mark.parametrize(
    "preference",
    [SYSTEM, LIGHT, DARK],
)
def test_color_scheme_preference_set_and_get(appearance_settings_service, preference):
    appearance_settings_service.color_scheme_preference = preference

    assert appearance_settings_service.color_scheme_preference == preference


def test_color_scheme_preference_writes_into_the_appearance_ini_section(appearance_settings_service, ini_section):
    appearance_settings_service.color_scheme_preference = LIGHT

    assert ini_section("Appearance")["colorSchemePreference"] == "light"


def test_unreadable_color_scheme_preference_falls_back_to_system(appearance_settings_service, settings_file):
    settings_file.qsettings.setValue("Appearance/colorSchemePreference", "sepia")

    assert appearance_settings_service.color_scheme_preference == SYSTEM


def test_accent_color_preference_reports_no_preference_when_nothing_stored(appearance_settings_service):
    assert appearance_settings_service.appearance_preference.accent_color_preference_for(LIGHT) == NO_PREFERENCE
    assert appearance_settings_service.appearance_preference.accent_color_preference_for(DARK) == NO_PREFERENCE


def test_set_accent_color_preference_stores_one_value_per_color_scheme(appearance_settings_service):
    appearance_settings_service.set_accent_color_preference(LIGHT, AccentColor("#ff5722"))
    appearance_settings_service.set_accent_color_preference(DARK, AccentColor("#3f51b5"))

    assert appearance_settings_service.appearance_preference.accent_color_preference_for(LIGHT) == AccentColor(
        "#ff5722"
    )
    assert appearance_settings_service.appearance_preference.accent_color_preference_for(DARK) == AccentColor("#3f51b5")


def test_set_accent_color_preference_to_no_preference_clears_the_stored_entry(
    appearance_settings_service, settings_file, make_spy
):
    appearance_settings_service.set_accent_color_preference(DARK, AccentColor("#3f51b5"))
    spy = make_spy(appearance_settings_service.appearance_preference_changed)

    appearance_settings_service.set_accent_color_preference(DARK, NO_PREFERENCE)
    appearance_settings_service.set_accent_color_preference(DARK, NO_PREFERENCE)

    assert appearance_settings_service.appearance_preference.accent_color_preference_for(DARK) == NO_PREFERENCE
    assert not settings_file.qsettings.contains("Appearance/accentColor/dark")
    assert spy.count() == 1


def test_set_accent_color_preference_writes_into_the_appearance_ini_section(appearance_settings_service, ini_section):
    appearance_settings_service.set_accent_color_preference(LIGHT, AccentColor("#ff5722"))

    # QSettings writes the sub-key separator as a backslash in INI files
    assert ini_section("Appearance")[r"accentColor\light"] == "#ff5722"


def test_appearance_preference_projects_the_color_scheme_preference_and_both_stored_accents(
    appearance_settings_service,
):
    assert appearance_settings_service.appearance_preference == AppearancePreference(
        color_scheme_preference=SYSTEM,
        light_accent_color_preference=NO_PREFERENCE,
        dark_accent_color_preference=NO_PREFERENCE,
    )

    appearance_settings_service.color_scheme_preference = DARK
    appearance_settings_service.set_accent_color_preference(LIGHT, AccentColor("#ff5722"))

    assert appearance_settings_service.appearance_preference == AppearancePreference(
        color_scheme_preference=DARK,
        light_accent_color_preference=AccentColor("#ff5722"),
        dark_accent_color_preference=NO_PREFERENCE,
    )


def test_preference_write_emits_the_appearance_preference(appearance_settings_service, make_spy):
    spy = make_spy(appearance_settings_service.appearance_preference_changed)

    appearance_settings_service.color_scheme_preference = LIGHT

    assert spy.count() == 1
    assert spy.at(0, 0) == AppearancePreference(
        color_scheme_preference=LIGHT,
        light_accent_color_preference=NO_PREFERENCE,
        dark_accent_color_preference=NO_PREFERENCE,
    )

    appearance_settings_service.color_scheme_preference = LIGHT
    assert spy.count() == 1


def test_restore_writes_every_key_before_emitting_once(appearance_settings_service, settings_file, make_spy):
    appearance_settings_service.color_scheme_preference = DARK
    appearance_settings_service.set_accent_color_preference(LIGHT, AccentColor("#ff5722"))
    baseline = appearance_settings_service.appearance_preference
    appearance_settings_service.color_scheme_preference = LIGHT
    appearance_settings_service.set_accent_color_preference(LIGHT, AccentColor("#3f51b5"))
    appearance_settings_service.set_accent_color_preference(DARK, AccentColor("#009688"))
    spy = make_spy(appearance_settings_service.appearance_preference_changed)
    deliveries = []
    store = settings_file.qsettings
    appearance_settings_service.appearance_preference_changed.connect(
        lambda preference: deliveries.append(
            (
                preference,
                appearance_settings_service.appearance_preference,
                store.value("Appearance/colorSchemePreference"),
                store.value("Appearance/accentColor/light"),
                store.contains("Appearance/accentColor/dark"),
            )
        )
    )

    appearance_settings_service.restore(baseline)

    assert spy.count() == 1
    assert spy.at(0, 0) == baseline
    assert appearance_settings_service.appearance_preference == baseline
    assert deliveries == [(baseline, baseline, "dark", "#ff5722", False)]


def test_restore_of_what_is_already_stored_emits_nothing(appearance_settings_service, make_spy):
    appearance_settings_service.color_scheme_preference = DARK
    spy = make_spy(appearance_settings_service.appearance_preference_changed)

    appearance_settings_service.restore(appearance_settings_service.appearance_preference)

    assert spy.count() == 0


@pytest.mark.parametrize(
    "color_scheme",
    [LIGHT, DARK],
    ids=["light", "dark"],
)
def test_accent_write_for_either_scheme_emits_the_appearance_preference_once(
    appearance_settings_service, make_spy, color_scheme
):
    spy = make_spy(appearance_settings_service.appearance_preference_changed)

    appearance_settings_service.set_accent_color_preference(color_scheme, AccentColor("#ff5722"))

    assert spy.count() == 1
    assert spy.at(0, 0).accent_color_preference_for(color_scheme) == AccentColor("#ff5722")

    appearance_settings_service.set_accent_color_preference(color_scheme, AccentColor("#ff5722"))
    assert spy.count() == 1
