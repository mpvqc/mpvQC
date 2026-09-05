# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import patch

import pytest
from PySide6.QtCore import QLocale

from mpvqc.i18n.services import create_locale_from, default_language


def test_translation_override_works(qt_app, internationalization_service):
    internationalization_service.retranslate(qt_app, "es-ES")
    assert qt_app.translate("QPlatformTheme", "Reset") == "Reinicializar"

    internationalization_service.retranslate(qt_app, "es-MX")
    assert qt_app.translate("QPlatformTheme", "Reset") == "Restablecer"


@pytest.mark.parametrize(
    ("language_code", "expected_locale"),
    [
        ("de-DE", QLocale("de-DE")),
        ("en-US", QLocale("en-US")),
        ("pt-PT", QLocale("pt-BR")),
        ("pt-BR", QLocale("pt-BR")),
    ],
    ids=[
        "de-DE -> de-DE",
        "en-US -> en-US",
        "pt-PT -> pt-BR",
        "pt-BR -> pt-BR",
    ],
)
def test_locale_mapping(language_code: str, expected_locale: QLocale) -> None:
    result = create_locale_from(language_code)
    assert result == expected_locale


@pytest.mark.parametrize(
    ("locale_string", "expected"),
    [
        ("fr-FR", "fr-FR"),  # We have translations
        ("sw-TZ", "en-US"),  # We don't have translations
    ],
)
@patch("mpvqc.i18n.services.languages.LANGUAGES")
def test_default_language(mock_languages, locale_string, expected):
    class MockLanguage:
        def __init__(self, identifier):
            self.identifier = identifier

    mock_languages.__iter__.return_value = [MockLanguage("fr-FR"), MockLanguage("en-US"), MockLanguage("de-DE")]
    locale = QLocale(locale_string)

    result = default_language(locale)

    assert result == expected
