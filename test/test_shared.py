# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pytest
from PySide6.QtCore import QUrl
from PySide6.QtGui import QFontMetricsF

from mpvqc.appearance.services import application_font
from mpvqc.shared import (
    calculate_label_width,
    format_milliseconds_to_string,
    format_milliseconds_to_subsecond_string,
    format_time_to_string,
    map_path_to_str,
    map_path_to_url,
    map_url_to_path,
    map_urls_to_paths,
    needs_long_format,
)


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0, False),
        (3599, False),
        (3600, True),
        (3601, True),
    ],
)
def test_needs_long_format_is_inclusive_at_one_hour(seconds, expected):
    assert needs_long_format(seconds) is expected


@pytest.mark.parametrize(
    ("expected", "input_seconds"),
    [
        ("00:00:00", 0),
        ("00:01:08", 68),
        ("00:16:39", 999),
        ("02:46:40", 10000),
    ],
)
def test_format_time_to_string_long(expected, input_seconds):
    actual = format_time_to_string(input_seconds, long_format=True)
    assert expected == actual


@pytest.mark.parametrize(
    ("expected", "input_seconds"),
    [
        ("00:00", 0),
        ("01:08", 68),
        ("16:39", 999),
    ],
)
def test_format_time_to_string_short(expected, input_seconds):
    actual = format_time_to_string(input_seconds, long_format=False)
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
def test_format_milliseconds_to_string(expected, input_milliseconds, long_format):
    actual = format_milliseconds_to_string(input_milliseconds, long_format=long_format)
    assert expected == actual


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


@pytest.fixture
def metrics(qt_app) -> QFontMetricsF:
    return QFontMetricsF(application_font())


def test_empty_input_yields_zero(metrics):
    assert calculate_label_width([], metrics) == 0


def test_empty_generator_yields_zero(metrics):
    empty: list[str] = []
    assert calculate_label_width((text for text in empty), metrics) == 0


def test_one_shot_generator_measures_like_a_list(metrics):
    expected = calculate_label_width(["i", "Wwwwwwwwww"], metrics)

    assert calculate_label_width((text for text in ["i", "Wwwwwwwwww"]), metrics) == expected


def test_width_is_the_advance_width_rounded_up(metrics):
    advance = metrics.horizontalAdvance("Translation")

    width = calculate_label_width(["Translation"], metrics)

    assert advance <= width < advance + 1


def test_widest_text_wins(metrics):
    widest = calculate_label_width(["Wwwwwwwwww"], metrics)

    assert calculate_label_width(["i", "Wwwwwwwwww"], metrics) == widest


@pytest.fixture
def detour(tmp_path) -> Path:
    """A path that only resolving collapses, so a mapper that skips it fails."""
    return tmp_path / "sub" / ".." / "video.mkv"


def test_map_url_to_path(detour):
    assert map_url_to_path(QUrl.fromLocalFile(f"{detour}")) == detour.resolve()


def test_map_urls_to_paths(detour, tmp_path):
    files = [detour, tmp_path / "sub" / ".." / "document.json"]
    urls = [QUrl.fromLocalFile(f"{file}") for file in files]
    assert map_urls_to_paths(urls) == [file.resolve() for file in files]


def test_map_path_to_url(detour):
    assert map_path_to_url(detour) == QUrl.fromLocalFile(f"{detour.resolve()}")


def test_map_path_to_url_makes_a_relative_path_absolute():
    url = map_path_to_url(Path("video.mkv"))
    assert Path(url.toLocalFile()).is_absolute()


def test_map_path_to_str(detour):
    assert map_path_to_str(detour) == f"{detour.resolve()}"
