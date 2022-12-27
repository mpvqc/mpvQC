/*
mpvQC

Copyright (C) 2022 mpvQC developers

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
import QtQuick.Controls
import QtTest


Item {
    id: testHelper
    width: 400
    height: 400

    property var edges: undefined
    property var mpvqcApplication: ApplicationWindow {
        function startSystemResize(edges) {
            testHelper.edges = edges
        }
    }

    MpvqcWindowResizeHandler {
        id: objectUnderTest

        borderWidth: 25
        mpvqcApplication: testHelper.mpvqcApplication
    }

    TestCase {
        name: "MpvqcWindowResizeHandler"
        when: windowShown

        function cleanup() {
            testHelper.edges = undefined
        }

        function test_resize_data() {
            return [
                { x: 200, y: 0, dx: 0, dy: 10, expected: Qt.TopEdge, tag: 'top' },
                { x: 200, y: 399, dx: 0, dy: 10, expected: Qt.BottomEdge, tag: 'bottom' },
                { x: 0, y: 200, dx: 10, dy: 00, expected: Qt.LeftEdge, tag: 'left' },
                { x: 399, y: 200, dx: 10, dy: 00, expected: Qt.RightEdge, tag: 'right' },
                { x: 0, y: 0, dx: 10, dy: 10, expected: Qt.TopEdge + Qt.LeftEdge, tag: 'top-left' },
                { x: 399, y: 0, dx: 10, dy: 10, expected: Qt.TopEdge + Qt.RightEdge, tag: 'top-right' },
                { x: 399, y: 399, dx: 10, dy: 10, expected: Qt.BottomEdge + Qt.RightEdge, tag: 'bottom-right' },
                { x: 0, y: 399, dx: 10, dy: 10, expected: Qt.BottomEdge + Qt.LeftEdge, tag: 'bottom-left' },
            ]
        }

        function test_resize(data) {
            mouseDrag(testHelper, data.x, data.y, data.dx, data.dy)
            compare(testHelper.edges, data.expected)
        }
    }

}
