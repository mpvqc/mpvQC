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

import "../../app"

TestCase {
    id: testCase

    width: 600
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcList"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcList {
            anchors.fill: parent

            model: ["Type 0", "Type 1", "Type 2", "Type 3", "Type 4", "Type 5"]
            itemHeight: 42

            mpvqcApplication: QtObject {
                property var mpvqcTheme: MpvqcTheme {
                    themeColorOption: 4
                    themeIdentifier: "Material You"
                }
            }
        }
    }

    function test_selection_data() {
        return [
            {
                tag: "row-3",
                index: 3
            },
            {
                tag: "row-5",
                index: 5
            },
        ];
    }

    function test_selection(data) {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        compare(control.currentIndex, 0);

        const item = control.itemAtIndex(data.index);
        mouseClick(item);

        compare(control.currentIndex, data.index);
    }
}
