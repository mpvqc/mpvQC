/*
mpvQC

Copyright (C) 2024 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick


QtObject {
    id: root

    required property var searchFunc // params: query: str, include_current_row: bool, top_down: bool

    property int currentResult: -1
    property int totalResults: -1
    property string _lastQuery: ''

    signal highlightRequested(int rowIndex)

    function search(query: string): void {
        _lastQuery = query
        const includeCurrentRow = true
        const topDown = true
        _search(includeCurrentRow, topDown)
    }

    function requestNext(): void {
        const includeCurrentRow = false
        const topDown = true
        _search(includeCurrentRow, topDown)
    }

    function requestPrevious(): void {
        const includeCurrentRow = false
        const topDown = false
        _search(includeCurrentRow, topDown)
    }

    function _search(includeCurrentRow: bool, topDown: bool): void {
        const result = root.searchFunc(_lastQuery, includeCurrentRow, topDown)
        const nextIndex = result.nextIndex
        if (nextIndex >= 0) {
            root.highlightRequested(nextIndex)
        }
        root.currentResult = result.currentResult
        root.totalResults = result.totalResults
    }

}
