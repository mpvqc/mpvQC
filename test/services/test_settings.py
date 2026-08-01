# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import patch

import pytest
from PySide6.QtCore import QLocale

from mpvqc.appearance import AccentColor, Appearance, ThemeIdentifier
from mpvqc.services.settings import default_language


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


def test_accent_color_for_returns_none_when_nothing_stored(settings_service):
    assert settings_service.accent_color_for(ThemeIdentifier("material-you-dark")) is None


def test_set_accent_color_stores_one_value_per_theme(settings_service):
    dark = ThemeIdentifier("material-you-dark")
    light = ThemeIdentifier("material-you")

    settings_service.set_accent_color(dark, AccentColor("#3f51b5"))
    settings_service.set_accent_color(light, AccentColor("#ff5722"))

    assert settings_service.accent_color_for(dark) == "#3f51b5"
    assert settings_service.accent_color_for(light) == "#ff5722"


def test_set_accent_color_writes_into_the_theme_ini_section(settings_service, tmp_path):
    settings_service.set_accent_color(ThemeIdentifier("material-you"), AccentColor("#3f51b5"))
    settings_service.qsettings.sync()

    ini = (tmp_path / "test_settings.ini").read_text()
    theme_section = ini.split("[Theme]", 1)[1].split("[", 1)[0]
    # QSettings writes the sub-key separator as a backslash in INI files
    assert r"accent\material-you=#3f51b5" in theme_section


def test_appearance_projects_the_current_theme_and_its_stored_accent(settings_service):
    dark = ThemeIdentifier("material-you-dark")
    light = ThemeIdentifier("material-you")

    assert settings_service.appearance == Appearance(theme_identifier=dark, stored_accent=None)

    settings_service.set_accent_color(dark, AccentColor("#3f51b5"))
    assert settings_service.appearance == Appearance(theme_identifier=dark, stored_accent=AccentColor("#3f51b5"))

    settings_service.theme_identifier = str(light)
    assert settings_service.appearance == Appearance(theme_identifier=light, stored_accent=None)


def test_theme_write_emits_the_new_appearance(settings_service, make_spy):
    spy = make_spy(settings_service.appearance_changed)
    light = ThemeIdentifier("material-you")
    settings_service.set_accent_color(light, AccentColor("#ff5722"))
    spy.reset()

    settings_service.theme_identifier = str(light)

    assert spy.count() == 1
    assert spy.at(0, 0) == Appearance(theme_identifier=light, stored_accent=AccentColor("#ff5722"))

    settings_service.theme_identifier = str(light)
    assert spy.count() == 1


def test_current_theme_accent_write_emits_the_new_appearance_once(settings_service, make_spy):
    spy = make_spy(settings_service.appearance_changed)
    dark = ThemeIdentifier("material-you-dark")

    settings_service.set_accent_color(dark, AccentColor("#3f51b5"))

    assert spy.count() == 1
    assert spy.at(0, 0) == Appearance(theme_identifier=dark, stored_accent=AccentColor("#3f51b5"))

    settings_service.set_accent_color(dark, AccentColor("#3f51b5"))
    assert spy.count() == 1


def test_other_theme_accent_write_stores_silently(settings_service, make_spy):
    spy = make_spy(settings_service.appearance_changed)
    light = ThemeIdentifier("material-you")

    settings_service.set_accent_color(light, AccentColor("#ff5722"))

    assert spy.count() == 0
    assert settings_service.accent_color_for(light) == "#ff5722"


def test_multiple_property_changes(settings_service):
    settings_service.backup_interval = 30
    settings_service.theme_identifier = "test-theme"
    settings_service.time_display_mode = 1

    assert settings_service.backup_interval == 30
    assert settings_service.theme_identifier == "test-theme"
    assert settings_service.time_display_mode == 1
