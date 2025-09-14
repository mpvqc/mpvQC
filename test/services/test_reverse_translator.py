# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.services import ReverseTranslatorService


@pytest.fixture
def service() -> ReverseTranslatorService:
    return ReverseTranslatorService()


@pytest.mark.parametrize(
    ("expected", "translated"),
    [
        ("Spelling", "Spelling"),
        ("Spelling", "Rechtschreibung"),
        ("Spelling", "איות"),
        ("Spelling", "Typo"),
        ("Spelling", "Ortografía"),
        ("not-found", "not-found"),
    ],
)
def test_lookup2(service, expected, translated):
    assert expected == service.lookup(translated)
