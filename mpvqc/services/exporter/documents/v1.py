# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import QCoreApplication, QDateTime, Qt

from mpvqc.services.formatter_time import TimeFormatterService
from mpvqc.services.type_mapper import TypeMapperService

if TYPE_CHECKING:
    from mpvqc.datamodels import Comment
    from mpvqc.services.exporter.context import RenderContext

_SCHEMA_URL = "https://raw.githubusercontent.com/mpvqc/mpvQC/main/docs/document-format/v1.json"


def render_v1(context: RenderContext) -> str:
    document: dict[str, object] = {"$schema": _SCHEMA_URL, "version": 1}

    if context.write_header_date:
        document["created_at"] = QDateTime.currentDateTimeUtc().toString(Qt.DateFormat.ISODate)

    if context.write_header_generator:
        document["generator"] = context.generator

    if context.write_header_nickname and (author := context.nickname):
        document["author"] = author

    if context.write_header_video_path and (video := context.video_path):
        document["video"] = TypeMapperService.map_path_to_str(Path(video))

    if context.write_header_subtitles and (subtitles := context.external_subtitles):
        document["subtitles"] = [TypeMapperService.map_path_to_str(Path(subtitle)) for subtitle in subtitles]

    document["comments"] = _render_comments(context.comments)

    return _dump(document)


def render_backup(context: RenderContext) -> str:
    document: dict[str, object] = {
        "$schema": _SCHEMA_URL,
        "version": 1,
        "created_at": QDateTime.currentDateTimeUtc().toString(Qt.DateFormat.ISODate),
    }

    if video := context.video_path:
        document["video"] = TypeMapperService.map_path_to_str(Path(video))

    document["comments"] = _render_comments(context.comments)

    return _dump(document)


def _dump(document: dict[str, object]) -> str:
    return json.dumps(document, ensure_ascii=False, indent=4) + "\n"


def _render_comments(comments: tuple[Comment, ...]) -> list[dict[str, str]]:
    return [
        {
            "time": TimeFormatterService.format_milliseconds_to_subsecond_string(comment.time),
            "type": QCoreApplication.translate("CommentTypes", comment.comment_type),
            "text": comment.comment,
        }
        for comment in comments
    ]
