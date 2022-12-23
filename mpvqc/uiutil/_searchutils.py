# mpvQC
#
# Copyright (C) 2020 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import bisect
from typing import Optional, List, NamedTuple, Tuple

from PyQt5.QtCore import Qt, QModelIndex, QObject, QItemSelectionModel, QAbstractItemModel, pyqtSignal, pyqtSlot


class _Result(NamedTuple):
    results: Optional[List[QModelIndex]]
    results_row_idx: Optional[List[int]]

    def first(self) -> Tuple[Optional[QModelIndex], int, int]:
        if self.results is None:  # Query was empty
            return None, -1, -1
        if not self.results:  # Nothing found
            return None, 0, 0
        m_idx = self.results[0]
        current = 1
        total = len(self.results)
        return m_idx, current, total

    def next(self, cur_row: int, top_down: bool, incl_cur_row: bool) -> Tuple[Optional[QModelIndex], int, int]:
        if self.results is None:  # Query was empty
            return None, -1, -1
        if not self.results:  # Nothing found
            return None, 0, 0
        total = len(self.results)
        if top_down:
            next_idx = bisect.bisect_right(self.results_row_idx, cur_row - incl_cur_row) % total
        else:
            next_idx = (bisect.bisect_left(self.results_row_idx, cur_row + incl_cur_row) - 1) % total
        m_idx = self.results[next_idx]
        return m_idx, next_idx + 1, total


class CommentsTableSearcher(QObject):

    @staticmethod
    def search(query: str, model: QAbstractItemModel) -> _Result:
        if not query:
            return _Result(None, None)

        start = model.index(0, 2)
        role = Qt.DisplayRole
        hits = -1  # all hits
        flags = Qt.MatchContains | Qt.MatchWrap
        results = sorted(model.match(start, role, query, hits, flags))
        results_row_idx = list(map(lambda m_idx: m_idx.row(), results))
        return _Result(results, results_row_idx)

    # Invoked, whenever the next/previous result should be selected
    # p1='the new model index to select'
    # p2='current hit'
    # p3='total hits'
    highlight = pyqtSignal(object, int, int)

    def __init__(self, parent, model: QAbstractItemModel, model_sel: QItemSelectionModel):
        super().__init__(parent)

        self.__model = model
        self.__model_sel = model_sel

        self.__query = ""
        self.__result: Optional[_Result] = None

    def __get_result(self) -> _Result:
        if not self.__result:
            self.__result = CommentsTableSearcher.search(self.__query, self.__model)
        return self.__result

    def __first(self):
        m_idx, current, total = self.__get_result().first()
        self.highlight.emit(m_idx, current, total)

    def __next(self, top_down: bool, incl_cur_row: bool):
        current_row = self.__model_sel.currentIndex().row()
        m_idx, current, total = self.__get_result().next(current_row, top_down, incl_cur_row)
        self.highlight.emit(m_idx, current, total)

    @pyqtSlot()
    def on_comments_changed(self):
        self.__result = None

    @pyqtSlot()
    def on_search_shown(self):
        self.__next(top_down=True, incl_cur_row=True)

    @pyqtSlot()
    def on_search_hidden(self):
        pass

    @pyqtSlot(str)
    def on_search_query_changed(self, query: str):
        self.__result = None
        self.__query = query
        self.__first()

    @pyqtSlot()
    def on_search_next_result(self):
        self.__next(top_down=True, incl_cur_row=False)

    @pyqtSlot()
    def on_search_previous_result(self):
        self.__next(top_down=False, incl_cur_row=False)
