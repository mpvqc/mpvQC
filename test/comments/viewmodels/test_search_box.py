# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import inject
import pytest

from mpvqc.comments.services import CommentsService, Found, NoMatches, NoQuery, SearchOutcome
from mpvqc.comments.viewmodels import MpvqcCommentSearchBoxViewModel


class SearchCall(NamedTuple):
    query: str
    include_current_row: bool
    top_down: bool


class CommentsServiceMock:
    """Doubles the comments service surface the view model consumes: a stubbed search method."""

    def __init__(self):
        assert callable(CommentsService.search), "mocked surface drifted: not a plain method anymore"
        self.calls: list[SearchCall] = []
        self._outcome: SearchOutcome = NoQuery()

    def returning(self, outcome: SearchOutcome) -> None:
        self._outcome = outcome

    def search(self, query: str, *, include_current_row: bool, top_down: bool) -> SearchOutcome:
        self.calls.append(SearchCall(query, include_current_row, top_down))
        return self._outcome


@pytest.fixture
def comments_service_mock() -> CommentsServiceMock:
    return CommentsServiceMock()


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, comments_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(CommentsService, comments_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def view_model() -> MpvqcCommentSearchBoxViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcCommentSearchBoxViewModel()


class OutcomeCase(NamedTuple):
    name: str
    outcome: SearchOutcome
    label: str
    has_multiple: bool
    highlighted_index: int | None


@pytest.mark.parametrize(
    "case",
    [
        OutcomeCase(
            name="a single match renders current over total without has-multiple",
            outcome=Found(index=4, current=1, total=1),
            label="1/1",
            has_multiple=False,
            highlighted_index=4,
        ),
        OutcomeCase(
            name="several matches render current over total and set has-multiple",
            outcome=Found(index=2, current=3, total=5),
            label="3/5",
            has_multiple=True,
            highlighted_index=2,
        ),
        OutcomeCase(
            name="no matches render 0/0",
            outcome=NoMatches(),
            label="0/0",
            has_multiple=False,
            highlighted_index=None,
        ),
        OutcomeCase(
            name="no query renders an empty label",
            outcome=NoQuery(),
            label="",
            has_multiple=False,
            highlighted_index=None,
        ),
    ],
    ids=lambda case: case.name,
)
def test_outcome_maps_to_state(case, view_model, comments_service_mock, make_spy):
    comments_service_mock.returning(case.outcome)
    highlight_spy = make_spy(view_model.highlightRequested)

    view_model.search("query")

    assert view_model.statusLabel == case.label
    assert view_model.hasMultipleResults == case.has_multiple
    if case.highlighted_index is None:
        assert highlight_spy.count() == 0
    else:
        assert highlight_spy.count() == 1
        assert highlight_spy.at(invocation=0, argument=0) == case.highlighted_index


def test_search_query_changed_dedupes_repeats(view_model, comments_service_mock, make_spy):
    comments_service_mock.returning(NoMatches())
    spy = make_spy(view_model.searchQueryChanged)

    view_model.search("Query")
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == "Query"

    view_model.selectNext()
    assert spy.count() == 1

    view_model.selectPrevious()
    assert spy.count() == 1

    view_model.search("Query")
    assert spy.count() == 1

    view_model.search("Other Query")
    assert spy.count() == 2


def test_status_label_and_has_multiple_emit_only_on_change(view_model, comments_service_mock, make_spy):
    status_spy = make_spy(view_model.statusLabelChanged)
    has_multiple_spy = make_spy(view_model.hasMultipleResultsChanged)

    comments_service_mock.returning(Found(index=0, current=1, total=3))
    view_model.search("Word")
    assert status_spy.count() == 1
    assert has_multiple_spy.count() == 1

    view_model.search("Word")
    assert status_spy.count() == 1
    assert has_multiple_spy.count() == 1

    comments_service_mock.returning(Found(index=1, current=2, total=3))
    view_model.selectNext()
    assert status_spy.count() == 2
    assert has_multiple_spy.count() == 1


def test_highlight_fires_on_every_found_including_repeats(view_model, comments_service_mock, make_spy):
    comments_service_mock.returning(Found(index=2, current=1, total=1))
    spy = make_spy(view_model.highlightRequested)

    view_model.search("Word")
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == 2

    view_model.search("Word")
    assert spy.count() == 2
    assert spy.at(invocation=1, argument=0) == 2


def test_slots_forward_flags_and_reuse_the_stored_query(view_model, comments_service_mock):
    comments_service_mock.returning(Found(index=0, current=1, total=2))

    view_model.search("Query")
    assert comments_service_mock.calls[-1] == SearchCall(query="Query", include_current_row=True, top_down=True)

    view_model.selectNext()
    assert comments_service_mock.calls[-1] == SearchCall(query="Query", include_current_row=False, top_down=True)

    view_model.selectPrevious()
    assert comments_service_mock.calls[-1] == SearchCall(query="Query", include_current_row=False, top_down=False)
