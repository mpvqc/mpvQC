# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import NamedTuple

import pytest

from mpvqc.comments.models import CommentStore
from mpvqc.shared import Comment


class _SearchRowsCase(NamedTuple):
    name: str
    comments: tuple[Comment, ...]
    query: str
    expected_rows: list[int]


def _comment(text: str, comment_type: str = "commentType") -> Comment:
    return Comment(time=0, comment_type=comment_type, comment=text)


_CASES = [
    _SearchRowsCase(
        name="finds an exact text match",
        comments=(_comment("needle"),),
        query="needle",
        expected_rows=[0],
    ),
    _SearchRowsCase(
        name="does not find absent text",
        comments=(_comment("haystack"),),
        query="needle",
        expected_rows=[],
    ),
    _SearchRowsCase(
        name="finds text in the middle of a comment",
        comments=(_comment("before needle after"),),
        query="needle",
        expected_rows=[0],
    ),
    _SearchRowsCase(
        name="matches uppercase text with a lowercase query",
        comments=(_comment("NEEDLE"),),
        query="needle",
        expected_rows=[0],
    ),
    _SearchRowsCase(
        name="matches lowercase text with an uppercase query",
        comments=(_comment("needle"),),
        query="NEEDLE",
        expected_rows=[0],
    ),
    _SearchRowsCase(
        name="casefolds sharp s",
        comments=(_comment("ß"),),
        query="SS",
        expected_rows=[0],
    ),
    _SearchRowsCase(
        name="does not match the comment type",
        comments=(_comment("unrelated text", comment_type="needle"),),
        query="needle",
        expected_rows=[],
    ),
    _SearchRowsCase(
        name="does not match an empty query",
        comments=(_comment("every comment would otherwise match"),),
        query="",
        expected_rows=[],
    ),
    _SearchRowsCase(
        name="treats whitespace as a literal query",
        comments=(_comment("contains a space"), _comment("nospace")),
        query=" ",
        expected_rows=[0],
    ),
    _SearchRowsCase(
        name="returns matching rows in ascending order",
        comments=(
            _comment("needle first"),
            _comment("miss"),
            _comment("needle third"),
            _comment("needle fourth"),
        ),
        query="needle",
        expected_rows=[0, 2, 3],
    ),
]


@pytest.mark.parametrize("case", _CASES, ids=lambda case: case.name)
def test_search_rows_matches_comment_text(store: CommentStore, case: _SearchRowsCase):
    for row, comment in enumerate(case.comments):
        store.insert(row, store.mint(comment))

    assert store.search_rows(case.query) == case.expected_rows


@pytest.fixture
def store() -> CommentStore:
    return CommentStore()
