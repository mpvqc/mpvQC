# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from PySide6.QtCore import QLocale

from mpvqc.services.i18n import create_locale_from


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
