# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import patch

import pytest
from PySide6.QtCore import QLocale

from mpvqc.services.settings import get_default_language


@pytest.fixture(autouse=True)
def clear_cache():
    get_default_language.cache_clear()
    yield
    get_default_language.cache_clear()


@pytest.mark.parametrize(
    ("locale_string", "expected"),
    [
        ("fr-FR", "fr-FR"),  # We have translations
        ("sw-TZ", "en-US"),  # We don't have translations
    ],
)
@patch("mpvqc.models.languages.LANGUAGES")
def test_get_default_language(mock_languages, locale_string, expected):
    class MockLanguage:
        def __init__(self, identifier):
            self.identifier = identifier

    mock_languages.__iter__.return_value = [MockLanguage("fr-FR"), MockLanguage("en-US"), MockLanguage("de-DE")]
    locale = QLocale(locale_string)

    result = get_default_language(locale)

    assert result == expected


def test_backup_enabled_default(settings_service):
    assert settings_service.backup_enabled is True


def test_backup_enabled_set_and_get(settings_service):
    settings_service.backup_enabled = False
    assert settings_service.backup_enabled is False

    settings_service.backup_enabled = True
    assert settings_service.backup_enabled is True


def test_backup_enabled_signal_emission(settings_service, make_spy):
    spy = make_spy(settings_service.backupEnabledChanged)

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
    spy = make_spy(settings_service.themeIdentifierChanged)

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
    spy = make_spy(settings_service.backupIntervalChanged)

    test_interval = 90
    settings_service.backup_interval = test_interval
    assert spy.count() == 1
    assert spy.at(0, 0) == test_interval

    settings_service.backup_interval = test_interval
    assert spy.count() == 1


def test_time_format_default(settings_service):
    assert settings_service.time_format == 3


def test_time_format_set_and_get(settings_service):
    test_format = 1
    settings_service.time_format = test_format
    assert settings_service.time_format == test_format


def test_time_format_signal_emission(settings_service, make_spy):
    spy = make_spy(settings_service.timeFormatChanged)

    test_format = 2
    settings_service.time_format = test_format
    assert spy.count() == 1
    assert spy.at(0, 0) == test_format

    settings_service.time_format = test_format
    assert spy.count() == 1


def test_multiple_property_changes(settings_service):
    settings_service.backup_interval = 30
    settings_service.theme_identifier = "test-theme"
    settings_service.time_format = 1

    assert settings_service.backup_interval == 30
    assert settings_service.theme_identifier == "test-theme"
    assert settings_service.time_format == 1
