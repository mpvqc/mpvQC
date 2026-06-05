# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

from mpvqc.datamodels import DocumentImportResult

from .documents import parse_classic, parse_v1

if TYPE_CHECKING:
    from pathlib import Path

    from .parsed import ParsedDocument

logger = logging.getLogger(__name__)


def read_documents(documents: list[Path]) -> DocumentImportResult:
    valid_docs = []
    invalid_docs = []
    existing_vids = []
    existing_subs = []
    all_comments = []

    for document in documents:
        try:
            content = document.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            logger.exception("Failed to read document: %s", document)
            invalid_docs.append(document)
            continue

        parsed = _parse_document(content, document)
        if parsed is None:
            invalid_docs.append(document)
            continue

        valid_docs.append(document)

        if parsed.video is not None and parsed.video.is_file():
            existing_vids.append(parsed.video)

        existing_subs.extend(s for s in parsed.subtitles if s.is_file())
        all_comments.extend(parsed.comments)

    return DocumentImportResult(
        valid_documents=tuple(valid_docs),
        invalid_documents=tuple(invalid_docs),
        existing_videos=tuple(existing_vids),
        existing_subtitles=tuple(existing_subs),
        comments=tuple(all_comments),
    )


def _parse_document(content: str, document: Path) -> ParsedDocument | None:
    if content.startswith("[FILE]"):
        return parse_classic(content)

    if (data := _parse_json(content)) is not None:
        return _parse_json_document(data, document)

    logger.warning("Unrecognized document format: %s", document)
    return None


def _parse_json(content: str) -> object | None:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None


def _parse_json_document(data: object, document: Path) -> ParsedDocument | None:
    if not isinstance(data, dict):
        logger.warning("Document is JSON but not an object: %s", document)
        return None

    match data.get("version"):
        case 1:
            try:
                return parse_v1(data)
            except ValueError:
                logger.exception("Malformed version 1 document: %s", document)
                return None
        case version:
            logger.warning("Unsupported document version %r: %s", version, document)
            return None
