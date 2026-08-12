# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import patch

import pytest
from PySide6.QtCore import QLocale

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
