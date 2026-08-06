# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from mpvqc.importing.domain import ScanResult, collect_subtitle_sources, collect_video_sources

from .reader import read_documents
from .subtitle_videos import find_videos_in_subtitles

if TYPE_CHECKING:
    from pathlib import Path


def scan(documents: list[Path], videos: list[Path], subtitles: list[Path]) -> ScanResult:
    doc_data = read_documents(documents)

    merged_subtitles = collect_subtitle_sources(
        explicitly_provided=(sub.resolve() for sub in subtitles),
        found_in_document=(sub.resolve() for sub in doc_data.existing_subtitles),
    )
    merged_videos = collect_video_sources(
        explicitly_provided=(video.resolve() for video in videos),
        found_in_document=(video.resolve() for video in doc_data.existing_videos),
        found_in_subtitle=find_videos_in_subtitles(tuple(s.path for s in merged_subtitles)),
    )

    return ScanResult(
        videos=merged_videos,
        subtitles=merged_subtitles,
        comments=doc_data.comments,
        rejected_documents=doc_data.rejected_documents,
    )
