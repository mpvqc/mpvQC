# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import bisect
from collections.abc import Callable

from PySide6.QtCore import Property, QAbstractItemModel, QObject, Qt, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.models import MpvqcCommentModel
from mpvqc.models.comments.roles import Role

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcSearchBoxController(QObject):
    modelChanged = Signal(MpvqcCommentModel)
    selectedIndexChanged = Signal(int)

    nextIndexChanged = Signal(int)
    currentResultChanged = Signal(int)
    totalResultsChanged = Signal(int)
    searchQueryChanged = Signal(str)

    highlightRequested = Signal(int)

    def __init__(self):
        super().__init__()
        self._search_backend = SearchBackend()

        self._next_index = -1
        self._current_result = -1
        self._total_results = -1
        self._search_query = ""

        self._model: QAbstractItemModel | None = None
        self._selected_index: int = -1
        self._search_invalidate_connection = None

    @Property(MpvqcCommentModel, notify=modelChanged)
    def model(self) -> MpvqcCommentModel:
        if self._model is None:
            raise ValueError
        # noinspection PyTypeChecker
        return self._model

    @model.setter
    def model(self, model: MpvqcCommentModel) -> None:
        if self._search_invalidate_connection is not None and model is not None:
            self._search_invalidate_connection.disconnect(self._model)

        self._model = model
        # noinspection PyUnresolvedReferences
        self._search_invalidate_connection = model.searchInvalidated.connect(self._search_backend.invalidate)

    @Property(int, notify=selectedIndexChanged)
    def selectedIndex(self) -> int:
        return self._selected_index

    @selectedIndex.setter
    def selectedIndex(self, value: int) -> None:
        if self._selected_index != value:
            self._selected_index = value
            self.selectedIndexChanged.emit(value)

    @Property(int, notify=nextIndexChanged)
    def nextIndex(self) -> int:
        return self._next_index

    def _set_next_index(self, value: int) -> None:
        if self._next_index != value:
            self._next_index = value
            self.nextIndexChanged.emit(value)

    @Property(int, notify=currentResultChanged)
    def currentResult(self) -> int:
        return self._current_result

    def _set_current_result(self, value: int) -> None:
        if self._current_result != value:
            self._current_result = value
            self.currentResultChanged.emit(value)

    @Property(int, notify=totalResultsChanged)
    def totalResults(self) -> int:
        return self._total_results

    def _set_total_results(self, value: int) -> None:
        if self._total_results != value:
            self._total_results = value
            self.totalResultsChanged.emit(value)

    @Property(str, notify=searchQueryChanged)
    def searchQuery(self) -> str:
        return self._search_query

    def _set_search_query(self, query: str) -> None:
        if self._search_query != query:
            self._search_query = query
            self.searchQueryChanged.emit(query)

    @Slot(str)
    def search(self, query: str) -> None:
        self._set_search_query(query)
        self._search(include_current_row=True, top_down=True)

    @Slot()
    def selectNext(self) -> None:
        self._search(include_current_row=False, top_down=True)

    @Slot()
    def selectPrevious(self) -> None:
        self._search(include_current_row=False, top_down=False)

    def _search(self, include_current_row: bool, top_down: bool) -> dict:
        result = self._search_backend.search(
            query=self._search_query,
            include_current_row=include_current_row,
            top_down=top_down,
            selected_index=self._selected_index,
            search_func=self._search_func,
        )

        next_index = result["nextIndex"]
        current_result = result["currentResult"]
        total_result = result["totalResults"]

        self._set_next_index(next_index)
        self._set_current_result(current_result)
        self._set_total_results(total_result)

        if next_index >= 0:
            self.highlightRequested.emit(next_index)

    # noinspection PyUnresolvedReferences,PyTypeChecker
    def _search_func(self, query: str) -> list[int]:
        from_beginning = self._model.index(0, 0)
        role = Role.COMMENT
        flags = Qt.MatchFlag.MatchContains | Qt.MatchFlag.MatchWrap
        all_results = -1  # Search everything
        results = self._model.match(from_beginning, role, query, all_results, flags)
        results = sorted(results)
        return [m_idx.row() for m_idx in results]


class SearchBackend:
    def __init__(self):
        self._query = ""
        self._hits: list[int] | None = None

    def invalidate(self):
        self._hits = None

    def search(
        self,
        query: str,
        include_current_row: bool,
        top_down: bool,
        selected_index: int,
        search_func: Callable[[str], list[int]],
    ) -> dict:
        if not query:
            self._query = ""
            self._hits = None
            return {"nextIndex": -1, "currentResult": -1, "totalResults": -1}

        # Check if we need new search results
        query_changed = self._query != query
        if query_changed or self._hits is None:
            self._query = query
            self._hits = search_func(query)

        # No matches found
        if not self._hits:
            return {"nextIndex": -1, "currentResult": 0, "totalResults": 0}

        total = len(self._hits)

        # First result for new query
        if query_changed:
            return {"nextIndex": self._hits[0], "currentResult": 1, "totalResults": total}

        # Find next/previous result
        if top_down:
            start = selected_index if include_current_row else selected_index + 1
            idx = bisect.bisect_left(self._hits, start)
            if idx >= total:
                idx = 0  # Wrap to beginning
        else:
            end = selected_index if include_current_row else selected_index - 1
            idx = bisect.bisect_right(self._hits, end) - 1
            if idx < 0:
                idx = total - 1  # Wrap to end

        return {"nextIndex": self._hits[idx], "currentResult": idx + 1, "totalResults": total}
