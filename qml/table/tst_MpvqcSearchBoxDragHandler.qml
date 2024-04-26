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

import models


TestCase {
    id: testCase

    property int topBottomMargin: 50

    width: 500
    height: 500
    visible: true
    when: windowShown
    name: 'MpvqcSearchBoxDragHandler'

    Component {
        id: objectUnderTest

        Rectangle {
            id: _commentTable
            color: 'lightblue'
            width: 500
            height: 500

            property alias commentTable: _commentTable
            property alias searchBox: _searchBox

            Rectangle {
                id: _searchBox
                color: 'darkblue'
                x: parent.width - width - testCase.topBottomMargin
                y: testCase.topBottomMargin
                width: 200
                height: 40

                MpvqcSearchBoxDragHandler {
                    commentTable: _commentTable
                    searchBox: _searchBox
                    topBottomMargin: testCase.topBottomMargin
                    handleTransition: { /* Disable animation */ }
                }
            }
        }
    }

    function create(): QtObject {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)
        verify(control.commentTable)
        verify(control.searchBox)
        return control
    }

    function test_canDrag() {
        const control = create()

        const yBefore = control.searchBox.y
        mouseDrag(control.searchBox, 0, 0, 0, 50)
        const yAfter = control.searchBox.y
        verify(yBefore < yAfter)
    }

    function test_canNotDragAboveMarginTop() {
        const control = create()

        const yBefore = control.searchBox.y
        mouseDrag(control.searchBox, 0, 0, 0, -500)
        const yAfter = control.searchBox.y
        compare(yBefore, yAfter)
    }

    function test_canNotDragBelowMarginBottom() {
        const control = create()

        const yMax = testCase.height + control.searchBox.height
        mouseDrag(control.searchBox, 0, 0, 0, yMax)
        const yAfter = control.searchBox.y + control.searchBox.height + testCase.topBottomMargin
        compare(testCase.height, yAfter)

        const control2 = create()
        const yMax2 = testCase.height + control2.searchBox.height + 2
        mouseDrag(control2.searchBox, 0, 0, 0, yMax2)
        const yAfter2 = control2.searchBox.y + control2.searchBox.height + testCase.topBottomMargin
        verify(yAfter2 <= testCase.height)
    }

    function test_shrinksWithContainer() {
        const control = create()

        const yMax = testCase.height + control.searchBox.height
        mouseDrag(control.searchBox, 0, 0, 0, yMax)

        const yResize = 250
        const yBefore = control.searchBox.y

        control.commentTable.height -= yResize

        const yAfter = control.searchBox.y
        compare(yAfter + yResize, yBefore)
    }

}
