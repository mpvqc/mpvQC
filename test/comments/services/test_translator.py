# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Generator

import pytest
from PySide6.QtCore import QTranslator

from mpvqc.application import MpvqcApplication
from mpvqc.comments.services import reverse_translate_comment_type, translate_comment_type


@pytest.fixture
def german(qt_app: MpvqcApplication) -> Generator[None]:
    translator = QTranslator()
    assert translator.load(":/i18n/de-DE.qm")
    qt_app.installTranslator(translator)
    yield
    qt_app.removeTranslator(translator)


@pytest.mark.parametrize(
    ("expected", "translated"),
    [
        ("Spelling", "Spelling"),
        ("Spelling", "Rechtschreibung"),
        ("Spelling", "איות"),  # Hebrew
        ("Spelling", "Typo"),
        ("Spelling", "Ortografía"),
        ("not-found", "not-found"),
        ("", ""),
    ],
)
def test_lookup_maps_translated_comment_types_to_english(expected, translated):
    assert expected == reverse_translate_comment_type(translated)


@pytest.mark.parametrize(
    ("expected", "comment_type"),
    [
        ("Rechtschreibung", "Spelling"),
        ("Timing", "Timing"),
        ("not-a-comment-type", "not-a-comment-type"),
        ("", ""),
    ],
)
@pytest.mark.usefixtures("german")
def test_translate_maps_comment_types_to_the_current_language(expected, comment_type):
    assert expected == translate_comment_type(comment_type)
