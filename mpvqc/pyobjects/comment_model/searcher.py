# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import bisect
from collections.abc import Callable


class Searcher:
    def __init__(self):
        self._query = ""
        self._hits: list[int] | None = None

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

    def invalidate(self):
        self._hits = None
