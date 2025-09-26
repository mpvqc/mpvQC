# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.datamodels import Comment

DEFAULT_COMMENTS_SEARCH = [
    Comment(time=0, comment_type="commentType", comment="Word 1"),
    Comment(time=1, comment_type="commentType", comment="Word 2"),
    Comment(time=2, comment_type="commentType", comment="Word 3"),
    Comment(time=3, comment_type="commentType", comment="Word 4"),
    Comment(time=4, comment_type="commentType", comment="Word 5"),
    Comment(time=5, comment_type="commentType", comment="Word 6"),
    Comment(time=6, comment_type="commentType", comment=""),
    Comment(time=9, comment_type="commentType", comment="Word 9"),
]

EXTRA_COMMENTS = [
    Comment(time=7, comment_type="commentType", comment="Word 7"),
    Comment(time=8, comment_type="commentType", comment="Word 8"),
]


@pytest.fixture
def model(make_model):
    # noinspection PyArgumentList
    model, _ = make_model(set_comments=DEFAULT_COMMENTS_SEARCH)
    return model


@pytest.fixture
def search(model):
    def _search(query, include_current=True, forward=True, selected_index=0):
        result = model.search(query, include_current, forward, selected_index)
        return result["nextIndex"], result["currentResult"], result["totalResults"]

    return _search


def test_search_with_empty_query(search):
    next_idx, current, total = search("")
    assert (next_idx, current, total) == (-1, -1, -1)


def test_search_no_match(search):
    next_idx, current, total = search("Query")
    assert (next_idx, current, total) == (-1, 0, 0)


def test_search_match(search):
    next_idx, current, total = search("Word")
    assert (next_idx, current, total) == (0, 1, 7)


def test_search_match_next(search):
    idx, current, total = search("Word")
    assert (idx, current, total) == (0, 1, 7)

    idx, current, total = search("Word", include_current=False, forward=True, selected_index=idx)
    assert (idx, current, total) == (1, 2, 7)

    idx, current, total = search("Word", include_current=False, forward=True, selected_index=idx)
    assert (idx, current, total) == (2, 3, 7)


def test_search_match_next_new_query(search):
    idx, current, total = search("Word")
    assert (idx, current, total) == (0, 1, 7)

    idx, current, total = search("Word", include_current=False, forward=True, selected_index=idx)
    assert (idx, current, total) == (1, 2, 7)

    idx, current, total = search("Word", include_current=False, forward=True, selected_index=idx)
    assert (idx, current, total) == (2, 3, 7)

    idx, current, total = search("4")
    assert (idx, current, total) == (3, 1, 1)


def test_search_match_next_after_import(search, model):
    idx, current, total = search("Word")
    assert (idx, current, total) == (0, 1, 7)

    idx, current, total = search("Word", include_current=False, forward=True, selected_index=idx)
    assert (idx, current, total) == (1, 2, 7)

    idx, current, total = search("Word", include_current=False, forward=True, selected_index=idx)
    assert (idx, current, total) == (2, 3, 7)

    model.import_comments(EXTRA_COMMENTS)

    idx, current, total = search("Word", include_current=False, forward=True, selected_index=8)
    assert (idx, current, total) == (9, 9, 9)


def test_search_match_previous(search):
    idx, current, total = search("Word")
    assert (idx, current, total) == (0, 1, 7)

    idx, current, total = search("Word", include_current=False, forward=False, selected_index=idx)
    assert (idx, current, total) == (7, 7, 7)

    idx, current, total = search("Word", include_current=False, forward=False, selected_index=idx)
    assert (idx, current, total) == (5, 6, 7)


def test_search_match_previous_with_selection_change(search):
    idx, current, total = search("Word")
    assert (idx, current, total) == (0, 1, 7)

    idx, current, total = search("Word", include_current=False, forward=False, selected_index=idx)
    assert (idx, current, total) == (7, 7, 7)

    idx, current, total = search("Word", include_current=False, forward=False, selected_index=idx)
    assert (idx, current, total) == (5, 6, 7)

    idx, current, total = search("Word", include_current=False, forward=False, selected_index=2)
    assert (idx, current, total) == (1, 2, 7)


def test_search_match_previous_after_import(search, model):
    idx, current, total = search("Word")
    assert (idx, current, total) == (0, 1, 7)

    idx, current, total = search("Word", include_current=False, forward=True, selected_index=idx)
    assert (idx, current, total) == (1, 2, 7)

    idx, current, total = search("Word", include_current=False, forward=True, selected_index=idx)
    assert (idx, current, total) == (2, 3, 7)

    model.import_comments(EXTRA_COMMENTS)

    idx, current, total = search("Word", include_current=False, forward=False, selected_index=8)
    assert (idx, current, total) == (7, 7, 9)


def test_search_wrap_around(search):
    idx, current, total = search("Word", selected_index=6)
    assert (idx, current, total) == (0, 1, 7)

    idx, current, total = search("Word", include_current=False, forward=False, selected_index=idx)
    assert (idx, current, total) == (7, 7, 7)

    idx, current, total = search("Word", include_current=False, forward=False, selected_index=idx)
    assert (idx, current, total) == (5, 6, 7)

    idx, current, total = search("Word", include_current=False, forward=True, selected_index=5)
    assert (idx, current, total) == (7, 7, 7)

    idx, current, total = search("Word", include_current=False, forward=True, selected_index=idx)
    assert (idx, current, total) == (0, 1, 7)
