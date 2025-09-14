# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


import bisect
from collections.abc import Callable
from dataclasses import dataclass


def report_result(next_idx: int, current_result: int, total_results: int):
    return {"nextIndex": next_idx, "currentResult": current_result, "totalResults": total_results}


@dataclass
class Hits:
    row_indexes_matched: list[int]

    def first(self):
        total = len(self.row_indexes_matched)
        if total == 0:
            return self._no_results()
        return report_result(next_idx=self.row_indexes_matched[0], current_result=1, total_results=total)

    def next(self, include_current_row: bool, top_down: bool, current_row: int):
        total = len(self.row_indexes_matched)
        if total == 0:
            return self._no_results()
        if top_down:
            next_idx = bisect.bisect_right(self.row_indexes_matched, current_row - include_current_row) % total
        else:
            next_idx = (bisect.bisect_left(self.row_indexes_matched, current_row + include_current_row) - 1) % total
        return report_result(
            next_idx=self.row_indexes_matched[next_idx], current_result=next_idx + 1, total_results=total
        )

    @staticmethod
    def _no_results():
        return report_result(next_idx=-1, current_result=0, total_results=0)


class Searcher:
    def __init__(self):
        self._last_query = ""
        self._hits: Hits | None = None

    def search(
        self,
        query: str,
        include_current_row: bool,
        top_down: bool,
        selected_index: int,
        search_func: Callable[[str], list[int]],
    ):
        if query == "":
            self._last_query = query
            self._hits = None
            return report_result(-1, -1, -1)

        query_has_changed = self._last_query != query
        self._last_query = query

        if self._hits is None or query_has_changed:
            self._hits = Hits(row_indexes_matched=search_func(query))

        if query_has_changed:
            return self._hits.first()

        return self._hits.next(include_current_row=include_current_row, top_down=top_down, current_row=selected_index)

    def invalidate(self):
        self._hits = None
