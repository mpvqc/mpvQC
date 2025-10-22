# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import re
from dataclasses import dataclass, field
from pathlib import Path

import inject

from mpvqc.datamodels import Comment

from .reverse_translator import ReverseTranslatorService


class DocumentImporterService:
    _reverse_translator: ReverseTranslatorService = inject.attr(ReverseTranslatorService)

    _REGEX_PATH = re.compile("^path\\s*?:(?P<path>.*)$")
    _REGEX_SUBTITLE = re.compile("^subtitle\\s*?:(?P<subtitle>.*)$")
    _REGEX_COMMENT = re.compile(r"^\[(?P<time>\d{2}:\d{2}:\d{2})]\s*?\[(?P<type>.*?)]\s*?(?P<comment>.*?)$")

    @dataclass
    class DocumentImportResult:
        valid_documents: list[Path] = field(default_factory=list)
        invalid_documents: list[Path] = field(default_factory=list)
        existing_videos: list[Path] = field(default_factory=list)
        existing_subtitles: list[Path] = field(default_factory=list)
        comments: list[Comment] = field(default_factory=list)

    def read(self, documents: list[Path]) -> DocumentImportResult:
        result = self.DocumentImportResult()

        for document in documents:
            content = document.read_text(encoding="utf-8")

            if content.startswith("[FILE]"):
                result.valid_documents.append(document)
            else:
                result.invalid_documents.append(document)
                continue

            video, subtitles, comments = self._parse(content)
            if video is not None and video.is_file():
                result.existing_videos.append(video)

            result.existing_subtitles.extend(s for s in subtitles if s.is_file())
            result.comments.extend(comments)

        return result

    def _parse(self, content: str) -> tuple[Path | None, list[Path], list[Comment]]:
        path = None
        subtitles = []
        comments = []

        for line in content.splitlines(keepends=False):
            if path is None:
                path = self._parse_path(line)
                if path is not None:
                    continue

            if subtitle := self._parse_subtitle(line):
                subtitles.append(subtitle)
                continue

            if comment := self._parse_comment(line):
                comments.append(comment)

        return path, subtitles, comments

    def _parse_path(self, line: str) -> Path | None:
        match = self._REGEX_PATH.match(line)

        if match is None:
            return None

        return Path(match.group("path").strip())

    def _parse_subtitle(self, line: str) -> Path | None:
        match = self._REGEX_SUBTITLE.match(line)

        if match is None:
            return None

        return Path(match.group("subtitle").strip())

    def _parse_comment(self, line: str) -> Comment | None:
        match = self._REGEX_COMMENT.match(line.strip())

        if match is None:
            return None

        time = match.group("time").strip()
        comment_type = match.group("type").strip()
        comment = match.group("comment").strip()

        hours, minutes, seconds = map(int, time.split(":"))
        time = hours * 3600 + minutes * 60 + seconds
        comment_type = self._reverse_translator.lookup(comment_type)

        return Comment(time, comment_type, comment)
