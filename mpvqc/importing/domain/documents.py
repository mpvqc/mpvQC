# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from mpvqc.datamodels import Comment

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass(frozen=True)
class ParsedDocument:
    video: Path | None
    subtitles: tuple[Path, ...]
    comments: tuple[Comment, ...]


_REGEX_CLASSIC_PATH = re.compile(r"^path\s*?:(?P<path>.*)$")
_REGEX_CLASSIC_SUBTITLE = re.compile(r"^subtitle\s*?:(?P<subtitle>.*)$")
_REGEX_CLASSIC_COMMENT = re.compile(r"^\[(?P<time>\d{2}:\d{2}:\d{2})]\s*?\[(?P<type>.*?)]\s*?(?P<comment>.*?)$")
_REGEX_V1_TIME = re.compile(r"^\d{2}:[0-5]\d:[0-5]\d\.\d{3}$")


def parse_classic(content: str, translate_comment_type: Callable[[str], str]) -> ParsedDocument:
    video: Path | None = None
    subtitles = []
    comments = []

    for line in content.splitlines(keepends=False):
        if video is None:
            video = _parse_classic_path(line)
            if video is not None:
                continue

        if subtitle := _parse_classic_subtitle(line):
            subtitles.append(subtitle)
            continue

        if comment := _parse_classic_comment(line, translate_comment_type):
            comments.append(comment)

    return ParsedDocument(video=video, subtitles=tuple(subtitles), comments=tuple(comments))


def _parse_classic_path(line: str) -> Path | None:
    match = _REGEX_CLASSIC_PATH.match(line)
    if match is None:
        return None
    return Path(match.group("path").strip())


def _parse_classic_subtitle(line: str) -> Path | None:
    match = _REGEX_CLASSIC_SUBTITLE.match(line)
    if match is None:
        return None
    return Path(match.group("subtitle").strip())


def _parse_classic_comment(line: str, translate_comment_type: Callable[[str], str]) -> Comment | None:
    match = _REGEX_CLASSIC_COMMENT.match(line.strip())
    if match is None:
        return None

    time = match.group("time").strip()
    comment_type = match.group("type").strip()
    comment = match.group("comment").strip()

    return Comment(
        time=_parse_string_to_milliseconds(time),
        comment_type=translate_comment_type(comment_type),
        comment=comment,
    )


def parse_v1(data: dict, translate_comment_type: Callable[[str], str]) -> ParsedDocument:
    return ParsedDocument(
        video=_parse_v1_video(data),
        subtitles=_parse_v1_subtitles(data),
        comments=_parse_v1_comments(data, translate_comment_type),
    )


def _parse_v1_video(data: dict) -> Path | None:
    match data.get("video"):
        case None:
            return None
        case str(video):
            return Path(video)
        case other:
            msg = f"Expected 'video' to be a string, got: {type(other).__name__}"
            raise ValueError(msg)


def _parse_v1_subtitles(data: dict) -> tuple[Path, ...]:
    match data.get("subtitles"):
        case None:
            return ()
        case list(subtitles) if all(isinstance(subtitle, str) for subtitle in subtitles):
            return tuple(Path(subtitle) for subtitle in subtitles)
        case other:
            msg = f"Expected 'subtitles' to be a list of strings, got: {other!r}"
            raise ValueError(msg)


def _parse_v1_comments(data: dict, translate_comment_type: Callable[[str], str]) -> tuple[Comment, ...]:
    match data.get("comments"):
        case list(comments):
            return tuple(_parse_v1_comment(comment, translate_comment_type) for comment in comments)
        case other:
            msg = f"Expected 'comments' to be a list, got: {type(other).__name__}"
            raise ValueError(msg)


def _parse_v1_comment(entry: object, translate_comment_type: Callable[[str], str]) -> Comment:
    if isinstance(entry, dict):
        time = entry.get("time")
        comment_type = entry.get("type")
        text = entry.get("text")
        if (
            isinstance(time, str)
            and isinstance(comment_type, str)
            and isinstance(text, str)
            and _REGEX_V1_TIME.match(time)
        ):
            return Comment(
                time=_parse_subsecond_string_to_milliseconds(time),
                comment_type=translate_comment_type(comment_type),
                comment=text,
            )

    msg = f"Expected a comment with 'time', 'type' and 'text', got: {entry!r}"
    raise ValueError(msg)


def _parse_string_to_milliseconds(time_string: str) -> int:
    hours, minutes, seconds = map(int, time_string.split(":"))
    return (hours * 3600 + minutes * 60 + seconds) * 1000


def _parse_subsecond_string_to_milliseconds(time_string: str) -> int:
    time, milliseconds = time_string.split(".")
    return _parse_string_to_milliseconds(time) + int(milliseconds)
