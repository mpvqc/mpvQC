# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import patch

import pytest
from PySide6.QtCore import QLocale

from mpvqc.i18n.services import create_locale_from, default_language


def test_translation_override_works(qt_app, internationalization_service):
    internationalization_service.retranslate(qt_app, "es-ES")
    assert qt_app.translate("QPlatformTheme", "Reset") == "Reinicializar"

    internationalization_service.retranslate(qt_app, "es-MX")
    assert qt_app.translate("QPlatformTheme", "Reset") == "Restablecer"


class LocaleCase(NamedTuple):
    name: str
    language_code: str
    expected_locale: QLocale


@pytest.mark.parametrize(
    "case",
    [
        LocaleCase(name="de-DE -> de-DE", language_code="de-DE", expected_locale=QLocale("de-DE")),
        LocaleCase(name="en-US -> en-US", language_code="en-US", expected_locale=QLocale("en-US")),
        LocaleCase(name="pt-PT -> pt-BR", language_code="pt-PT", expected_locale=QLocale("pt-BR")),
        LocaleCase(name="pt-BR -> pt-BR", language_code="pt-BR", expected_locale=QLocale("pt-BR")),
    ],
    ids=lambda case: case.name,
)
def test_locale_mapping(case: LocaleCase) -> None:
    result = create_locale_from(case.language_code)
    assert result == case.expected_locale


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
