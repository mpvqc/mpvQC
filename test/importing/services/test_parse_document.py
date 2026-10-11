# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from typing import NamedTuple

import pytest
from hypothesis import given
from hypothesis import strategies as st

from mpvqc.importing.services import DocumentMalformed, DocumentVersionUnsupported, ParsedDocument, parse_document


def test_parse_document_reads_classic_document_by_its_header():
    result = parse_document("[FILE]\n\n[DATA]\n[00:00:10] [Translation] a comment\n")

    assert isinstance(result, ParsedDocument)
    assert [(c.time, c.comment) for c in result.comments] == [(10_000, "a comment")]


def test_parse_document_reads_v1_document():
    content = json.dumps({"version": 1, "comments": [{"time": "00:00:20.000", "type": "Translation", "text": "x"}]})

    result = parse_document(content)

    assert isinstance(result, ParsedDocument)
    assert [(c.time, c.comment) for c in result.comments] == [(20_000, "x")]


class InvalidCase(NamedTuple):
    name: str
    content: str


INVALID_DOCUMENTS = [
    InvalidCase(name="no header and no json", content="erroneous_document\n"),
    InvalidCase(name="json array", content="[]"),
    InvalidCase(name="missing version", content='{"comments": []}'),
    InvalidCase(name="version as bool", content='{"version": true}'),
    InvalidCase(name="malformed v1", content='{"version": 1}'),
    InvalidCase(name="deeply nested array", content="[" * 100_000),
    InvalidCase(name="over-long version", content='{"version": ' + "1" * 5000 + "}"),
]


@pytest.mark.parametrize("case", INVALID_DOCUMENTS, ids=lambda case: case.name)
def test_parse_document_rejects_invalid_document(case: InvalidCase):
    assert isinstance(parse_document(case.content), DocumentMalformed)


def test_parse_document_tells_null_version_from_missing_version():
    result = parse_document('{"version": null}')

    assert isinstance(result, DocumentMalformed)
    assert "Missing" not in result.detail


HUGE = "x" * 10_000


@pytest.mark.parametrize(
    "document",
    [
        {"version": 1, "subtitles": [HUGE, 42], "comments": []},
        {"version": 1, "comments": [{"time": HUGE}]},
    ],
    ids=["subtitles", "comment"],
)
def test_parse_document_keeps_detail_short_for_large_malformed_entries(document: dict):
    result = parse_document(json.dumps(document))

    assert isinstance(result, DocumentMalformed)
    assert HUGE not in result.detail


def test_parse_document_rejects_unsupported_version():
    result = parse_document('{"version": 999}')

    assert isinstance(result, DocumentVersionUnsupported)
    assert result.version == 999


json_scalars = st.one_of(st.none(), st.booleans(), st.integers(), st.floats(), st.text())
json_values = st.recursive(
    json_scalars,
    lambda children: st.one_of(st.lists(children), st.dictionaries(st.text(), children)),
)
v1_comment = st.fixed_dictionaries(
    {
        "time": st.one_of(st.from_regex(r"\d{2}:[0-5]\d:[0-5]\d\.\d{3}", fullmatch=True), json_values),
        "type": json_values,
        "text": json_values,
    }
)
v1_like_documents = st.fixed_dictionaries(
    {"version": st.one_of(st.just(1), json_values)},
    optional={
        "video": json_values,
        "subtitles": json_values,
        "comments": st.one_of(json_values, st.lists(st.one_of(v1_comment, json_values))),
    },
)


@pytest.mark.fuzz
@given(st.text())
def test_parse_document_never_raises_on_any_text(content: str):
    assert isinstance(parse_document(content), ParsedDocument | DocumentMalformed | DocumentVersionUnsupported)


@pytest.mark.fuzz
@given(st.one_of(json_values, v1_like_documents).map(json.dumps))
def test_parse_document_never_raises_on_any_json(content: str):
    assert isinstance(parse_document(content), ParsedDocument | DocumentMalformed | DocumentVersionUnsupported)
