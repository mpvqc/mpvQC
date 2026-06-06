# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

from mpvqc.datamodels import DocumentImportResult, DocumentRejectionReason, RejectedDocument

from .documents import parse_classic, parse_v1
from .parsed import ParsedDocument

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


def read_documents(documents: list[Path]) -> DocumentImportResult:
    valid_docs = []
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

        match _parse_document(content, document):
            case DocumentRejectionReason() as reason:
                rejected_docs.append(RejectedDocument(document, reason))
            case ParsedDocument() as parsed:
                valid_docs.append(document)

                if parsed.video is not None and parsed.video.is_file():
                    existing_vids.append(parsed.video)

                existing_subs.extend(s for s in parsed.subtitles if s.is_file())
                all_comments.extend(parsed.comments)

    return DocumentImportResult(
        valid_documents=tuple(valid_docs),
        rejected_documents=tuple(rejected_docs),
        existing_videos=tuple(existing_vids),
        existing_subtitles=tuple(existing_subs),
        comments=tuple(all_comments),
    )


def _parse_document(content: str, document: Path) -> ParsedDocument | DocumentRejectionReason:
    if content.startswith("[FILE]"):
        return parse_classic(content)

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        logger.exception("Unrecognized document format: %s", document)
        return DocumentRejectionReason.INVALID

    if not isinstance(data, dict):
        logger.warning("Document is JSON but not an object: %s", document)
        return DocumentRejectionReason.INVALID

    match data.get("version"):
        case bool() | float() as version:
            logger.warning("Malformed document version %r: %s", version, document)
            return DocumentRejectionReason.INVALID
        case 1:
            try:
                return parse_v1(data)
            except ValueError:
                logger.exception("Malformed version 1 document: %s", document)
                return DocumentRejectionReason.INVALID
        case int(version):
            logger.warning("Unsupported document version %d: %s", version, document)
            return DocumentRejectionReason.UNSUPPORTED_VERSION
        case version:
            logger.warning("Malformed document version %r: %s", version, document)
            return DocumentRejectionReason.INVALID
