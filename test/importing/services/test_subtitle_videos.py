# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from mpvqc.importing.services import find_videos_in_subtitles

if TYPE_CHECKING:
    from pathlib import Path


def write_subtitle(tmp_path: Path, name: str, content: str) -> Path:
    file_path = tmp_path / name
    file_path.write_text(content, encoding="utf-8-sig")
    return file_path


@pytest.mark.parametrize("suffix", [".ass", ".ssa"])
def test_reads_ass_and_ssa_subtitles(tmp_path: Path, suffix: str) -> None:
    video = tmp_path / "video.mp4"
    video.touch()
    subtitle = write_subtitle(tmp_path, f"subtitle{suffix}", f"[Script Info]\nVideo File: {video}\n")

    assert find_videos_in_subtitles([subtitle]) == (video,)


def test_ignores_a_suffix_that_cannot_carry_a_video_reference(tmp_path: Path) -> None:
    video = tmp_path / "video.mp4"
    video.touch()
    subtitle = write_subtitle(tmp_path, "subtitle.srt", f"[Script Info]\nVideo File: {video}\n")

    assert find_videos_in_subtitles([subtitle]) == ()


def test_skips_a_missing_subtitle(tmp_path: Path) -> None:
    missing = tmp_path / "missing.ass"

    assert find_videos_in_subtitles([missing]) == ()


def test_skips_a_subtitle_with_invalid_encoding(tmp_path: Path) -> None:
    subtitle = tmp_path / "subtitle.ass"
    subtitle.write_bytes(b"[Script Info]\n\xff\xfe not valid utf-8")

    assert find_videos_in_subtitles([subtitle]) == ()


def test_joins_a_relative_reference_against_the_subtitle_directory(tmp_path: Path) -> None:
    video = tmp_path / "video.mp4"
    video.touch()
    subtitle = write_subtitle(tmp_path, "subtitle.ass", "[Script Info]\nVideo File: video.mp4\n")

    assert find_videos_in_subtitles([subtitle]) == (video,)


def test_keeps_the_first_reference_that_exists(tmp_path: Path) -> None:
    video_1 = tmp_path / "video_1.mp4"
    video_1.touch()
    video_2 = tmp_path / "video_2.mp4"
    video_2.touch()
    content = f"[Script Info]\nVideo File: {video_1}\n\n[Aegisub Project Garbage]\nVideo File: {video_2}\n"
    subtitle = write_subtitle(tmp_path, "subtitle.ass", content)

    assert find_videos_in_subtitles([subtitle]) == (video_1,)


def test_falls_through_a_dead_first_reference_to_a_live_second(tmp_path: Path) -> None:
    dead = tmp_path / "missing.mp4"
    live = tmp_path / "video.mp4"
    live.touch()
    content = f"[Script Info]\nVideo File: {dead}\n\n[Aegisub Project Garbage]\nVideo File: {live}\n"
    subtitle = write_subtitle(tmp_path, "subtitle.ass", content)

    assert find_videos_in_subtitles([subtitle]) == (live,)


def test_finds_nothing_when_every_reference_is_dead(tmp_path: Path) -> None:
    dead = tmp_path / "missing.mp4"
    subtitle = write_subtitle(tmp_path, "subtitle.ass", f"[Script Info]\nVideo File: {dead}\n")

    assert find_videos_in_subtitles([subtitle]) == ()
