# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from mpvqc.datamodels import SearchResult
from mpvqc.services.comments.search import CommentSearchEngine


@pytest.fixture
def store():
    def _find(query: str) -> list[int]:
        if query == "match":
            return [0, 2, 4]
        if query == "wrap":
            return [1, 3, 5]
        return []

    return SimpleNamespace(search_rows=Mock(side_effect=_find))


@pytest.fixture
def selection():
    return SimpleNamespace(selectedRow=0)


@pytest.fixture
def engine(store, selection):
    # pyrefly: ignore [bad-argument-type]
    return CommentSearchEngine(store, selection)


def _search(engine: CommentSearchEngine, query: str) -> SearchResult:
    return engine.search(query, include_current_row=True, top_down=True)


def test_empty_query_returns_inactive_sentinel(engine):
    assert _search(engine, "") == SearchResult(index=-1, current=-1, total=-1)


def test_no_match_returns_zero_zero(engine):
    assert _search(engine, "miss") == SearchResult(index=-1, current=0, total=0)


def test_first_hit_returned_on_new_query(engine):
    assert _search(engine, "match") == SearchResult(index=0, current=1, total=3)


def test_new_query_top_anchored_even_when_top_down_false(engine):
    result = engine.search("match", include_current_row=True, top_down=False)
    assert result == SearchResult(index=0, current=1, total=3)


def test_repeated_same_query_is_cached(engine, store):
    _search(engine, "match")
    _search(engine, "match")
    _search(engine, "match")

    assert store.search_rows.call_count == 1


def test_invalidate_drops_cache(engine, store):
    _search(engine, "match")
    engine.invalidate()
    _search(engine, "match")

    assert store.search_rows.call_count == 2


def test_next_wraps_forward(engine, selection):
    engine.search("wrap", include_current_row=True, top_down=True)
    selection.selectedRow = 5
    result = engine.search("wrap", include_current_row=False, top_down=True)

    assert result == SearchResult(index=1, current=1, total=3)


def test_previous_wraps_backward(engine, selection):
    engine.search("wrap", include_current_row=True, top_down=True)
    selection.selectedRow = 1
    result = engine.search("wrap", include_current_row=False, top_down=False)

    assert result == SearchResult(index=5, current=3, total=3)
