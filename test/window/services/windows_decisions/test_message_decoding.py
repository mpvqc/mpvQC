# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest

from mpvqc.window.services import read_hit_test_point


def pack_point(x: int, y: int) -> int:
    return ((y & 0xFFFF) << 16) | (x & 0xFFFF)


class PointCase(NamedTuple):
    name: str
    l_param: int
    expected: tuple[int, int]


@pytest.mark.parametrize(
    "case",
    [
        PointCase(name="origin", l_param=pack_point(0, 0), expected=(0, 0)),
        PointCase(name="primary_monitor", l_param=pack_point(640, 480), expected=(640, 480)),
        PointCase(name="monitor_left_of_primary", l_param=pack_point(-1280, 480), expected=(-1280, 480)),
        PointCase(name="monitor_above_primary", l_param=pack_point(640, -1080), expected=(640, -1080)),
        PointCase(name="monitor_left_of_and_above_primary", l_param=pack_point(-1, -1), expected=(-1, -1)),
        PointCase(name="largest_positive_coordinates", l_param=pack_point(32767, 32767), expected=(32767, 32767)),
        PointCase(name="smallest_negative_coordinates", l_param=pack_point(-32768, -32768), expected=(-32768, -32768)),
    ],
    ids=lambda case: case.name,
)
def test_cursor_point_unpacks_both_coordinates_signed(case: PointCase):
    assert read_hit_test_point(case.l_param) == case.expected
