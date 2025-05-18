# mpvQC
#
# Copyright (C) 2024 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
from dataclasses import dataclass
from pathlib import Path

import inject

from mpvqc.models import Comment

from .reverse_translator import ReverseTranslatorService


class DocumentImporterService:
    _reverse_translator: ReverseTranslatorService = inject.attr(ReverseTranslatorService)

    _REGEX_PATH = re.compile("^path\\s*?:(?P<path>.*)$")
    _REGEX_COMMENT = re.compile(r"^\[(?P<time>\d{2}:\d{2}:\d{2})]\s*?\[(?P<type>.*?)]\s*?(?P<comment>.*?)$")

    @dataclass
    class DocumentImportResult:
        valid_documents: list[Path]
        invalid_documents: list[Path]
        existing_videos: list[Path]
        comments: list[Comment]

    def read(self, documents: list[Path]) -> DocumentImportResult:
        valid_documents: list[Path] = []
        invalid_documents: list[Path] = []
        existing_videos: list[Path] = []
        all_comments: list[Comment] = []

        for document in documents:
            content = document.read_text(encoding="utf-8")

            if content.startswith("[FILE]"):
                valid_documents.append(document)
            else:
                invalid_documents.append(document)
                continue

            video, comments = self._parse(content)
            if video is not None and video.is_file():
                existing_videos.append(video)
            all_comments.extend(comments)

        return self.DocumentImportResult(valid_documents, invalid_documents, existing_videos, all_comments)

    def _parse(self, content: str) -> tuple[Path | None, list[Comment]]:
        path = None
        comments = []

        for line in content.splitlines(keepends=False):
            if path is None:
                path = self._parse_path(line)
                if path is not None:
                    continue

            if comment := self._parse_comment(line):
                comments.append(comment)

        return path, comments

    def _parse_path(self, line: str) -> Path | None:
        match = self._REGEX_PATH.match(line)

        if match is None:
            return None

        return Path(match.group("path").strip())

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
