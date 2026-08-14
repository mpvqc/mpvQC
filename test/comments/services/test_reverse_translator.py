# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.comments.services import reverse_translate


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
    assert expected == reverse_translate(translated)
