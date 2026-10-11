# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .documents import DocumentRejectionReason, ParsedDocument, parse_document

if TYPE_CHECKING:
    from pathlib import Path

    from mpvqc.shared import Comment

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RejectedDocument:
    path: Path
    reason: DocumentRejectionReason


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
        try:
            content = document.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError):
            logger.exception("Failed to read document: %s", document)
            rejected_docs.append(RejectedDocument(document, DocumentRejectionReason.INVALID))
            continue

        match parse_document(content):
            case DocumentRejectionReason() as reason:
                logger.warning("Rejected document %s: %s", document, reason.name)
                rejected_docs.append(RejectedDocument(document, reason))
            case ParsedDocument() as parsed:
                if parsed.video is not None and parsed.video.is_file():
                    existing_vids.append(parsed.video)

                existing_subs.extend(s for s in parsed.subtitles if s.is_file())
                all_comments.extend(parsed.comments)

    return ReadDocumentsResult(
        rejected_documents=tuple(rejected_docs),
        existing_videos=tuple(existing_vids),
        existing_subtitles=tuple(existing_subs),
        comments=tuple(all_comments),
    )
