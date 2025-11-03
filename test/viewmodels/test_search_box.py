# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable, Iterable
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.datamodels import Comment
from mpvqc.models import MpvqcCommentModel
from mpvqc.services import ImporterService, PlayerService, ResetService
from mpvqc.viewmodels import MpvqcSearchBoxViewModel

DEFAULT_COMMENTS_SEARCH = (
    Comment(time=0, comment_type="commentType", comment="Word 1"),
    Comment(time=1, comment_type="commentType", comment="Word 2"),
    Comment(time=2, comment_type="commentType", comment="Word 3"),
    Comment(time=3, comment_type="commentType", comment="Word 4"),
    Comment(time=4, comment_type="commentType", comment="Word 5"),
    Comment(time=5, comment_type="commentType", comment="Word 6"),
    Comment(time=6, comment_type="commentType", comment=""),
    Comment(time=9, comment_type="commentType", comment="Word 9"),
)

EXTRA_COMMENTS = (
    Comment(time=7, comment_type="commentType", comment="Word 7"),
    Comment(time=8, comment_type="commentType", comment="Word 8"),
)


@pytest.fixture(scope="session")
def make_model() -> Callable[[Iterable[Comment]], MpvqcCommentModel]:
    def _make_model(
        set_comments: Iterable[Comment],
    ):
        def config(binder: inject.Binder):
            binder.bind(ImporterService, MagicMock(spec_set=ImporterService))
            binder.bind(PlayerService, MagicMock(spec_set=PlayerService))
            binder.bind(ResetService, MagicMock(spec_set=ResetService))

        inject.configure(config, bind_in_runtime=False, clear=True)

        # noinspection PyCallingNonCallable
        model: MpvqcCommentModel = MpvqcCommentModel()
        model.import_comments(tuple(set_comments))

        return model

    return _make_model


@pytest.fixture
def model(make_model):
    # noinspection PyArgumentList
    return make_model(set_comments=DEFAULT_COMMENTS_SEARCH)


@pytest.fixture
def view_model(model) -> MpvqcSearchBoxViewModel:
    # noinspection PyCallingNonCallable
    view_model = MpvqcSearchBoxViewModel()
    view_model.model = model
    return view_model


@pytest.fixture
def select(view_model):
    def _select_index(index: int):
        view_model.selectedIndex = index

    return _select_index


@pytest.fixture
def search(view_model) -> Callable[[str], tuple[str, bool, int]]:
    def _search(query):
        next_index = -1

        def track_highlight(idx):
            nonlocal next_index
            next_index = idx

        view_model.highlightRequested.connect(track_highlight)
        view_model.search(query)
        view_model.highlightRequested.disconnect(track_highlight)

        return view_model.statusLabel, view_model.hasMultipleResults, next_index

    # noinspection PyTypeChecker
    return _search


@pytest.fixture
def get_next(view_model) -> Callable[[], tuple[str, bool, int]]:
    def _func():
        next_index = -1

        def track_highlight(idx):
            nonlocal next_index
            next_index = idx

        view_model.highlightRequested.connect(track_highlight)
        view_model.selectNext()
        view_model.highlightRequested.disconnect(track_highlight)

        return view_model.statusLabel, view_model.hasMultipleResults, next_index

    # noinspection PyTypeChecker
    return _func


@pytest.fixture
def get_previous(view_model) -> Callable[[], tuple[str, bool, int]]:
    def _func():
        next_index = -1

        def track_highlight(idx):
            nonlocal next_index
            next_index = idx

        view_model.highlightRequested.connect(track_highlight)
        view_model.selectPrevious()
        view_model.highlightRequested.disconnect(track_highlight)

        return view_model.statusLabel, view_model.hasMultipleResults, next_index

    # noinspection PyTypeChecker
    return _func


def test_search_query_changed(view_model, make_spy, search, get_next, get_previous):
    spy = make_spy(view_model.searchQueryChanged)

    search("Query")
    assert spy.count() == 1
    assert spy.at(0, 0) == "Query"

    get_next()
    assert spy.count() == 1

    get_previous()
    assert spy.count() == 1

    search("Query")
    assert spy.count() == 1

    search("Other Query")
    assert spy.count() == 2


def test_search_with_empty_query(search):
    status_label, has_multiple, next_idx = search("")
    assert status_label == ""
    assert not has_multiple
    assert next_idx == -1


def test_search_no_match(search):
    status_label, has_multiple, next_idx = search("Query")
    assert status_label == "0/0"
    assert not has_multiple
    assert next_idx == -1


def test_search_match(search, view_model, make_spy):
    status_label_spy = make_spy(view_model.statusLabelChanged)
    has_multiple_spy = make_spy(view_model.hasMultipleResultsChanged)
    highlight_spy = make_spy(view_model.highlightRequested)

    status_label, has_multiple, next_idx = search("Word")

    assert status_label == "1/7"
    assert has_multiple
    assert next_idx == 0

    assert status_label_spy.count() == 1
    assert status_label_spy.at(0, 0) == "1/7"

    assert has_multiple_spy.count() == 1
    assert has_multiple_spy.at(0, 0) is True

    assert highlight_spy.count() >= 1
    assert highlight_spy.at(0, 0) == 0


def test_search_match_next(search, select, get_next):
    status_label, has_multiple, idx = search("Word")
    assert status_label == "1/7"
    assert has_multiple
    assert idx == 0

    select(idx)

    status_label, has_multiple, idx = get_next()
    assert status_label == "2/7"
    assert has_multiple
    assert idx == 1

    select(idx)

    status_label, has_multiple, idx = get_next()
    assert status_label == "3/7"
    assert has_multiple
    assert idx == 2


def test_search_match_next_new_query(search, select, get_next):
    status_label, has_multiple, idx = search("Word")
    assert status_label == "1/7"
    assert has_multiple
    assert idx == 0

    select(idx)

    status_label, has_multiple, idx = get_next()
    assert status_label == "2/7"
    assert has_multiple
    assert idx == 1

    select(idx)

    status_label, has_multiple, idx = get_next()
    assert status_label == "3/7"
    assert has_multiple
    assert idx == 2

    status_label, has_multiple, idx = search("4")
    assert status_label == "1/1"
    assert not has_multiple
    assert idx == 3


def test_search_match_next_after_import(model, search, select, get_next):
    status_label, has_multiple, idx = search("Word")
    assert status_label == "1/7"
    assert has_multiple
    assert idx == 0

    select(idx)

    status_label, has_multiple, idx = get_next()
    assert status_label == "2/7"
    assert has_multiple
    assert idx == 1

    select(idx)

    status_label, has_multiple, idx = get_next()
    assert status_label == "3/7"
    assert has_multiple
    assert idx == 2

    model.import_comments(EXTRA_COMMENTS)
    select(8)

    status_label, has_multiple, idx = get_next()
    assert status_label == "9/9"
    assert has_multiple
    assert idx == 9


def test_search_match_previous(search, select, get_previous):
    status_label, has_multiple, idx = search("Word")
    assert status_label == "1/7"
    assert has_multiple
    assert idx == 0

    select(idx)

    status_label, has_multiple, idx = get_previous()
    assert status_label == "7/7"
    assert has_multiple
    assert idx == 7

    select(idx)

    status_label, has_multiple, idx = get_previous()
    assert status_label == "6/7"
    assert has_multiple
    assert idx == 5


def test_search_match_previous_with_selection_change(search, select, get_previous):
    status_label, has_multiple, idx = search("Word")
    assert status_label == "1/7"
    assert has_multiple
    assert idx == 0

    select(idx)

    status_label, has_multiple, idx = get_previous()
    assert status_label == "7/7"
    assert has_multiple
    assert idx == 7

    select(idx)

    status_label, has_multiple, idx = get_previous()
    assert status_label == "6/7"
    assert has_multiple
    assert idx == 5

    select(index=2)

    status_label, has_multiple, idx = get_previous()
    assert status_label == "2/7"
    assert has_multiple
    assert idx == 1


def test_search_match_previous_after_import(search, model, select, get_next, get_previous):
    status_label, has_multiple, idx = search("Word")
    assert status_label == "1/7"
    assert has_multiple
    assert idx == 0

    select(idx)

    status_label, has_multiple, idx = get_next()
    assert status_label == "2/7"
    assert has_multiple
    assert idx == 1

    select(idx)

    status_label, has_multiple, idx = get_next()
    assert status_label == "3/7"
    assert has_multiple
    assert idx == 2

    model.import_comments(EXTRA_COMMENTS)

    select(index=8)

    status_label, has_multiple, idx = get_previous()
    assert status_label == "7/9"
    assert has_multiple
    assert idx == 7


def test_search_wrap_around(search, select, get_next, get_previous):
    select(index=6)

    status_label, has_multiple, idx = search("Word")
    assert status_label == "1/7"
    assert has_multiple
    assert idx == 0

    select(idx)

    status_label, has_multiple, idx = get_previous()
    assert status_label == "7/7"
    assert has_multiple
    assert idx == 7

    select(idx)

    status_label, has_multiple, idx = get_previous()
    assert status_label == "6/7"
    assert has_multiple
    assert idx == 5

    select(index=5)

    status_label, has_multiple, idx = get_next()
    assert status_label == "7/7"
    assert has_multiple
    assert idx == 7

    select(idx)

    status_label, has_multiple, idx = get_next()
    assert status_label == "1/7"
    assert has_multiple
    assert idx == 0
