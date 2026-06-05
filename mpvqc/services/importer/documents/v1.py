# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import re
from pathlib import Path

import inject

from mpvqc.datamodels import Comment
from mpvqc.services.formatter_time import TimeFormatterService
from mpvqc.services.reverse_translator import ReverseTranslatorService

from .parsed import ParsedDocument

_REGEX_TIME = re.compile(r"^\d{2}:[0-5]\d:[0-5]\d\.\d{3}$")


def parse(data: dict) -> ParsedDocument:
    return ParsedDocument(
        video=_parse_video(data),
        subtitles=_parse_subtitles(data),
        comments=_parse_comments(data),
    )


def _parse_video(data: dict) -> Path | None:
    match data.get("video"):
        case None:
            return None
        case str(video):
            return Path(video)
        case other:
            msg = f"Expected 'video' to be a string, got: {type(other).__name__}"
            raise ValueError(msg)


def _parse_subtitles(data: dict) -> tuple[Path, ...]:
    match data.get("subtitles"):
        case None:
            return ()
        case list(subtitles) if all(isinstance(subtitle, str) for subtitle in subtitles):
            return tuple(Path(subtitle) for subtitle in subtitles)
        case other:
            msg = f"Expected 'subtitles' to be a list of strings, got: {other!r}"
            raise ValueError(msg)


def _parse_comments(data: dict) -> tuple[Comment, ...]:
    match data.get("comments"):
        case list(comments):
            time_formatter = inject.instance(TimeFormatterService)
            reverse_translator = inject.instance(ReverseTranslatorService)
            return tuple(_parse_comment(comment, time_formatter, reverse_translator) for comment in comments)
        case other:
            msg = f"Expected 'comments' to be a list, got: {type(other).__name__}"
            raise ValueError(msg)


def _parse_comment(
    entry: object,
    time_formatter: TimeFormatterService,
    reverse_translator: ReverseTranslatorService,
) -> Comment:
    if isinstance(entry, dict):
        time = entry.get("time")
        comment_type = entry.get("type")
        text = entry.get("text")
        if (
            isinstance(time, str)
            and isinstance(comment_type, str)
            and isinstance(text, str)
            and _REGEX_TIME.match(time)
        ):
            return Comment(
                time=time_formatter.parse_subsecond_string_to_milliseconds(time),
                comment_type=reverse_translator.lookup(comment_type),
                comment=text,
            )

    msg = f"Expected a comment with 'time', 'type' and 'text', got: {entry!r}"
    raise ValueError(msg)
