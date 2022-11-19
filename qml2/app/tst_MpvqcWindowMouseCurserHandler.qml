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
import QtTest


MpvqcWindowMouseCurserHandler {
    id: objectUnderTest
    width: 400
    height: 400

    borderWidth: 25

    TestCase {
        name: "MpvqcWindowMouseCurserHandler"
        when: windowShown

        function test_cursorShape_data() {
            return [
                { x: 200, y: 200, expected: Qt.ArrowCursor, tag: 'center' },
                { x: 0, y: 0,  expected: Qt.SizeFDiagCursor, tag: 'top-left' },
                { x: 399, y: 399,  expected: Qt.SizeFDiagCursor, tag: 'bottom-right' },
                { x: 399, y: 0, expected: Qt.SizeBDiagCursor, tag: 'top-right' },
                { x: 0, y: 399, expected: Qt.SizeBDiagCursor, tag: 'bottom-left' },
            ]
        }

        function test_cursorShape(data) {
            mouseMove(objectUnderTest, data.x, data.y)
            compare(objectUnderTest.cursorShape, data.expected)
        }
    }

 }
