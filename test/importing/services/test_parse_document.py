# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from typing import NamedTuple

import pytest

from mpvqc.importing.services import DocumentRejectionReason, ParsedDocument, parse_document


def test_parse_document_reads_classic_document_by_its_header():
    result = parse_document("[FILE]\n\n[DATA]\n[00:00:10] [Translation] a comment\n")

    assert isinstance(result, ParsedDocument)
    assert [(c.time, c.comment) for c in result.comments] == [(10_000, "a comment")]


def test_parse_document_reads_v1_document():
    content = json.dumps({"version": 1, "comments": [{"time": "00:00:20.000", "type": "Translation", "text": "x"}]})

    result = parse_document(content)

    assert isinstance(result, ParsedDocument)
    assert [(c.time, c.comment) for c in result.comments] == [(20_000, "x")]


class RejectionCase(NamedTuple):
    name: str
    content: str
    reason: DocumentRejectionReason


REJECTED_DOCUMENTS = [
    RejectionCase(
        name="no header and no json",
        content="erroneous_document\n",
        reason=DocumentRejectionReason.INVALID,
    ),
    RejectionCase(
        name="json array",
        content="[]",
        reason=DocumentRejectionReason.INVALID,
    ),
    RejectionCase(
        name="missing version",
        content='{"comments": []}',
        reason=DocumentRejectionReason.INVALID,
    ),
    RejectionCase(
        name="version as bool",
        content='{"version": true}',
        reason=DocumentRejectionReason.INVALID,
    ),
    RejectionCase(
        name="malformed v1",
        content='{"version": 1}',
        reason=DocumentRejectionReason.INVALID,
    ),
    RejectionCase(
        name="unsupported version",
        content='{"version": 999}',
        reason=DocumentRejectionReason.UNSUPPORTED_VERSION,
    ),
    RejectionCase(
        name="deeply nested array",
        content="[" * 100_000,
        reason=DocumentRejectionReason.INVALID,
    ),
    RejectionCase(
        name="over-long version",
        content='{"version": ' + "1" * 5000 + "}",
        reason=DocumentRejectionReason.INVALID,
    ),
]


@pytest.mark.parametrize("case", REJECTED_DOCUMENTS, ids=lambda case: case.name)
def test_parse_document_rejects(case: RejectionCase):
    assert parse_document(case.content) == case.reason

