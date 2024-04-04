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

import unittest
from unittest.mock import MagicMock

import inject
from parameterized import parameterized

from mpvqc.models import Comment
from mpvqc.pyobjects.comment_model import MpvqcCommentModelPyObject, Role
from mpvqc.services import PlayerService


class TestCommentsModel(unittest.TestCase):
    _default_comments = [
        Comment(time=0, comment_type='commentType', comment='Word 1'),
        Comment(time=5, comment_type='commentType', comment='Word 2'),
        Comment(time=10, comment_type='commentType', comment='Word 3'),
        Comment(time=15, comment_type='commentType', comment='Word 4'),
        Comment(time=20, comment_type='commentType', comment='Word 5'),
    ]

    def setUp(self):
        # noinspection PyCallingNonCallable
        self._model: MpvqcCommentModelPyObject = MpvqcCommentModelPyObject()

        self._model.import_comments(self._default_comments[:])

        self._player_mock = MagicMock()
        self._player_mock.current_time = 0
        inject.clear_and_configure(lambda binder: binder
                                   .bind(PlayerService, self._player_mock))

    def tearDown(self):
        inject.clear()

    def _mock_player_time(self, time: int):
        self._player_mock.current_time = time

    def test_add_row_count(self):
        count = self._model.rowCount()
        self.assertEqual(count, 5)
        self._model.add_row('comment')
        self.assertEqual(count + 1, 6)

    @parameterized.expand([
        (0, 0.499999),
        (0, 0.500000),
        (1, 0.500001),
        (1, 1.499999),
        (2, 1.500001),
    ])
    def test_add_comment_time_rounded(self, expected, input_time):
        self._model.clear()
        self._mock_player_time(time=input_time)

        self._model.add_row('comment')

        index = self._model.index(0, 0)
        item = self._model.itemFromIndex(index)
        actual = item.data(Role.TIME)

        self.assertEqual(expected, actual)

    def test_add_row_sorting(self):
        self._mock_player_time(time=7)
        self._model.add_row('my custom comment type')

        item = self._model.item(2, 0)
        self.assertEqual('my custom comment type', item.data(Role.TYPE))

    def test_add_row_signals(self):
        signals_fired = {}

        def signal_fired(key, val=True):
            signals_fired[key] = val

        self._model.commentsChanged.connect(lambda: signal_fired('commentsChanged'))
        self._model.newItemAdded.connect(lambda idx: signal_fired('newItemAdded', idx))

        self._model.add_row('comment type')

        self.assertIsNotNone(signals_fired.get('commentsChanged', None))
        self.assertIsNotNone(signals_fired.get('newItemAdded', None))

    def test_add_row_invalidates_search(self):
        self._model._searcher._hits = ['result']
        self._model.add_row('comment type')

        self.assertIsNone(self._model._searcher._hits)

    def test_import_comments_signals(self):
        signals_fired = {}

        def signal_fired(key, val=True):
            signals_fired[key] = val

        self._model.commentsImported.connect(lambda: signal_fired('commentsImported'))

        self._model.import_comments([
            Comment(time=0, comment_type='commentType', comment='Word ok'),
        ])

        self.assertIsNotNone(signals_fired.get('commentsImported', None))

    def test_import_comments_invalidates_search(self):
        self._model._searcher._hits = ['result']
        self._model.import_comments([
            Comment(time=0, comment_type='commentType', comment='Word ok'),
        ])

        self.assertIsNone(self._model._searcher._hits)

    def test_remove_row(self):
        count = self._model.rowCount()
        self.assertEqual(count, 5)
        self._model.remove_row(0)
        self.assertEqual(count - 1, 4)

    def test_clear_comments(self):
        self._model.clear_comments()
        self.assertEqual(0, self._model.rowCount())

    def test_remove_row_signals(self):
        signals_fired = {}

        def signal_fired(key, val=True):
            signals_fired[key] = val

        self._model.commentsChanged.connect(lambda: signal_fired('commentsChanged'))

        self._model.remove_row(0)

        self.assertIsNotNone(signals_fired.get('commentsChanged', None))

    def test_remove_row_invalidates_search(self):
        self._model._searcher._hits = ['result']
        self._model.remove_row(0)

        self.assertIsNone(self._model._searcher._hits)

    def test_update_time_sorting(self):
        self._model.update_time(0, time=7)

        index = self._model.index(1, 0)
        item = self._model.itemFromIndex(index)
        data = item.data(Role.COMMENT)

        self.assertEqual(data, 'Word 1')

    def test_update_time_signals(self):
        signals_fired = {}

        def signal_fired(key, val=True):
            signals_fired[key] = val

        self._model.timeUpdated.connect(lambda: signal_fired('timeUpdated'))

        self._model.update_time(0, time=7)

        self.assertIsNotNone(signals_fired.get('timeUpdated', None))

    def test_update_time_invalidates_search(self):
        self._model._searcher._hits = ['result']
        self._model.update_time(0, time=7)

        self.assertIsNone(self._model._searcher._hits)

    def test_update_comment_invalidates_search(self):
        self._model._searcher._hits = ['result']
        self._model.update_comment(0, comment='new')

        self.assertIsNone(self._model._searcher._hits)

    def test_clear_comments_invalidates_search(self):
        self._model._searcher._hits = ['result']
        self._model.clear_comments()

        self.assertIsNone(self._model._searcher._hits)

    def test_get_all_comments(self):
        self.assertListEqual(self._default_comments, self.map_to_objects(self._model.comments()))

    def map_to_objects(self, comments: list):
        return list(map(lambda c: Comment(c['time'], c['commentType'], c['comment']), comments))


class TestCommentsModelSearch(unittest.TestCase):
    _query = ''
    _selected_index = -1
    _default_comments = [
        Comment(time=0, comment_type='commentType', comment='Word 1'),
        Comment(time=1, comment_type='commentType', comment='Word 2'),
        Comment(time=2, comment_type='commentType', comment='Word 3'),
        Comment(time=3, comment_type='commentType', comment='Word 4'),
        Comment(time=4, comment_type='commentType', comment='Word 5'),
        Comment(time=5, comment_type='commentType', comment='Word 6'),
        Comment(time=6, comment_type='commentType', comment=''),
        Comment(time=9, comment_type='commentType', comment='Word 9'),
    ]

    def setUp(self):
        # noinspection PyCallingNonCallable
        self._model: MpvqcCommentModelPyObject = MpvqcCommentModelPyObject()
        self._model.import_comments(self._default_comments)

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

    def _import(self):
        self._model.import_comments([
            Comment(time=7, comment_type='commentType', comment='Word 7'),
            Comment(time=8, comment_type='commentType', comment='Word 8'),
        ])
        self._select(row_index=8)

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

    def test_match_next_after_import(self):
        self._search(
            query='Word',
            include_current_row=True,
            top_down=True,
            selected_index=0
        )

        self._next()
        self._next()
        self._import()

        next_idx, current_result, total_results = self._next()
        self.assertEqual(9, next_idx)
        self.assertEqual(9, current_result)
        self.assertEqual(9, total_results)

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

    def test_match_previous_after_import(self):
        self._search(
            query='Word',
            include_current_row=True,
            top_down=True,
            selected_index=0
        )

        self._next()
        self._next()
        self._import()

        next_idx, current_result, total_results = self._previous()
        self.assertEqual(7, next_idx)
        self.assertEqual(7, current_result)
        self.assertEqual(9, total_results)

    def test_time_is_int(self):
        self._model.import_comments([
            Comment(time=999.99, comment_type='commentType', comment='Word 1'),
        ])
        comment = self._model.comments()[-1]
        self.assertEqual(999, comment['time'])
