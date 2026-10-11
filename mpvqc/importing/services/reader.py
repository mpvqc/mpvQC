# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, assert_never

from .documents import (
    DocumentMalformed,
    DocumentUnreadable,
    DocumentVersionUnsupported,
    ParsedDocument,
    parse_document,
)

if TYPE_CHECKING:
    from pathlib import Path

    from mpvqc.shared import Comment

    from .documents import DocumentRejection

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RejectedDocument:
    path: Path
    reason: DocumentRejection


@dataclass(frozen=True)
class ReadDocumentsResult:
    rejected_documents: tuple[RejectedDocument, ...]
    existing_videos: tuple[Path, ...]
    existing_subtitles: tuple[Path, ...]
    comments: tuple[Comment, ...]


def read_documents(documents: tuple[Path, ...]) -> ReadDocumentsResult:
    rejected_docs = []
    existing_vids = []
    existing_subs = []
    all_comments = []

    for document in documents:
        result: ParsedDocument | DocumentRejection
        try:
            content = document.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError as error:
            result = DocumentMalformed(f"Failed to decode: {error}")
        except OSError as error:
            result = DocumentUnreadable(error)
        else:
            result = parse_document(content)

        match result:
            case ParsedDocument() as parsed:
                if parsed.video is not None and parsed.video.is_file():
                    existing_vids.append(parsed.video)

                existing_subs.extend(s for s in parsed.subtitles if s.is_file())
                all_comments.extend(parsed.comments)
            case DocumentMalformed() | DocumentVersionUnsupported() | DocumentUnreadable() as rejection:
                logger.warning("Rejected document %s: %s", document, _describe(rejection))
                rejected_docs.append(RejectedDocument(document, rejection))
            case _ as unreachable:
                assert_never(unreachable)

    return ReadDocumentsResult(
        rejected_documents=tuple(rejected_docs),
        existing_videos=tuple(existing_vids),
        existing_subtitles=tuple(existing_subs),
        comments=tuple(all_comments),
    )


def _describe(rejection: DocumentRejection) -> str:
    match rejection:
        case DocumentMalformed(detail):
            return detail
        case DocumentVersionUnsupported(version):
            return f"unsupported version {version}"
        case DocumentUnreadable(error):
            return str(error)
        case _ as unreachable:
            assert_never(unreachable)
