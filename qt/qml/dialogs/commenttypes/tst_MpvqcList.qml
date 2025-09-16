// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

import "../../themes"

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
