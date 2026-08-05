# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from mpvqc.importing.domain import make_plan

from .scanner import scan

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from pathlib import Path

    from mpvqc.importing.domain import FinishedPlan, LoadFoundVideo, UnfinishedPlan


def plan_import(
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
