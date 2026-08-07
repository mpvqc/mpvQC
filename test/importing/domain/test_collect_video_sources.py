# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path

from mpvqc.importing.domain import VideoSource, collect_video_sources

VIDEO_A = Path("/movies/a.mp4")
VIDEO_B = Path("/movies/b.mp4")
VIDEO_C = Path("/movies/c.mp4")


def test_explicit_video_gets_explicit_flag() -> None:
    result = collect_video_sources(explicitly_provided=[VIDEO_A], found_in_document=[], found_in_subtitle=[])
    assert result == (VideoSource(path=VIDEO_A, explicitly_provided=True),)


def test_document_video_gets_document_flag() -> None:
    result = collect_video_sources(explicitly_provided=[], found_in_document=[VIDEO_A], found_in_subtitle=[])
    assert result == (VideoSource(path=VIDEO_A, found_in_document=True),)


def test_subtitle_video_gets_subtitle_flag() -> None:
    result = collect_video_sources(explicitly_provided=[], found_in_document=[], found_in_subtitle=[VIDEO_A])
    assert result == (VideoSource(path=VIDEO_A, found_in_subtitle=True),)


def test_same_path_from_every_origin_is_one_record_with_every_flag() -> None:
    result = collect_video_sources(
        explicitly_provided=[VIDEO_A], found_in_document=[VIDEO_A], found_in_subtitle=[VIDEO_A]
    )
    assert result == (
        VideoSource(path=VIDEO_A, explicitly_provided=True, found_in_document=True, found_in_subtitle=True),
    )


def test_duplicate_paths_within_an_origin_collapse() -> None:
    result = collect_video_sources(explicitly_provided=[VIDEO_A, VIDEO_A], found_in_document=[], found_in_subtitle=[])
    assert result == (VideoSource(path=VIDEO_A, explicitly_provided=True),)


def test_collapsed_record_keeps_first_seen_position() -> None:
    result = collect_video_sources(
        explicitly_provided=[VIDEO_A, VIDEO_B], found_in_document=[VIDEO_A], found_in_subtitle=[]
    )
    assert result == (
        VideoSource(path=VIDEO_A, explicitly_provided=True, found_in_document=True),
        VideoSource(path=VIDEO_B, explicitly_provided=True),
    )


def test_sources_keep_first_seen_order_explicit_before_document_before_subtitle() -> None:
    result = collect_video_sources(
        explicitly_provided=[VIDEO_B], found_in_document=[VIDEO_A], found_in_subtitle=[VIDEO_C]
    )
    assert result == (
        VideoSource(path=VIDEO_B, explicitly_provided=True),
        VideoSource(path=VIDEO_A, found_in_document=True),
        VideoSource(path=VIDEO_C, found_in_subtitle=True),
    )
