# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import functools
from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import QCoreApplication, QDateTime

from mpvqc.services.formatter_time import TimeFormatterService
from mpvqc.services.type_mapper import TypeMapperService

if TYPE_CHECKING:
    from jinja2 import Environment

    from mpvqc.services.exporter.context import RenderContext


def render_classic(template: str, context: RenderContext) -> str:
    return _environment().from_string(template).render(**_arguments(context))


@functools.cache
def _environment() -> Environment:
    from jinja2 import BaseLoader
    from jinja2.sandbox import ImmutableSandboxedEnvironment

    environment = ImmutableSandboxedEnvironment(loader=BaseLoader(), keep_trailing_newline=True)
    environment.filters["as_time"] = _as_time
    environment.filters["as_time_ms"] = _as_time_ms
    environment.filters["as_comment_type"] = _as_comment_type
    return environment


def _as_time(seconds: int) -> str:
    return TimeFormatterService.format_time_to_string(seconds, long_format=True)


def _as_time_ms(milliseconds: int) -> str:
    return TimeFormatterService.format_milliseconds_to_subsecond_string(milliseconds)


def _as_comment_type(comment_type: str) -> str:
    return QCoreApplication.translate("CommentTypes", comment_type)


def _arguments(context: RenderContext) -> dict:
    if raw_path := context.video_path:
        path = Path(raw_path)
        video_path = TypeMapperService.map_path_to_str(path)
        video_name = path.name
    else:
        video_path = ""
        video_name = ""

    return {
        "write_date": context.write_header_date,
        "write_generator": context.write_header_generator,
        "write_nickname": context.write_header_nickname,
        "write_video_path": context.write_header_video_path,
        "write_subtitle_paths": context.write_header_subtitles,
        "date": QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm"),
        "generator": context.generator,
        "nickname": context.nickname,
        "video_path": video_path,
        "video_name": video_name,
        "subtitles": tuple(TypeMapperService.map_path_to_str(Path(s)) for s in context.external_subtitles),
        "comments": [
            {**c, "time": c["time"] // TimeFormatterService.MILLISECONDS_PER_SECOND, "time_ms": c["time"]}
            for c in context.comments
        ],
    }
