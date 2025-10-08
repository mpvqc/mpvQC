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

    searchQueryChanged = Signal(str)
    hasMultipleResultsChanged = Signal(bool)
    statusLabelChanged = Signal(str)
    highlightRequested = Signal(int)

    def __init__(self):
        super().__init__()
        self._search_backend = SearchBackend()

        self._current_result = -1
        self._total_results = -1

        self._search_query = ""
        self._has_multiple_results = False
        self._status_label = ""

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

    @Property(str, notify=searchQueryChanged)
    def searchQuery(self) -> str:
        return self._search_query

    @Property(bool, notify=hasMultipleResultsChanged)
    def hasMultipleResults(self) -> bool:
        return self._has_multiple_results

    @Property(str, notify=statusLabelChanged)
    def statusLabel(self) -> str:
        return self._status_label

    def _update_search_state(self, query: str, current: int, total: int) -> None:
        if self._search_query != query:
            self._search_query = query
            self.searchQueryChanged.emit(query)

        self._current_result = current
        self._total_results = total

        has_multiple = total > 1
        if self._has_multiple_results != has_multiple:
            self._has_multiple_results = has_multiple
            self.hasMultipleResultsChanged.emit(has_multiple)

        label = f"{current}/{total}" if current >= 0 and total >= 0 else ""

        if self._status_label != label:
            self._status_label = label
            self.statusLabelChanged.emit(label)

    @Slot(str)
    def search(self, query: str) -> None:
        self._perform_search(query, include_current_row=True, top_down=True)

    @Slot()
    def selectNext(self) -> None:
        self._perform_search(self._search_query, include_current_row=False, top_down=True)

    @Slot()
    def selectPrevious(self) -> None:
        self._perform_search(self._search_query, include_current_row=False, top_down=False)

    def _perform_search(self, query: str, include_current_row: bool, top_down: bool) -> None:
        next_index, current_result, total_results = self._search_backend.search(
            query=query,
            include_current_row=include_current_row,
            top_down=top_down,
            selected_index=self._selected_index,
            search_func=self._search_func,
        )

        self._update_search_state(query, current_result, total_results)

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
    ) -> tuple[int, int, int]:
        """Perform a search and return a tuple of (next_index, current_result_number, total_results)."""

        if not query:
            self._query = ""
            self._hits = None
            return -1, -1, -1

        query_changed = self._query != query
        if query_changed or self._hits is None:
            self._query = query
            self._hits = search_func(query)

        if not self._hits:
            return -1, 0, 0

        total = len(self._hits)

        if query_changed:
            return self._hits[0], 1, total

        if top_down:
            start = selected_index if include_current_row else selected_index + 1
            idx = bisect.bisect_left(self._hits, start)
            if idx >= total:
                idx = 0
        else:
            end = selected_index if include_current_row else selected_index - 1
            idx = bisect.bisect_right(self._hits, end) - 1
            if idx < 0:
                idx = total - 1

        return self._hits[idx], idx + 1, total
