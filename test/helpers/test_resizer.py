# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest

from mpvqc.helpers.resizer import calculate_horizontal_layout_sizes, calculate_vertical_layout_sizes

HEADER_HEIGHT = 40
BORDER_SIZE = 6
HANDLE_WIDTH = 6
HANDLE_HEIGHT = 6


class VerticalLayoutTestCase(NamedTuple):
    video_width: int
    video_height: int
    table_height: int
    available_height: int
    expected_window_width: int
    expected_window_height: int
    expected_table_width: int
    expected_table_height: int


@pytest.mark.parametrize(
    "test_case",
    [
        VerticalLayoutTestCase(
            video_width=854,
            video_height=480,
            table_height=200,
            available_height=int(1440 * 0.95),
            expected_window_width=866,
            expected_window_height=738,
            expected_table_width=854,
            expected_table_height=200,
        ),
        VerticalLayoutTestCase(
            video_width=854,
            video_height=480,
            table_height=900,
            available_height=int(1440 * 0.95),
            expected_window_width=866,
            expected_window_height=1368,
            expected_table_width=854,
            expected_table_height=830,
        ),
    ],
)
def test_calculate_vertical_layout_sizes(test_case: VerticalLayoutTestCase):
    window_width, window_height, table_width, table_height = calculate_vertical_layout_sizes(
        video_width=test_case.video_width,
        video_height=test_case.video_height,
        header_height=HEADER_HEIGHT,
        border_size=BORDER_SIZE,
        handle_height=HANDLE_HEIGHT,
        table_height=test_case.table_height,
        available_height=test_case.available_height,
    )

    assert window_width == test_case.expected_window_width
    assert window_height == test_case.expected_window_height
    assert table_width == test_case.expected_table_width
    assert table_height == test_case.expected_table_height


class HorizontalLayoutTestCase(NamedTuple):
    video_width: int
    video_height: int
    table_width: int
    available_width: int
    expected_window_width: int
    expected_window_height: int
    expected_table_width: int
    expected_table_height: int


@pytest.mark.parametrize(
    "test_case",
    [
        HorizontalLayoutTestCase(
            video_width=854,
            video_height=480,
            table_width=200,
            available_width=int(2560 * 0.95),
            expected_window_width=1072,
            expected_window_height=532,
            expected_table_width=200,
            expected_table_height=480,
        ),
        HorizontalLayoutTestCase(
            video_width=854,
            video_height=480,
            table_width=900,
            available_width=int(2560 * 0.95),
            expected_window_width=1772,
            expected_window_height=532,
            expected_table_width=900,
            expected_table_height=480,
        ),
    ],
)
def test_calculate_horizontal_layout_sizes(test_case: HorizontalLayoutTestCase):
    window_width, window_height, table_width, table_height = calculate_horizontal_layout_sizes(
        video_width=test_case.video_width,
        video_height=test_case.video_height,
        header_height=HEADER_HEIGHT,
        border_size=BORDER_SIZE,
        handle_width=HANDLE_WIDTH,
        table_width=test_case.table_width,
        available_width=test_case.available_width,
    )

    assert window_width == test_case.expected_window_width
    assert window_height == test_case.expected_window_height
    assert table_width == test_case.expected_table_width
    assert table_height == test_case.expected_table_height
