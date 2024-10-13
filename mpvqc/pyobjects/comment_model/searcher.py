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


import bisect
from dataclasses import dataclass
from typing import Callable


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
