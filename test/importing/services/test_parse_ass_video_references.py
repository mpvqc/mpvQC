# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from mpvqc.importing.services import parse_ass_video_references

ass_lines = st.one_of(st.text(), st.text().map(lambda path: f"Video File:{path}"))


def test_parse_ass_video_references_empty_content():
    assert parse_ass_video_references("") == ()


def test_parse_ass_video_references_without_a_video_file_line():
    content = "[Script Info]\n\n[Aegisub Project Garbage]\n"

    assert parse_ass_video_references(content) == ()


def test_parse_ass_video_references_in_script_info():
    content = "[Script Info]\nVideo File: /videos/movie.mkv\n\n[Aegisub Project Garbage]\n"

    assert parse_ass_video_references(content) == (Path("/videos/movie.mkv"),)


def test_parse_ass_video_references_in_aegisub_project_garbage():
    content = "[Aegisub Project Garbage]\nVideo AR Mode: 4\nVideo File: /videos/movie.mkv\nScroll Position: 0\n"

    assert parse_ass_video_references(content) == (Path("/videos/movie.mkv"),)


def test_parse_ass_video_references_returns_every_reference_in_order():
    content = (
        "[Script Info]\nVideo File: /videos/first.mkv\n\n[Aegisub Project Garbage]\nVideo File: /videos/second.mkv\n"
    )

    assert parse_ass_video_references(content) == (Path("/videos/first.mkv"), Path("/videos/second.mkv"))


def test_parse_ass_video_references_keeps_a_relative_path_relative():
    content = "[Script Info]\nVideo File: video.mkv\n"

    assert parse_ass_video_references(content) == (Path("video.mkv"),)


def test_parse_ass_video_references_skips_a_line_with_no_path():
    content = "[Script Info]\nVideo File: \n"

    assert parse_ass_video_references(content) == ()


def test_parse_ass_video_references_requires_the_exact_prefix():
    content = "[Script Info]\nvideo file: /videos/movie.mkv\n"

    assert parse_ass_video_references(content) == ()


def test_parse_ass_video_references_on_malformed_content_never_raises():
    assert parse_ass_video_references("not a subtitle at all\n\x00�") == ()


@pytest.mark.fuzz
@given(st.one_of(st.text(), st.lists(ass_lines).map("\n".join)))
def test_parse_ass_video_references_never_raises_on_any_text(content: str):
    references = parse_ass_video_references(content)

    assert isinstance(references, tuple)
    assert all(isinstance(reference, Path) for reference in references)
