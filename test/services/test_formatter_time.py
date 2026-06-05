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


@pytest.mark.parametrize(
    ("expected", "input_milliseconds", "long_format"),
    [
        ("00:00:00", 0 * 1000, True),
        ("00:01:08", 68 * 1000, True),
        ("02:46:40", 10000 * 1000, True),
        ("00:01:08", 68 * 1000 + 999, True),
        ("01:08", 68 * 1000, False),
    ],
)
def test_format_milliseconds_to_string(service, expected, input_milliseconds, long_format):
    actual = service.format_milliseconds_to_string(input_milliseconds, long_format=long_format)
    assert expected == actual


@pytest.mark.parametrize(
    ("expected", "input_milliseconds"),
    [
        ("00:00:00.000", 0),
        ("00:01:08.001", 68 * 1000 + 1),
        ("00:15:29.340", (15 * 60 + 29) * 1000 + 340),
        ("02:46:40.999", 10000 * 1000 + 999),
        ("99:59:59.999", 359999 * 1000 + 999),
    ],
)
def test_format_milliseconds_to_subsecond_string(service, expected, input_milliseconds):
    actual = service.format_milliseconds_to_subsecond_string(input_milliseconds)
    assert expected == actual


@pytest.mark.parametrize(
    ("expected_milliseconds", "input_string"),
    [
        (0 * 1000, "00:00:00"),
        (68 * 1000, "00:01:08"),
        (10000 * 1000, "02:46:40"),
        (118800 * 1000, "33:00:00"),
    ],
)
def test_parse_string_to_milliseconds(service, expected_milliseconds, input_string):
    actual = service.parse_string_to_milliseconds(input_string)
    assert expected_milliseconds == actual


@pytest.mark.parametrize(
    ("expected_milliseconds", "input_string"),
    [
        (0, "00:00:00.000"),
        (68 * 1000 + 1, "00:01:08.001"),
        ((15 * 60 + 29) * 1000 + 340, "00:15:29.340"),
        (10000 * 1000 + 999, "02:46:40.999"),
        (359999 * 1000 + 999, "99:59:59.999"),
    ],
)
def test_parse_subsecond_string_to_milliseconds(service, expected_milliseconds, input_string):
    actual = service.parse_subsecond_string_to_milliseconds(input_string)
    assert expected_milliseconds == actual
