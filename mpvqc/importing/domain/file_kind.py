# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


DOCUMENT_EXTENSIONS: frozenset[str] = frozenset(
    {
        ".txt",
        ".json",
    }
)

SUBTITLE_EXTENSIONS: frozenset[str] = frozenset(
    {
        ".aqt",
        ".ass",
        ".idx",
        ".js",
        ".jss",
        ".mks",
        ".rt",
        ".scc",
        ".smi",
        ".srt",
        ".ssa",
        ".sub",
        ".sup",
        ".utf",
        ".utf-8",
        ".utf8",
        ".vtt",
    }
)


@dataclass(frozen=True, slots=True)
class ClassifiedPaths:
    documents: tuple[Path, ...]
    videos: tuple[Path, ...]
    subtitles: tuple[Path, ...]


def classify_paths(paths: list[Path]) -> ClassifiedPaths:
    documents = []
    videos = []
    subtitles = []

    for path in paths:
        suffix = path.suffix.lower()
        if suffix in DOCUMENT_EXTENSIONS:
            documents.append(path)
        elif suffix in SUBTITLE_EXTENSIONS:
            subtitles.append(path)
        else:
            videos.append(path)

    return ClassifiedPaths(documents=tuple(documents), videos=tuple(videos), subtitles=tuple(subtitles))
