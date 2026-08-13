# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import pytest

from mpvqc.importing.services import ClassifiedPaths, classify_paths


def _only_document(path: Path) -> ClassifiedPaths:
    return ClassifiedPaths(documents=(path,), videos=(), subtitles=())


def _only_video(path: Path) -> ClassifiedPaths:
    return ClassifiedPaths(documents=(), videos=(path,), subtitles=())


def _only_subtitle(path: Path) -> ClassifiedPaths:
    return ClassifiedPaths(documents=(), videos=(), subtitles=(path,))


class ClassifyCase(NamedTuple):
    name: str
    path: Path
    expected: ClassifiedPaths


CLASSIFY_CASES = [
    ClassifyCase(
        name="txt is a document",
        path=Path("/work/report.txt"),
        expected=_only_document(Path("/work/report.txt")),
    ),
    ClassifyCase(
        name="json is a document",
        path=Path("/work/notes.json"),
        expected=_only_document(Path("/work/notes.json")),
    ),
    ClassifyCase(
        name="uppercase document suffix",
        path=Path("/work/notes.JSON"),
        expected=_only_document(Path("/work/notes.JSON")),
    ),
    ClassifyCase(
        name="srt is a subtitle",
        path=Path("/work/subtitle.srt"),
        expected=_only_subtitle(Path("/work/subtitle.srt")),
    ),
    ClassifyCase(
        name="ass is a subtitle",
        path=Path("/work/subtitle.ass"),
        expected=_only_subtitle(Path("/work/subtitle.ass")),
    ),
    ClassifyCase(
        name="mixed-case subtitle suffix",
        path=Path("/work/other.SrT"),
        expected=_only_subtitle(Path("/work/other.SrT")),
    ),
    ClassifyCase(
        name="mkv falls back to video",
        path=Path("/movies/movie.mkv"),
        expected=_only_video(Path("/movies/movie.mkv")),
    ),
    ClassifyCase(
        name="unrecognized suffix falls back to video",
        path=Path("/movies/movie.webm"),
        expected=_only_video(Path("/movies/movie.webm")),
    ),
    ClassifyCase(
        name="no suffix falls back to video",
        path=Path("/movies/movie"),
        expected=_only_video(Path("/movies/movie")),
    ),
]


@pytest.mark.parametrize("case", CLASSIFY_CASES, ids=lambda c: c.name)
def test_classify_paths_by_kind(case: ClassifyCase) -> None:
    assert classify_paths([case.path]) == case.expected


def test_classify_paths_splits_a_mixed_bucket() -> None:
    documents = [Path("/work/report.txt"), Path("/work/notes.JSON")]
    subtitles = [Path("/work/subtitle.ass"), Path("/work/other.SrT")]
    videos = [Path("/movies/movie.mkv")]

    result = classify_paths([*documents, *subtitles, *videos])

    assert result == ClassifiedPaths(documents=tuple(documents), videos=tuple(videos), subtitles=tuple(subtitles))
