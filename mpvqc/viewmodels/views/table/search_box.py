# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import assert_never

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import CommentsService, MainWindowService
from mpvqc.services.comments import Found, NoMatches, NoQuery

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcSearchBoxViewModel(QObject):
    _comments_service = inject.attr(CommentsService)
    _main_window = inject.attr(MainWindowService)

    searchQueryChanged = Signal(str)
    hasMultipleResultsChanged = Signal(bool)
    statusLabelChanged = Signal(str)
    highlightRequested = Signal(int)
    isMainWindowFocusedChanged = Signal(bool)

    def __init__(self) -> None:
        super().__init__()
        self._search_query = ""
        self._has_multiple_results = False
        self._status_label = ""

        self._main_window.is_main_window_focused_changed.connect(self.isMainWindowFocusedChanged)

    @Property(str, notify=searchQueryChanged)
    def searchQuery(self) -> str:
        return self._search_query

    @Property(bool, notify=hasMultipleResultsChanged)
    def hasMultipleResults(self) -> bool:
        return self._has_multiple_results

    @Property(str, notify=statusLabelChanged)
    def statusLabel(self) -> str:
        return self._status_label

    @Property(bool, notify=isMainWindowFocusedChanged)
    def isMainWindowFocused(self) -> bool:
        return self._main_window.is_main_window_focused

    def _update_search_state(self, query: str, *, label: str, has_multiple: bool) -> None:
        if self._search_query != query:
            self._search_query = query
            self.searchQueryChanged.emit(query)

        if self._has_multiple_results != has_multiple:
            self._has_multiple_results = has_multiple
            self.hasMultipleResultsChanged.emit(has_multiple)

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
        outcome = self._comments_service.search(query, include_current_row=include_current_row, top_down=top_down)

        match outcome:
            case Found(index, current, total):
                self._update_search_state(query, label=f"{current}/{total}", has_multiple=total > 1)
                self.highlightRequested.emit(index)
            case NoMatches():
                self._update_search_state(query, label="0/0", has_multiple=False)
            case NoQuery():
                self._update_search_state(query, label="", has_multiple=False)
            case _:
                assert_never(outcome)
