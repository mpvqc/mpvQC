# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.shared import format_milliseconds_to_subsecond_string


@pytest.mark.parametrize(
    ("expected", "input_milliseconds"),
    [
        ("00:00:00.000", 0),
        ("00:01:08.001", 68 * 1000 + 1),
        ("00:15:29.340", (15 * 60 + 29) * 1000 + 340),
        ("02:46:40.999", 10000 * 1000 + 999),
        ("99:59:59.999", 359999 * 1000 + 999),
        ("99:59:59.999", 359999 * 1000 + 1000),
        ("99:59:59.999", 100 * 3600 * 1000),
    ],
)
def test_format_milliseconds_to_subsecond_string(expected, input_milliseconds):
    actual = format_milliseconds_to_subsecond_string(input_milliseconds)
    assert expected == actual
