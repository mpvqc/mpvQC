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


@dataclass(frozen=True)
class ValidDocument:
    path: Path
    video_path: Path | None
    video_exists: bool


@dataclass(frozen=True)
class DocumentImportResult:
    valid_documents: list[ValidDocument]
    invalid_documents: list[Path]
    comments: list[Comment]


class DocumentImporterService:
    _reverse_translator: ReverseTranslatorService = inject.attr(ReverseTranslatorService)

    _REGEX_PATH = re.compile("^path\\s*?:(?P<path>.*)$")
    _REGEX_COMMENT = re.compile(r"^\[(?P<time>\d{2}:\d{2}:\d{2})]\s*?\[(?P<type>.*?)]\s*?(?P<comment>.*?)$")

    def read(self, documents: list[Path]) -> DocumentImportResult:
        valid_documents: list[ValidDocument] = []
        invalid_documents: list[Path] = []
        comments: list[Comment] = []

        for document in documents:
            content = document.read_text(encoding="utf-8")

            if not content.startswith("[FILE]"):
                invalid_documents.append(document.resolve())
                continue

            valid_document, more_comments = self._parse_document(document, content)
            valid_documents.append(valid_document)
            comments.extend(more_comments)

        return DocumentImportResult(
            valid_documents=valid_documents,
            invalid_documents=invalid_documents,
            comments=comments,
        )

    def _parse_document(self, document_path: Path, content: str) -> tuple[ValidDocument, list[Comment]]:
        video_path, comments = self._parse_document_content(content)
        valid_document = ValidDocument(
            path=document_path,
            video_path=video_path,
            video_exists=video_path is not None and video_path.is_file(),
        )
        return valid_document, comments

    def _parse_document_content(self, content: str) -> tuple[Path | None, list[Comment]]:
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
