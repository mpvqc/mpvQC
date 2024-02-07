#  mpvQC
#
#  Copyright (C) 2024 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from unittest.mock import MagicMock

import inject

from mpvqc.pyobjects import MpvqcCommentModelPyObject
from mpvqc.services import PlayerService


class TestCommentsModelSearch(unittest.TestCase):
    _query = ''
    _selected_index = -1

    def setUp(self):
        # noinspection PyCallingNonCallable
        self._model: MpvqcCommentModelPyObject = MpvqcCommentModelPyObject()
        self._model.import_comments([
            {'time': 0, 'commentType': 'commentType', 'comment': 'Word 1'},
            {'time': 0, 'commentType': 'commentType', 'comment': 'Word 2'},
            {'time': 0, 'commentType': 'commentType', 'comment': 'Word 3'},
            {'time': 0, 'commentType': 'commentType', 'comment': 'Word 4'},
            {'time': 0, 'commentType': 'commentType', 'comment': 'Word 5'},
            {'time': 0, 'commentType': 'commentType', 'comment': 'Word 6'},
            {'time': 0, 'commentType': 'commentType', 'comment': ''},
            {'time': 0, 'commentType': 'commentType', 'comment': 'Word 7'},
        ])

        mock = MagicMock()
        mock.current_time = 0
        inject.clear_and_configure(lambda binder: binder
                                   .bind(PlayerService, mock))

    def tearDown(self):
        inject.clear()

    def _search(self, query, include_current_row, top_down, selected_index):
        result = self._model.search(query, include_current_row, top_down, selected_index)
        self._query = query
        self._selected_index = result['nextIndex']
        return result['nextIndex'], result['currentResult'], result['totalResults']

    def _select(self, row_index: int):
        self._selected_index = row_index

    def _next(self):
        return self._search(self._query, include_current_row=False, top_down=True, selected_index=self._selected_index)

    def _previous(self):
        return self._search(self._query, include_current_row=False, top_down=False, selected_index=self._selected_index)

    def test_empty_search(self):
        next_idx, current_result, total_results = self._search(
            query='',
            include_current_row=True,
            top_down=True,
            selected_index=0
        )

        self.assertEqual(-1, next_idx)
        self.assertEqual(-1, current_result)
        self.assertEqual(-1, total_results)

    def test_no_match(self):
        next_idx, current_result, total_results = self._search(
            query='Query',
            include_current_row=True,
            top_down=True,
            selected_index=0
        )

        self.assertEqual(-1, next_idx)
        self.assertEqual(0, current_result)
        self.assertEqual(0, total_results)

    def test_match(self):
        next_idx, current_result, total_results = self._search(
            query='Word',
            include_current_row=True,
            top_down=True,
            selected_index=0
        )

        self.assertEqual(0, next_idx)
        self.assertEqual(1, current_result)
        self.assertEqual(7, total_results)

    def test_match_next(self):
        self._search(
            query='Word',
            include_current_row=True,
            top_down=True,
            selected_index=0
        )

        next_idx, current_result, total_results = self._next()
        self.assertEqual(1, next_idx)
        self.assertEqual(2, current_result)
        self.assertEqual(7, total_results)

        next_idx, current_result, total_results = self._next()
        self.assertEqual(2, next_idx)
        self.assertEqual(3, current_result)
        self.assertEqual(7, total_results)

    def test_match_next_new_query(self):
        self._search(
            query='Word',
            include_current_row=True,
            top_down=True,
            selected_index=0
        )

        self._next()
        self._next()

        next_idx, current_result, total_results = self._search(
            query='4',
            include_current_row=True,
            top_down=True,
            selected_index=0
        )
        self.assertEqual(3, next_idx)
        self.assertEqual(1, current_result)
        self.assertEqual(1, total_results)

    def test_match_previous(self):
        self._search(
            query='Word',
            include_current_row=True,
            top_down=True,
            selected_index=0
        )

        next_idx, current_result, total_results = self._previous()
        self.assertEqual(7, next_idx)
        self.assertEqual(7, current_result)
        self.assertEqual(7, total_results)

        next_idx, current_result, total_results = self._previous()
        self.assertEqual(5, next_idx)
        self.assertEqual(6, current_result)
        self.assertEqual(7, total_results)

    def test_match_previous_change_selection(self):
        self._search(
            query='Word',
            include_current_row=True,
            top_down=True,
            selected_index=0
        )

        self._previous()
        self._previous()
        self._select(row_index=2)

        next_idx, current_result, total_results = self._previous()
        self.assertEqual(1, next_idx)
        self.assertEqual(2, current_result)
        self.assertEqual(7, total_results)
