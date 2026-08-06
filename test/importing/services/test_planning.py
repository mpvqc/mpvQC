# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from mpvqc.importing.domain import (
    ErrorsPresent,
    FinishedPlan,
    LoadFoundVideo,
    SessionMerge,
    SubtitlesSkip,
    UnfinishedPlan,
    VideoSkip,
)
from mpvqc.importing.services import plan

if TYPE_CHECKING:
    from pathlib import Path


def test_valid_document_composes_into_a_finished_plan(tmp_path: Path) -> None:
    document = tmp_path / "document.json"
    document.write_text(
        json.dumps({"version": 1, "comments": [{"time": "00:00:01.000", "type": "Phrasing", "text": "A comment"}]}),
        encoding="utf-8",
    )

    result = plan(
        [document],
        [],
        [],
        found_video_setting=LoadFoundVideo.ASK_EVERY_TIME,
        has_existing_comments=False,
        is_any_candidate_loaded=lambda _paths: False,
    )

    assert isinstance(result, FinishedPlan)
    assert len(result.comments) == 1
    assert result.comments[0].comment == "A comment"
    assert result.session == SessionMerge()
    assert result.video == VideoSkip()
    assert result.subtitles == SubtitlesSkip()


def test_invalid_document_composes_into_an_unfinished_plan(tmp_path: Path) -> None:
    document = tmp_path / "broken.json"
    document.write_text(json.dumps({"comments": []}), encoding="utf-8")

    result = plan(
        [document],
        [],
        [],
        found_video_setting=LoadFoundVideo.ASK_EVERY_TIME,
        has_existing_comments=False,
        is_any_candidate_loaded=lambda _paths: False,
    )

    assert isinstance(result, UnfinishedPlan)
    assert isinstance(result.errors, ErrorsPresent)
    assert result.errors.rejected_documents[0].path == document
