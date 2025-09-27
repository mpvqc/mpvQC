# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later
from collections.abc import Callable, Iterable
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.controllers import MpvqcSearchBoxController
from mpvqc.datamodels import Comment
from mpvqc.models import MpvqcCommentModel
from mpvqc.services import PlayerService

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


@pytest.fixture(scope="session")
def make_model() -> Callable[[Iterable[Comment]], MpvqcCommentModel]:
    def _make_model(
        set_comments: Iterable[Comment],
    ):
        # noinspection PyCallingNonCallable
        model: MpvqcCommentModel = MpvqcCommentModel()
        model.import_comments(list(set_comments))

        def config(binder: inject.Binder):
            binder.bind(PlayerService, MagicMock(spec_set=PlayerService))

        inject.configure(config, clear=True)

        return model

    return _make_model


@pytest.fixture
def model(make_model):
    # noinspection PyArgumentList
    return make_model(set_comments=DEFAULT_COMMENTS_SEARCH)


@pytest.fixture
def controller(model) -> MpvqcSearchBoxController:
    # noinspection PyCallingNonCallable
    controller = MpvqcSearchBoxController()
    controller.model = model
    return controller


@pytest.fixture
def select(controller):
    def _select_index(index: int):
        controller.selectedIndex = index

    return _select_index


@pytest.fixture
def search(controller) -> Callable[[str], tuple[int, int, int]]:
    def _search(query):
        controller.search(query)
        return controller.nextIndex, controller.currentResult, controller.totalResults

    # noinspection PyTypeChecker
    return _search


@pytest.fixture
def get_next(controller) -> Callable[[], tuple[int, int, int]]:
    def _func():
        controller.selectNext()
        return controller.nextIndex, controller.currentResult, controller.totalResults

    # noinspection PyTypeChecker
    return _func


@pytest.fixture
def get_previous(controller) -> Callable[[], tuple[int, int, int]]:
    def _func():
        controller.selectPrevious()
        return controller.nextIndex, controller.currentResult, controller.totalResults

    # noinspection PyTypeChecker
    return _func


def test_search_with_empty_query(search):
    next_idx, current, total = search("")
    assert (next_idx, current, total) == (-1, -1, -1)


def test_search_no_match(search):
    next_idx, current, total = search("Query")
    assert (next_idx, current, total) == (-1, 0, 0)


def test_search_match(search, controller, make_spy):
    next_index_changed = make_spy(controller.nextIndexChanged)
    current_results_changed_spy = make_spy(controller.currentResultChanged)
    total_results_changed_spy = make_spy(controller.totalResultsChanged)

    next_idx, current, total = search("Word")

    assert (next_idx, current, total) == (0, 1, 7)

    assert next_index_changed.count() == 1
    assert next_index_changed.at(0, 0) == 0

    assert current_results_changed_spy.count() == 1
    assert current_results_changed_spy.at(0, 0) == 1

    assert total_results_changed_spy.count() == 1
    assert total_results_changed_spy.at(0, 0) == 7


def test_search_match_next(search, select, get_next):
    idx, current, total = search("Word")
    assert (idx, current, total) == (0, 1, 7)

    select(idx)

    idx, current, total = get_next()
    assert (idx, current, total) == (1, 2, 7)

    select(idx)

    idx, current, total = get_next()
    assert (idx, current, total) == (2, 3, 7)


def test_search_match_next_new_query(search, select, get_next):
    idx, current, total = search("Word")
    assert (idx, current, total) == (0, 1, 7)

    select(idx)

    idx, current, total = get_next()
    assert (idx, current, total) == (1, 2, 7)

    select(idx)

    idx, current, total = get_next()
    assert (idx, current, total) == (2, 3, 7)

    idx, current, total = search("4")
    assert (idx, current, total) == (3, 1, 1)


def test_search_match_next_after_import(model, search, select, get_next):
    idx, current, total = search("Word")
    assert (idx, current, total) == (0, 1, 7)

    select(idx)

    idx, current, total = get_next()
    assert (idx, current, total) == (1, 2, 7)

    select(idx)

    idx, current, total = get_next()
    assert (idx, current, total) == (2, 3, 7)

    model.import_comments(EXTRA_COMMENTS)
    select(8)

    idx, current, total = get_next()
    assert (idx, current, total) == (9, 9, 9)


def test_search_match_previous(search, select, get_previous):
    idx, current, total = search("Word")
    assert (idx, current, total) == (0, 1, 7)

    select(idx)

    idx, current, total = get_previous()
    assert (idx, current, total) == (7, 7, 7)

    select(idx)

    idx, current, total = get_previous()
    assert (idx, current, total) == (5, 6, 7)


def test_search_match_previous_with_selection_change(search, select, get_previous):
    idx, current, total = search("Word")
    assert (idx, current, total) == (0, 1, 7)

    select(idx)

    idx, current, total = get_previous()
    assert (idx, current, total) == (7, 7, 7)

    select(idx)

    idx, current, total = get_previous()
    assert (idx, current, total) == (5, 6, 7)

    select(index=2)

    idx, current, total = get_previous()
    assert (idx, current, total) == (1, 2, 7)


def test_search_match_previous_after_import(search, model, select, get_next, get_previous):
    idx, current, total = search("Word")
    assert (idx, current, total) == (0, 1, 7)

    select(idx)

    idx, current, total = get_next()
    assert (idx, current, total) == (1, 2, 7)

    select(idx)

    idx, current, total = get_next()
    assert (idx, current, total) == (2, 3, 7)

    model.import_comments(EXTRA_COMMENTS)

    select(index=8)

    idx, current, total = get_previous()
    assert (idx, current, total) == (7, 7, 9)


def test_search_wrap_around(search, select, get_next, get_previous):
    select(index=6)

    idx, current, total = search("Word")
    assert (idx, current, total) == (0, 1, 7)

    select(idx)

    idx, current, total = get_previous()
    assert (idx, current, total) == (7, 7, 7)

    select(idx)

    idx, current, total = get_previous()
    assert (idx, current, total) == (5, 6, 7)

    select(index=5)

    idx, current, total = get_next()
    assert (idx, current, total) == (7, 7, 7)

    select(idx)

    idx, current, total = get_next()
    assert (idx, current, total) == (0, 1, 7)
