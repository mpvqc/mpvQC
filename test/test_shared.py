# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pytest
from PySide6.QtCore import QUrl

from mpvqc.shared import (
    format_milliseconds_to_subsecond_string,
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
