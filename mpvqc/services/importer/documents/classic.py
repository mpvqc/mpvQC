# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import re
from pathlib import Path

from mpvqc.datamodels import Comment
from mpvqc.services.formatter_time import TimeFormatterService
from mpvqc.services.importer.parsed import ParsedDocument
from mpvqc.services.reverse_translator import ReverseTranslatorService

_REGEX_PATH = re.compile(r"^path\s*?:(?P<path>.*)$")
_REGEX_SUBTITLE = re.compile(r"^subtitle\s*?:(?P<subtitle>.*)$")
_REGEX_COMMENT = re.compile(r"^\[(?P<time>\d{2}:\d{2}:\d{2})]\s*?\[(?P<type>.*?)]\s*?(?P<comment>.*?)$")


def parse_classic(content: str) -> ParsedDocument:
    video: Path | None = None
    subtitles = []
    comments = []

    for line in content.splitlines(keepends=False):
        if video is None:
            video = _parse_path(line)
            if video is not None:
                continue

        if subtitle := _parse_subtitle(line):
            subtitles.append(subtitle)
            continue

        if comment := _parse_comment(line):
            comments.append(comment)

    return ParsedDocument(video=video, subtitles=tuple(subtitles), comments=tuple(comments))


def _parse_path(line: str) -> Path | None:
    match = _REGEX_PATH.match(line)
    if match is None:
        return None
    return Path(match.group("path").strip())


def _parse_subtitle(line: str) -> Path | None:
    match = _REGEX_SUBTITLE.match(line)
    if match is None:
        return None
    return Path(match.group("subtitle").strip())


def _parse_comment(line: str) -> Comment | None:
    match = _REGEX_COMMENT.match(line.strip())
    if match is None:
        return None

    time = match.group("time").strip()
    comment_type = match.group("type").strip()
    comment = match.group("comment").strip()

    return Comment(
        time=TimeFormatterService.parse_string_to_milliseconds(time),
        comment_type=ReverseTranslatorService.lookup(comment_type),
        comment=comment,
    )
