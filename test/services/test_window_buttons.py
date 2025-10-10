# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.services.window_buttons import ButtonPreferences, GnomeDetector


@pytest.mark.parametrize(
    ("layout", "expected"),
    [
        ("appmenu:minimize,maximize,close", ButtonPreferences(True, True, True)),
        (":close", ButtonPreferences(False, False, True)),
        ("", ButtonPreferences(False, False, False)),
        ("minimize,close", ButtonPreferences(True, False, True)),
        ("MINIMIZE,MAXIMIZE,CLOSE", ButtonPreferences(True, True, True)),
    ],
)
def test_gnome_parse_button_layout(layout, expected):
    result = GnomeDetector.parse_button_layout(layout)
    assert result == expected
