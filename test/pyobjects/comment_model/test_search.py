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

import pytest

from mpvqc.models import Comment

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


class SearchHelper:
    """Helper class to abstract search functionality"""

    def __init__(self, model):
        self._model = model
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


@pytest.fixture
def search_helper(make_model) -> SearchHelper:
    # noinspection PyArgumentList
    model, _ = make_model(
        set_comments=DEFAULT_COMMENTS_SEARCH,
    )
    return SearchHelper(model)


def test_search_with_empty_query(search_helper):
    next_idx, current_result, total_results = search_helper.search(
        query="", include_current_row=True, top_down=True, selected_index=0
    )
    assert next_idx == -1
    assert current_result == -1
    assert total_results == -1


def test_search_no_match(search_helper):
    next_idx, current_result, total_results = search_helper.search(
        query="Query", include_current_row=True, top_down=True, selected_index=0
    )
    assert next_idx == -1
    assert current_result == 0
    assert total_results == 0


def test_search_match(search_helper):
    next_idx, current_result, total_results = search_helper.search(
        query="Word", include_current_row=True, top_down=True, selected_index=0
    )
    assert next_idx == 0
    assert current_result == 1
    assert total_results == 7


def test_search_match_next(search_helper):
    search_helper.search(query="Word", include_current_row=True, top_down=True, selected_index=0)

    next_idx, current_result, total_results = search_helper.next()
    assert next_idx == 1
    assert current_result == 2
    assert total_results == 7

    next_idx, current_result, total_results = search_helper.next()
    assert next_idx == 2
    assert current_result == 3
    assert total_results == 7


def test_search_match_next_new_query(search_helper):
    search_helper.search(query="Word", include_current_row=True, top_down=True, selected_index=0)
    search_helper.next()
    search_helper.next()

    next_idx, current_result, total_results = search_helper.search(
        query="4", include_current_row=True, top_down=True, selected_index=0
    )
    assert next_idx == 3
    assert current_result == 1
    assert total_results == 1


def test_search_match_next_after_import(search_helper):
    search_helper.search(query="Word", include_current_row=True, top_down=True, selected_index=0)
    search_helper.next()
    search_helper.next()
    search_helper.import_more_comments()

    next_idx, current_result, total_results = search_helper.next()
    assert next_idx == 9
    assert current_result == 9
    assert total_results == 9


def test_search_match_previous(search_helper):
    search_helper.search(query="Word", include_current_row=True, top_down=True, selected_index=0)

    next_idx, current_result, total_results = search_helper.previous()
    assert next_idx == 7
    assert current_result == 7
    assert total_results == 7

    next_idx, current_result, total_results = search_helper.previous()
    assert next_idx == 5
    assert current_result == 6
    assert total_results == 7


def test_search_match_previous_with_selection_change(search_helper):
    search_helper.search(query="Word", include_current_row=True, top_down=True, selected_index=0)
    search_helper.previous()
    search_helper.previous()
    search_helper.select(index=2)

    next_idx, current_result, total_results = search_helper.previous()
    assert next_idx == 1
    assert current_result == 2
    assert total_results == 7


def test_search_match_previous_after_import(search_helper):
    search_helper.search(query="Word", include_current_row=True, top_down=True, selected_index=0)
    search_helper.next()
    search_helper.next()
    search_helper.import_more_comments()

    next_idx, current_result, total_results = search_helper.previous()
    assert next_idx == 7
    assert current_result == 7
    assert total_results == 9
