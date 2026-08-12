# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import functools
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import QCoreApplication

from mpvqc.services import TimeFormatterService, TypeMapperService
from mpvqc.shared import MILLISECONDS_PER_SECOND, format_milliseconds_to_subsecond_string

from .writer import ExportError

if TYPE_CHECKING:
    from jinja2 import Environment

    from .snapshot import ExportSnapshot

logger = logging.getLogger(__name__)


def render_template_file(template: Path, snapshot: ExportSnapshot) -> str:
    from jinja2 import TemplateError, TemplateSyntaxError

    try:
        content = template.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        logger.exception("Failed to read export template %s", template)
        #: Shown when a user-supplied export template cannot be read (file gone,
        #: permission denied, or not valid UTF-8). The technical detail is logged,
        #: not surfaced to the user.
        msg = QCoreApplication.translate("MessageBoxes", "The export template could not be read.")
        raise ExportError(msg) from e

    try:
        return render_template(content, snapshot)
    except TemplateSyntaxError as e:
        raise ExportError(e.message or "", e.lineno) from e
    except TemplateError as e:
        raise ExportError(e.message or "") from e


def render_template(template: str, snapshot: ExportSnapshot) -> str:
    return _environment().from_string(template).render(**_arguments(snapshot))


@functools.cache
def _environment() -> Environment:
    from jinja2 import BaseLoader
    from jinja2.sandbox import ImmutableSandboxedEnvironment

    environment = ImmutableSandboxedEnvironment(loader=BaseLoader(), keep_trailing_newline=True)
    environment.filters["as_time"] = _as_time
    environment.filters["as_time_ms"] = format_milliseconds_to_subsecond_string
    environment.filters["as_comment_type"] = _as_comment_type
    return environment


def _as_time(seconds: int) -> str:
    return TimeFormatterService.format_time_to_string(seconds, long_format=True)


def _as_comment_type(comment_type: str) -> str:
    return QCoreApplication.translate("CommentTypes", comment_type)


def _arguments(snapshot: ExportSnapshot) -> dict:
    if raw_path := snapshot.video_path:
        path = Path(raw_path)
        video_path = TypeMapperService.map_path_to_str(path)
        video_name = path.name
    else:
        video_path = ""
        video_name = ""

    return {
        "write_date": snapshot.write_header_date,
        "write_generator": snapshot.write_header_generator,
        "write_nickname": snapshot.write_header_nickname,
        "write_video_path": snapshot.write_header_video_path,
        "write_subtitle_paths": snapshot.write_header_subtitles,
        "date": snapshot.captured_at.strftime("%Y-%m-%d %H:%M"),
        "generator": snapshot.generator,
        "nickname": snapshot.nickname,
        "video_path": video_path,
        "video_name": video_name,
        "subtitles": tuple(TypeMapperService.map_path_to_str(Path(s)) for s in snapshot.external_subtitles),
        "comments": [
            {
                "time": c.time // MILLISECONDS_PER_SECOND,
                "time_ms": c.time,
                "commentType": c.comment_type,
                "comment": c.comment,
            }
            for c in snapshot.comments
        ],
    }
