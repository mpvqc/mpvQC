# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from mpvqc.importing.domain import ScanResult, collect_subtitle_sources, collect_video_sources, make_plan

from .reader import read_documents
from .subtitle_videos import find_videos_in_subtitles

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from pathlib import Path

    from mpvqc.importing.domain import FinishedPlan, LoadFoundVideo, UnfinishedPlan


def plan(
    document_paths: list[Path],
    video_paths: list[Path],
    subtitle_paths: list[Path],
    *,
    found_video_setting: LoadFoundVideo,
    has_existing_comments: bool,
    is_any_candidate_loaded: Callable[[Iterable[Path]], bool],
) -> FinishedPlan | UnfinishedPlan:
    scan_result = scan(document_paths, video_paths, subtitle_paths)
    return make_plan(
        scan_result,
        found_video_setting=found_video_setting,
        has_existing_comments=has_existing_comments,
        any_candidate_loaded=is_any_candidate_loaded(v.path for v in scan_result.videos),
    )


def scan(documents: list[Path], videos: list[Path], subtitles: list[Path]) -> ScanResult:
    doc_data = read_documents(documents)

    merged_subtitles = collect_subtitle_sources(
        explicitly_provided=(sub.resolve() for sub in subtitles),
        found_in_document=(sub.resolve() for sub in doc_data.existing_subtitles),
    )
    subtitle_videos = find_videos_in_subtitles(tuple(s.path for s in merged_subtitles))

    merged_videos = collect_video_sources(
        explicitly_provided=(video.resolve() for video in videos),
        found_in_document=(video.resolve() for video in doc_data.existing_videos),
        found_in_subtitle=subtitle_videos,
    )

    return ScanResult(
        videos=merged_videos,
        subtitles=merged_subtitles,
        comments=doc_data.comments,
        rejected_documents=doc_data.rejected_documents,
    )
