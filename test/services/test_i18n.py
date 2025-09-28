# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from PySide6.QtCore import QLocale

from mpvqc.services import InternationalizationService
from mpvqc.services.i18n import create_locale_from


@pytest.fixture(scope="module")
def service() -> InternationalizationService:
    return InternationalizationService()


@pytest.fixture(scope="module", autouse=True)
def teardown(qt_app, service):
    yield
    service.retranslate(qt_app, QLocale.system().name())


def test_translation_override_works(qt_app, service):
    service.retranslate(qt_app, "es-ES")
    assert qt_app.translate("QPlatformTheme", "Reset") == "Reinicializar"

    service.retranslate(qt_app, "es-MX")
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
