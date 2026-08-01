# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import patch

import pytest
from PySide6.QtCore import QLocale

from mpvqc.appearance import (
    AccentColor,
    Appearance,
    ColorSchemePreference,
    EffectiveColorScheme,
    ThemeAppearance,
    ThemeIdentifier,
)
from mpvqc.services import SettingsService
from mpvqc.services.settings import default_language


@pytest.fixture
def stale_theme_config(tmp_path, type_mapper):
    """A config written by a version that stored the theme identifier."""

    def _make() -> SettingsService:
        ini = tmp_path / "stale_settings.ini"
        ini.write_text(
            "[Theme]\nthemeIdentifier=material-you\naccent\\material-you=#3f51b5\n",
            encoding="utf-8",
        )
        return SettingsService(ini_file=type_mapper.map_path_to_str(ini))

    return _make


@pytest.mark.parametrize(
    ("locale_string", "expected"),
    [
        ("fr-FR", "fr-FR"),  # We have translations
        ("sw-TZ", "en-US"),  # We don't have translations
    ],
)
@patch("mpvqc.services.settings.LANGUAGES")
def test_default_language(mock_languages, locale_string, expected):
    class MockLanguage:
        def __init__(self, identifier):
            self.identifier = identifier

    mock_languages.__iter__.return_value = [MockLanguage("fr-FR"), MockLanguage("en-US"), MockLanguage("de-DE")]
    locale = QLocale(locale_string)

    result = default_language(locale)

    assert result == expected


def test_backup_enabled_default(settings_service):
    assert settings_service.backup_enabled


def test_backup_enabled_set_and_get(settings_service):
    settings_service.backup_enabled = False
    assert not settings_service.backup_enabled

    settings_service.backup_enabled = True
    assert settings_service.backup_enabled


def test_backup_enabled_signal_emission(settings_service, make_spy):
    spy = make_spy(settings_service.backup_enabled_changed)

    settings_service.backup_enabled = False
    assert spy.count() == 1
    assert spy.at(0, 0) is False

    settings_service.backup_enabled = False
    assert spy.count() == 1


def test_theme_identifier_default(settings_service):
    assert settings_service.theme_identifier == "material-you-dark"


def test_theme_identifier_set_and_get(settings_service):
    test_theme = "custom-theme"
    settings_service.theme_identifier = test_theme
    assert settings_service.theme_identifier == test_theme


def test_theme_identifier_signal_emission(settings_service, make_spy):
    spy = make_spy(settings_service.theme_identifier_changed)

    test_theme = "new-theme"
    settings_service.theme_identifier = test_theme
    assert spy.count() == 1
    assert spy.at(0, 0) == test_theme

    settings_service.theme_identifier = test_theme
    assert spy.count() == 1


def test_backup_interval_default(settings_service):
    assert settings_service.backup_interval == 60


def test_backup_interval_set_and_get(settings_service):
    test_interval = 120
    settings_service.backup_interval = test_interval
    assert settings_service.backup_interval == test_interval


def test_backup_interval_signal_emission(settings_service, make_spy):
    spy = make_spy(settings_service.backup_interval_changed)

    test_interval = 90
    settings_service.backup_interval = test_interval
    assert spy.count() == 1
    assert spy.at(0, 0) == test_interval

    settings_service.backup_interval = test_interval
    assert spy.count() == 1


def test_time_display_mode_default(settings_service):
    assert settings_service.time_display_mode == 3


def test_time_display_mode_set_and_get(settings_service):
    test_mode = 1
    settings_service.time_display_mode = test_mode
    assert settings_service.time_display_mode == test_mode


def test_time_display_mode_signal_emission(settings_service, make_spy):
    spy = make_spy(settings_service.time_display_mode_changed)

    test_mode = 2
    settings_service.time_display_mode = test_mode
    assert spy.count() == 1
    assert spy.at(0, 0) == test_mode

    settings_service.time_display_mode = test_mode
    assert spy.count() == 1


def test_theme_accent_color_for_returns_none_when_nothing_stored(settings_service):
    assert settings_service.theme_accent_color_for(ThemeIdentifier("material-you-dark")) is None


def test_set_theme_accent_color_stores_one_value_per_theme(settings_service):
    dark = ThemeIdentifier("material-you-dark")
    light = ThemeIdentifier("material-you")

    settings_service.set_theme_accent_color(dark, AccentColor("#3f51b5"))
    settings_service.set_theme_accent_color(light, AccentColor("#ff5722"))

    assert settings_service.theme_accent_color_for(dark) == "#3f51b5"
    assert settings_service.theme_accent_color_for(light) == "#ff5722"


def test_set_theme_accent_color_writes_into_the_theme_ini_section(settings_service, tmp_path):
    settings_service.set_theme_accent_color(ThemeIdentifier("material-you"), AccentColor("#3f51b5"))
    settings_service.qsettings.sync()

    ini = (tmp_path / "test_settings.ini").read_text()
    theme_section = ini.split("[Theme]", 1)[1].split("[", 1)[0]
    # QSettings writes the sub-key separator as a backslash in INI files
    assert r"accent\material-you=#3f51b5" in theme_section


def test_theme_appearance_projects_the_current_theme_and_its_stored_accent(settings_service):
    dark = ThemeIdentifier("material-you-dark")
    light = ThemeIdentifier("material-you")

    assert settings_service.theme_appearance == ThemeAppearance(theme_identifier=dark, stored_accent=None)

    settings_service.set_theme_accent_color(dark, AccentColor("#3f51b5"))
    assert settings_service.theme_appearance == ThemeAppearance(
        theme_identifier=dark, stored_accent=AccentColor("#3f51b5")
    )

    settings_service.theme_identifier = str(light)
    assert settings_service.theme_appearance == ThemeAppearance(theme_identifier=light, stored_accent=None)


def test_theme_write_emits_the_new_theme_appearance(settings_service, make_spy):
    spy = make_spy(settings_service.theme_appearance_changed)
    light = ThemeIdentifier("material-you")
    settings_service.set_theme_accent_color(light, AccentColor("#ff5722"))
    spy.reset()

    settings_service.theme_identifier = str(light)

    assert spy.count() == 1
    assert spy.at(0, 0) == ThemeAppearance(theme_identifier=light, stored_accent=AccentColor("#ff5722"))

    settings_service.theme_identifier = str(light)
    assert spy.count() == 1


def test_current_theme_accent_write_emits_the_theme_appearance_once(settings_service, make_spy):
    spy = make_spy(settings_service.theme_appearance_changed)
    dark = ThemeIdentifier("material-you-dark")

    settings_service.set_theme_accent_color(dark, AccentColor("#3f51b5"))

    assert spy.count() == 1
    assert spy.at(0, 0) == ThemeAppearance(theme_identifier=dark, stored_accent=AccentColor("#3f51b5"))

    settings_service.set_theme_accent_color(dark, AccentColor("#3f51b5"))
    assert spy.count() == 1


def test_set_theme_accent_color_none_clears_the_stored_entry(settings_service):
    dark = ThemeIdentifier("material-you-dark")
    settings_service.set_theme_accent_color(dark, AccentColor("#3f51b5"))

    settings_service.set_theme_accent_color(dark, None)

    assert settings_service.theme_accent_color_for(dark) is None


def test_clearing_the_current_theme_accent_emits_the_theme_appearance(settings_service, make_spy):
    dark = ThemeIdentifier("material-you-dark")
    settings_service.set_theme_accent_color(dark, AccentColor("#3f51b5"))
    spy = make_spy(settings_service.theme_appearance_changed)

    settings_service.set_theme_accent_color(dark, None)

    assert spy.count() == 1
    assert spy.at(0, 0) == ThemeAppearance(theme_identifier=dark, stored_accent=None)

    settings_service.set_theme_accent_color(dark, None)
    assert spy.count() == 1


def test_other_theme_accent_write_stores_silently(settings_service, make_spy):
    spy = make_spy(settings_service.theme_appearance_changed)
    light = ThemeIdentifier("material-you")

    settings_service.set_theme_accent_color(light, AccentColor("#ff5722"))

    assert spy.count() == 0
    assert settings_service.theme_accent_color_for(light) == "#ff5722"


def test_color_scheme_preference_defaults_to_system(settings_service):
    assert settings_service.color_scheme_preference is ColorSchemePreference.SYSTEM


@pytest.mark.parametrize(
    "preference",
    [ColorSchemePreference.SYSTEM, ColorSchemePreference.LIGHT, ColorSchemePreference.DARK],
)
def test_color_scheme_preference_set_and_get(settings_service, preference):
    settings_service.color_scheme_preference = preference

    assert settings_service.color_scheme_preference is preference


def test_color_scheme_preference_signal_emission(settings_service, make_spy):
    spy = make_spy(settings_service.color_scheme_preference_changed)

    settings_service.color_scheme_preference = ColorSchemePreference.LIGHT
    assert spy.count() == 1
    assert spy.at(0, 0) is ColorSchemePreference.LIGHT

    settings_service.color_scheme_preference = ColorSchemePreference.LIGHT
    assert spy.count() == 1


def test_color_scheme_preference_writes_into_the_appearance_ini_section(settings_service, tmp_path):
    settings_service.color_scheme_preference = ColorSchemePreference.LIGHT
    settings_service.qsettings.sync()

    ini = (tmp_path / "test_settings.ini").read_text()
    appearance_section = ini.split("[Appearance]", 1)[1].split("[", 1)[0]
    assert "colorSchemePreference=light" in appearance_section


def test_unreadable_color_scheme_preference_falls_back_to_system(settings_service):
    settings_service.qsettings.setValue("Appearance/colorSchemePreference", "sepia")

    assert settings_service.color_scheme_preference is ColorSchemePreference.SYSTEM


def test_accent_color_for_returns_none_when_nothing_stored(settings_service):
    assert settings_service.accent_color_for(EffectiveColorScheme.LIGHT) is None
    assert settings_service.accent_color_for(EffectiveColorScheme.DARK) is None


def test_set_accent_color_stores_one_value_per_color_scheme(settings_service):
    settings_service.set_accent_color(EffectiveColorScheme.LIGHT, AccentColor("#ff5722"))
    settings_service.set_accent_color(EffectiveColorScheme.DARK, AccentColor("#3f51b5"))

    assert settings_service.accent_color_for(EffectiveColorScheme.LIGHT) == "#ff5722"
    assert settings_service.accent_color_for(EffectiveColorScheme.DARK) == "#3f51b5"


def test_set_accent_color_none_clears_the_stored_entry(settings_service):
    settings_service.set_accent_color(EffectiveColorScheme.DARK, AccentColor("#3f51b5"))

    settings_service.set_accent_color(EffectiveColorScheme.DARK, None)

    assert settings_service.accent_color_for(EffectiveColorScheme.DARK) is None


def test_set_accent_color_writes_into_the_appearance_ini_section(settings_service, tmp_path):
    settings_service.set_accent_color(EffectiveColorScheme.LIGHT, AccentColor("#ff5722"))
    settings_service.qsettings.sync()

    ini = (tmp_path / "test_settings.ini").read_text()
    appearance_section = ini.split("[Appearance]", 1)[1].split("[", 1)[0]
    # QSettings writes the sub-key separator as a backslash in INI files
    assert r"accentColor\light=#ff5722" in appearance_section


def test_appearance_projects_the_preference_and_both_stored_accents(settings_service):
    assert settings_service.appearance == Appearance(
        color_scheme_preference=ColorSchemePreference.SYSTEM,
        light_accent_color=None,
        dark_accent_color=None,
    )

    settings_service.color_scheme_preference = ColorSchemePreference.DARK
    settings_service.set_accent_color(EffectiveColorScheme.LIGHT, AccentColor("#ff5722"))

    assert settings_service.appearance == Appearance(
        color_scheme_preference=ColorSchemePreference.DARK,
        light_accent_color=AccentColor("#ff5722"),
        dark_accent_color=None,
    )


def test_preference_write_emits_the_appearance(settings_service, make_spy):
    spy = make_spy(settings_service.appearance_changed)

    settings_service.color_scheme_preference = ColorSchemePreference.LIGHT

    assert spy.count() == 1
    assert spy.at(0, 0) == Appearance(
        color_scheme_preference=ColorSchemePreference.LIGHT,
        light_accent_color=None,
        dark_accent_color=None,
    )

    settings_service.color_scheme_preference = ColorSchemePreference.LIGHT
    assert spy.count() == 1


@pytest.mark.parametrize(
    "color_scheme",
    [EffectiveColorScheme.LIGHT, EffectiveColorScheme.DARK],
)
def test_accent_write_for_either_scheme_emits_the_appearance_once(settings_service, make_spy, color_scheme):
    spy = make_spy(settings_service.appearance_changed)

    settings_service.set_accent_color(color_scheme, AccentColor("#ff5722"))

    assert spy.count() == 1
    assert spy.at(0, 0).accent_color_for(color_scheme) == "#ff5722"

    settings_service.set_accent_color(color_scheme, AccentColor("#ff5722"))
    assert spy.count() == 1


def test_a_config_holding_only_stale_theme_keys_yields_appearance_defaults(stale_theme_config):
    service = stale_theme_config()
    # the legacy reader sees them, so the defaults below are a real observation
    assert service.theme_identifier == "material-you"

    assert service.appearance == Appearance(
        color_scheme_preference=ColorSchemePreference.SYSTEM,
        light_accent_color=None,
        dark_accent_color=None,
    )


def test_writing_the_appearance_leaves_stale_theme_keys_untouched(stale_theme_config, tmp_path):
    service = stale_theme_config()

    service.color_scheme_preference = ColorSchemePreference.LIGHT
    service.set_accent_color(EffectiveColorScheme.LIGHT, AccentColor("#ff5722"))
    service.qsettings.sync()

    ini = (tmp_path / "stale_settings.ini").read_text()
    assert "colorSchemePreference=light" in ini  # the file was rewritten
    theme_section = ini.split("[Theme]", 1)[1].split("[", 1)[0]
    assert "themeIdentifier=material-you" in theme_section
    assert r"accent\material-you=#3f51b5" in theme_section


def test_multiple_property_changes(settings_service):
    settings_service.backup_interval = 30
    settings_service.theme_identifier = "test-theme"
    settings_service.time_display_mode = 1

    assert settings_service.backup_interval == 30
    assert settings_service.theme_identifier == "test-theme"
    assert settings_service.time_display_mode == 1
