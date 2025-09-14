# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.services import TimeFormatterService


@pytest.fixture(scope="module")
def service():
    return TimeFormatterService()


@pytest.mark.parametrize(
    ("expected", "input_seconds"),
    [
        ("00:00:00", 0),
        ("00:01:08", 68),
        ("00:16:39", 999),
        ("02:46:40", 10000),
    ],
)
def test_format_time_to_string_long(service, expected, input_seconds):
    actual = service.format_time_to_string(input_seconds, long_format=True)
    assert expected == actual


@pytest.mark.parametrize(
    ("expected", "input_seconds"),
    [
        ("00:00", 0),
        ("01:08", 68),
        ("16:39", 999),
    ],
)
def test_format_time_to_string_short(service, expected, input_seconds):
    actual = service.format_time_to_string(input_seconds, long_format=False)
    assert expected == actual
