# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

from mpvqc.importing.domain import SUBTITLE_WITH_VIDEO_REFERENCE_EXTENSIONS, parse_video_references


def test_parse_video_references_empty_content():
    assert parse_video_references("") == ()


def test_parse_video_references_without_a_video_file_line():
    content = "[Script Info]\n\n[Aegisub Project Garbage]\n"

    assert parse_video_references(content) == ()


def test_parse_video_references_in_script_info():
    content = "[Script Info]\nVideo File: /videos/movie.mkv\n\n[Aegisub Project Garbage]\n"

    assert parse_video_references(content) == (Path("/videos/movie.mkv"),)


def test_parse_video_references_in_aegisub_project_garbage():
    content = "[Aegisub Project Garbage]\nVideo AR Mode: 4\nVideo File: /videos/movie.mkv\nScroll Position: 0\n"

    assert parse_video_references(content) == (Path("/videos/movie.mkv"),)


def test_parse_video_references_returns_every_reference_in_order():
    content = (
        "[Script Info]\nVideo File: /videos/first.mkv\n\n[Aegisub Project Garbage]\nVideo File: /videos/second.mkv\n"
    )

    assert parse_video_references(content) == (Path("/videos/first.mkv"), Path("/videos/second.mkv"))


def test_parse_video_references_keeps_a_relative_path_relative():
    content = "[Script Info]\nVideo File: video.mkv\n"

    assert parse_video_references(content) == (Path("video.mkv"),)


def test_parse_video_references_skips_a_line_with_no_path():
    content = "[Script Info]\nVideo File: \n"

    assert parse_video_references(content) == ()


def test_parse_video_references_requires_the_exact_prefix():
    content = "[Script Info]\nvideo file: /videos/movie.mkv\n"

    assert parse_video_references(content) == ()


def test_parse_video_references_on_malformed_content_never_raises():
    assert parse_video_references("not a subtitle at all\n\x00�") == ()


def test_subtitle_with_video_reference_extensions():
    assert {".ass", ".ssa"} == SUBTITLE_WITH_VIDEO_REFERENCE_EXTENSIONS
