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


Item {
    id: testHelper

    width: 400
    height: 400

    MpvqcList {
        id: objectUnderTest
        anchors.fill: testHelper

        model: ['Type 0', 'Type 1', 'Type 2', 'Type 3', 'Type 4', 'Type 5']
        itemHeight: 42

        mpvqcApplication: QtObject {
            property var mpvqcTheme: QtObject
            {
                property color control: "purple"
            }
        }
    }

    TestCase {
        name: "MpvqcList"
        when: windowShown

        function cleanup() {
            objectUnderTest.currentIndex = 0
        }

        function test_selection_data() {
            return [
                { tag: 'row-3', index: 3 },
                { tag: 'row-5', index: 5 },
            ]
        }

        function test_selection(data) {
            ensureRenderedUntilItem(data.index + 1)
            compare(objectUnderTest.currentIndex, 0)

            const item = objectUnderTest.itemAtIndex(data.index)
            mouseClick(item)

            compare(objectUnderTest.currentIndex, data.index)
        }

        function ensureRenderedUntilItem(index: int): void {
            objectUnderTest.currentIndex = index
            objectUnderTest.currentIndex = 0
        }

    }

}
