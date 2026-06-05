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
    from mpvqc.services.comments import CommentsService
    from mpvqc.services.exporter.context import RenderContext

_SCHEMA_URL = "https://raw.githubusercontent.com/mpvqc/mpvQC/main/docs/document-format/v1.json"


def render_v1(context: RenderContext) -> str:
    settings = context.settings
    player = context.player

    document: dict[str, object] = {"$schema": _SCHEMA_URL, "version": 1}

    if settings.write_header_date:
        document["created_at"] = QDateTime.currentDateTimeUtc().toString(Qt.DateFormat.ISODate)

    if settings.write_header_generator:
        build_info = context.build_info
        document["generator"] = f"{build_info.name} {build_info.version}"

    if settings.write_header_nickname and (author := settings.nickname):
        document["author"] = author

    if settings.write_header_video_path and (video := player.path):
        document["video"] = TypeMapperService.map_path_to_str(Path(video))

    if settings.write_header_subtitles and (subtitles := player.external_subtitles):
        document["subtitles"] = [TypeMapperService.map_path_to_str(Path(subtitle)) for subtitle in subtitles]

    document["comments"] = _render_comments(context.comments)

    return json.dumps(document, ensure_ascii=False, indent=4) + "\n"


def _render_comments(comments_service: CommentsService) -> list[dict[str, str]]:
    return [
        {
            "time": TimeFormatterService.format_milliseconds_to_subsecond_string(comment["time"]),
            "type": QCoreApplication.translate("CommentTypes", comment["commentType"]),
            "text": comment["comment"],
        }
        for comment in comments_service.comments()
    ]
