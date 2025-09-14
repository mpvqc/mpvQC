// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtTest

MpvqcListControls {
    id: objectUnderTest

    width: 400
    height: 400

    TestCase {
        name: "MpvqcListControls"
        when: windowShown

        SignalSpy {
            id: upClickedSpy
            target: objectUnderTest
            signalName: "upClicked"
        }
        SignalSpy {
            id: downClickedSpy
            target: objectUnderTest
            signalName: "downClicked"
        }
        SignalSpy {
            id: editClickedSpy
            target: objectUnderTest
            signalName: "editClicked"
        }
        SignalSpy {
            id: deleteClickedSpy
            target: objectUnderTest
            signalName: "deleteClicked"
        }

        function cleanup() {
            upClickedSpy.clear();
            downClickedSpy.clear();
            editClickedSpy.clear();
            deleteClickedSpy.clear();
        }

        function test_click_data() {
            return [
                {
                    tag: "upButton",
                    item: objectUnderTest.upButton,
                    spy: upClickedSpy
                },
                {
                    tag: "downButton",
                    item: objectUnderTest.downButton,
                    spy: downClickedSpy
                },
                {
                    tag: "editButton",
                    item: objectUnderTest.editButton,
                    spy: editClickedSpy
                },
                {
                    tag: "deleteButton",
                    item: objectUnderTest.deleteButton,
                    spy: deleteClickedSpy
                },
            ];
        }

        function test_click(data) {
            mouseClick(data.item);
            compare(data.spy.count, 1);
        }
    }
}
