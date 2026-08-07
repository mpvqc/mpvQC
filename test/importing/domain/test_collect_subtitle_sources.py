# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path

from mpvqc.importing.domain import SubtitleSource, collect_subtitle_sources

SUB_A = Path("/work/a.en.srt")
SUB_B = Path("/work/b.en.srt")


def test_explicit_subtitle_gets_explicit_flag() -> None:
    result = collect_subtitle_sources(explicitly_provided=[SUB_A], found_in_document=[])
    assert result == (SubtitleSource(path=SUB_A, explicitly_provided=True),)


def test_document_subtitle_gets_document_flag() -> None:
    result = collect_subtitle_sources(explicitly_provided=[], found_in_document=[SUB_A])
    assert result == (SubtitleSource(path=SUB_A, found_in_document=True),)


def test_same_path_from_both_origins_is_one_record_with_both_flags() -> None:
    result = collect_subtitle_sources(explicitly_provided=[SUB_A], found_in_document=[SUB_A])
    assert result == (SubtitleSource(path=SUB_A, explicitly_provided=True, found_in_document=True),)


def test_duplicate_paths_within_an_origin_collapse() -> None:
    result = collect_subtitle_sources(explicitly_provided=[SUB_A, SUB_A], found_in_document=[])
    assert result == (SubtitleSource(path=SUB_A, explicitly_provided=True),)


def test_sources_keep_first_seen_order_explicit_before_document() -> None:
    result = collect_subtitle_sources(explicitly_provided=[SUB_B], found_in_document=[SUB_A])
    assert result == (
        SubtitleSource(path=SUB_B, explicitly_provided=True),
        SubtitleSource(path=SUB_A, found_in_document=True),
    )
