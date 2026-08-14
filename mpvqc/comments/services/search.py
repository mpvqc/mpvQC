# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import bisect
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .selection import SelectionState
    from .store import Store


@dataclass(frozen=True)
class NoQuery:
    """The query is empty. Search is inactive."""


@dataclass(frozen=True)
class NoMatches:
    """The query matched no comment."""


@dataclass(frozen=True)
class Found:
    index: int
    current: int
    total: int


type SearchOutcome = NoQuery | NoMatches | Found


class CommentSearchEngine:
    def __init__(self, store: Store, selection: SelectionState) -> None:
        self._store = store
        self._selection = selection
        self._query = ""
        self._hits: list[int] | None = None

    def invalidate(self) -> None:
        self._hits = None

    def search(self, query: str, *, include_current_row: bool, top_down: bool) -> SearchOutcome:
        if not query:
            self._query = ""
            self._hits = None
            return NoQuery()

        query_changed = self._query != query
        if query_changed or self._hits is None:
            self._query = query
            self._hits = self._store.search_rows(query)

        if not self._hits:
            return NoMatches()

        total = len(self._hits)

        if query_changed:
            return Found(index=self._hits[0], current=1, total=total)

        selected_index = cast("int", self._selection.selectedRow)

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

        return Found(index=self._hits[idx], current=idx + 1, total=total)
