# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
from datetime import UTC
from pathlib import Path
from typing import TYPE_CHECKING

from mpvqc.comments.services import translate_comment_type
from mpvqc.shared import format_milliseconds_to_subsecond_string

if TYPE_CHECKING:
    from datetime import datetime

    from mpvqc.shared import Comment

    from .snapshot import ExportSnapshot

_SCHEMA_URL = "https://raw.githubusercontent.com/mpvqc/mpvQC/main/docs/document-format/v1.json"


def render_v1(snapshot: ExportSnapshot) -> str:
    document: dict[str, object] = {"$schema": _SCHEMA_URL, "version": 1}

    if snapshot.write_header_date:
        document["created_at"] = _utc_timestamp(snapshot.captured_at)

    if snapshot.write_header_generator:
        document["generator"] = snapshot.generator

    if snapshot.write_header_nickname and (author := snapshot.nickname):
        document["author"] = author

    if snapshot.write_header_video_path and (video := snapshot.video_path):
        document["video"] = str(Path(video).resolve())

    if snapshot.write_header_subtitles and (subtitles := snapshot.external_subtitles):
        document["subtitles"] = [str(Path(subtitle).resolve()) for subtitle in subtitles]

    document["comments"] = _render_comments(snapshot.comments)

    return _dump(document)


def render_backup(snapshot: ExportSnapshot) -> str:
    document: dict[str, object] = {
        "$schema": _SCHEMA_URL,
        "version": 1,
        "created_at": _utc_timestamp(snapshot.captured_at),
    }

    if video := snapshot.video_path:
        document["video"] = str(Path(video).resolve())

    document["comments"] = _render_comments(snapshot.comments)

    return _dump(document)


def _utc_timestamp(moment: datetime) -> str:
    return moment.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _dump(document: dict[str, object]) -> str:
    return json.dumps(document, ensure_ascii=False, indent=4) + "\n"


def _render_comments(comments: tuple[Comment, ...]) -> list[dict[str, str]]:
    return [
        {
            "time": format_milliseconds_to_subsecond_string(comment.time),
            "type": translate_comment_type(comment.comment_type),
            "text": comment.comment,
        }
        for comment in comments
    ]
