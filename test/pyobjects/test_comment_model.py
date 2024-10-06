# mpvQC
#
# Copyright (C) 2024 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.models import Comment
from mpvqc.pyobjects.comment_model import MpvqcCommentModelPyObject, Role
from mpvqc.services import PlayerService

DEFAULT_COMMENTS = (
    Comment(time=0, comment_type="commentType", comment="Word 1"),
    Comment(time=5, comment_type="commentType", comment="Word 2"),
    Comment(time=10, comment_type="commentType", comment="Word 3"),
    Comment(time=15, comment_type="commentType", comment="Word 4"),
    Comment(time=20, comment_type="commentType", comment="Word 5"),
)

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


class SignalHelper:
    """Helper class to help with signal logging"""

    def __init__(self):
        self.signals_fired = {}

    def log(self, signal_name: str, val=True):
        self.signals_fired[signal_name] = val

    def has_logged(self, signal_name: str) -> bool:
        return signal_name in self.signals_fired


@pytest.fixture()
def signal_helper() -> SignalHelper:
    return SignalHelper()


class SearchHelper:
    """Helper class to abstract search functionality"""

    def __init__(self):
        self._model = make_model(set_comments=list(DEFAULT_COMMENTS_SEARCH))
        self._query = ""
        self._selected_index = -1

    def search(
        self,
        query: str,
        include_current_row: bool,
        top_down: bool,
        selected_index: int,
    ) -> tuple[int, int, int]:
        result = self._model.search(query, include_current_row, top_down, selected_index)
        self._query = query
        self._selected_index = result["nextIndex"]
        return result["nextIndex"], result["currentResult"], result["totalResults"]

    def select(self, index: int):
        self._selected_index = index

    def next(self) -> tuple[int, int, int]:
        return self.search(self._query, include_current_row=False, top_down=True, selected_index=self._selected_index)

    def previous(self) -> tuple[int, int, int]:
        return self.search(self._query, include_current_row=False, top_down=False, selected_index=self._selected_index)

    def import_more_comments(self):
        comments = [
            Comment(time=7, comment_type="commentType", comment="Word 7"),
            Comment(time=8, comment_type="commentType", comment="Word 8"),
        ]
        self._model.import_comments(comments)
        self.select(index=8)


@pytest.fixture()
def search_helper() -> SearchHelper:
    return SearchHelper()


def make_model(
    set_comments=DEFAULT_COMMENTS,
    set_player_time: int | float = 0,
) -> MpvqcCommentModelPyObject:
    # noinspection PyCallingNonCallable
    model: MpvqcCommentModelPyObject = MpvqcCommentModelPyObject()
    model.import_comments(set_comments)

    player_mock = MagicMock()
    player_mock.current_time = set_player_time

    inject.clear_and_configure(lambda binder: binder.bind(PlayerService, player_mock))

    return model


def test_add_comment():
    model = make_model()
    assert model.rowCount() == 5
    model.add_row("comment type")
    assert model.rowCount() == 6


@pytest.mark.parametrize(
    "expected,test_input",
    [
        (0, 0.499999),
        (0, 0.500000),
        (1, 0.500001),
        (1, 1.499999),
        (2, 1.500001),
    ],
)
def test_add_comment_rounds_time(expected, test_input):
    model = make_model(set_comments=[], set_player_time=test_input)

    model.add_row("comment type")

    item = model.item(0, 0)
    actual = item.data(Role.TIME)
    assert expected == actual


def test_add_comment_sorts_model():
    custom_comment_type = "my custom comment type"
    model = make_model(set_player_time=7)

    model.add_row(custom_comment_type)

    item = model.item(2, 0)
    actual = item.data(Role.TYPE)
    assert custom_comment_type == actual


def test_add_comment_invalidates_search_results():
    model = make_model()
    model._searcher._hits = ["result"]

    model.add_row("comment type")

    assert model._searcher._hits is None


def test_add_comment_fires_signals(signal_helper):
    model = make_model()
    model.commentsChanged.connect(lambda: signal_helper.log("commentsChanged"))
    model.newItemAdded.connect(lambda idx: signal_helper.log("newItemAdded", idx))

    model.add_row("comment type")

    assert signal_helper.has_logged("commentsChanged")
    assert signal_helper.has_logged("newItemAdded")


def test_import_comments():
    model = make_model()
    # noinspection PyTypeChecker
    comment = Comment(time=999.99, comment_type="commentType", comment="Word 1")

    assert model.rowCount() == 5
    model.import_comments([comment])
    assert model.rowCount() == 6

    # Ensure even importing float time properties results in time being stored as int
    assert 999 == model.comments()[-1]["time"]


def test_import_comments_invalidates_search_results():
    model = make_model()
    model._searcher._hits = ["result"]

    model.import_comments(list(DEFAULT_COMMENTS))

    assert model._searcher._hits is None


def test_import_comments_fires_signals(signal_helper):
    model = make_model()
    model.commentsImported.connect(lambda: signal_helper.log("commentsImported"))

    model.import_comments(list(DEFAULT_COMMENTS))

    assert signal_helper.has_logged("commentsImported")


def test_remove_comment():
    model = make_model()
    assert model.rowCount() == 5
    model.remove_row(0)
    assert model.rowCount() == 4


def test_remove_comment_invalidates_search_results():
    model = make_model()
    model._searcher._hits = ["result"]

    model.remove_row(0)

    assert model._searcher._hits is None


def test_remove_comment_fires_signals(signal_helper):
    model = make_model()
    model.commentsChanged.connect(lambda: signal_helper.log("commentsChanged"))

    model.remove_row(0)

    assert signal_helper.has_logged("commentsChanged")


def test_clear_comments():
    model = make_model()
    model.clear_comments()
    assert 0 == model.rowCount()


def test_clear_comments_invalidates_search_results():
    model = make_model()
    model._searcher._hits = ["result"]

    model.clear_comments()

    assert model._searcher._hits is None


def test_update_time_sorts_model_again():
    model = make_model()
    model.update_time(row=0, time=7)

    item = model.item(1, 0)
    actual = item.data(Role.COMMENT)

    assert actual == "Word 1"


def test_update_time_invalidates_search_results():
    model = make_model()
    model._searcher._hits = ["result"]

    model.update_time(row=0, time=7)

    assert model._searcher._hits is None


def test_update_time_fires_signals(signal_helper):
    model = make_model()
    model.timeUpdated.connect(lambda: signal_helper.log("timeUpdated"))

    model.update_time(row=0, time=7)

    assert signal_helper.has_logged("timeUpdated")


def test_update_comment_invalidates_search_results():
    model = make_model()
    model._searcher._hits = ["result"]

    model.update_comment(index=0, comment="new")

    assert model._searcher._hits is None


def test_get_all_comments():
    model = make_model()

    actual = [
        Comment(time=comment["time"], comment_type=comment["commentType"], comment=comment["comment"])
        for comment in model.comments()
    ]

    assert actual == list(DEFAULT_COMMENTS)


def test_search_with_empty_query(search_helper):
    next_idx, current_result, total_results = search_helper.search(
        query="", include_current_row=True, top_down=True, selected_index=0
    )
    assert -1 == next_idx
    assert -1 == current_result
    assert -1 == total_results


def test_search_no_match(search_helper):
    next_idx, current_result, total_results = search_helper.search(
        query="Query", include_current_row=True, top_down=True, selected_index=0
    )
    assert -1 == next_idx
    assert 0 == current_result
    assert 0 == total_results


def test_search_match(search_helper):
    next_idx, current_result, total_results = search_helper.search(
        query="Word", include_current_row=True, top_down=True, selected_index=0
    )
    assert 0 == next_idx
    assert 1 == current_result
    assert 7 == total_results


def test_search_match_next(search_helper):
    search_helper.search(query="Word", include_current_row=True, top_down=True, selected_index=0)

    next_idx, current_result, total_results = search_helper.next()
    assert 1 == next_idx
    assert 2 == current_result
    assert 7 == total_results

    next_idx, current_result, total_results = search_helper.next()
    assert 2 == next_idx
    assert 3 == current_result
    assert 7 == total_results


def test_search_match_next_new_query(search_helper):
    search_helper.search(query="Word", include_current_row=True, top_down=True, selected_index=0)
    search_helper.next()
    search_helper.next()

    next_idx, current_result, total_results = search_helper.search(
        query="4", include_current_row=True, top_down=True, selected_index=0
    )
    assert 3 == next_idx
    assert 1 == current_result
    assert 1 == total_results


def test_search_match_next_after_import(search_helper):
    search_helper.search(query="Word", include_current_row=True, top_down=True, selected_index=0)
    search_helper.next()
    search_helper.next()
    search_helper.import_more_comments()

    next_idx, current_result, total_results = search_helper.next()
    assert 9 == next_idx
    assert 9 == current_result
    assert 9 == total_results


def test_search_match_previous(search_helper):
    search_helper.search(query="Word", include_current_row=True, top_down=True, selected_index=0)

    next_idx, current_result, total_results = search_helper.previous()
    assert 7 == next_idx
    assert 7 == current_result
    assert 7 == total_results

    next_idx, current_result, total_results = search_helper.previous()
    assert 5 == next_idx
    assert 6 == current_result
    assert 7 == total_results


def test_search_match_previous_with_selection_change(search_helper):
    search_helper.search(query="Word", include_current_row=True, top_down=True, selected_index=0)
    search_helper.previous()
    search_helper.previous()
    search_helper.select(index=2)

    next_idx, current_result, total_results = search_helper.previous()
    assert 1 == next_idx
    assert 2 == current_result
    assert 7 == total_results


def test_search_match_previous_after_import(search_helper):
    search_helper.search(query="Word", include_current_row=True, top_down=True, selected_index=0)
    search_helper.next()
    search_helper.next()
    search_helper.import_more_comments()

    next_idx, current_result, total_results = search_helper.previous()
    assert 7 == next_idx
    assert 7 == current_result
    assert 9 == total_results
