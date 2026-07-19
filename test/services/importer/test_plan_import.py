# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from mpvqc.enums import ImportFoundVideo
from mpvqc.services.importer import FinishedPlan, UnfinishedPlan, errors, session, subtitles, video
from mpvqc.services.importer.plan import plan_import

if TYPE_CHECKING:
    from pathlib import Path


def test_valid_document_composes_into_a_finished_plan(tmp_path: Path) -> None:
    document = tmp_path / "document.json"
    document.write_text(
        json.dumps({"version": 1, "comments": [{"time": "00:00:01.000", "type": "Phrasing", "text": "A comment"}]}),
        encoding="utf-8",
    )

    plan = plan_import(
        [document],
        [],
        [],
        found_video_setting=ImportFoundVideo.ASK_EVERY_TIME,
        has_existing_comments=False,
        is_any_candidate_loaded=lambda _paths: False,
    )

    assert isinstance(plan, FinishedPlan)
    assert len(plan.comments) == 1
    assert plan.comments[0].comment == "A comment"
    assert plan.session == session.Merge()
    assert plan.video == video.Skip()
    assert plan.subtitles == subtitles.Skip()


def test_invalid_document_composes_into_an_unfinished_plan(tmp_path: Path) -> None:
    document = tmp_path / "broken.json"
    document.write_text(json.dumps({"comments": []}), encoding="utf-8")

    plan = plan_import(
        [document],
        [],
        [],
        found_video_setting=ImportFoundVideo.ASK_EVERY_TIME,
        has_existing_comments=False,
        is_any_candidate_loaded=lambda _paths: False,
    )

    assert isinstance(plan, UnfinishedPlan)
    assert isinstance(plan.errors, errors.Present)
    assert plan.errors.rejected_documents[0].path == document
