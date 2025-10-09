// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

Item {
    id: testHelper

    width: 400
    height: 400

    MpvqcSwitchRow {
        id: objectUnderTest

        property bool newChecked: false

        prefWidth: testHelper.width

        onCheckedChanged: {
            objectUnderTest.newChecked = checked;
        }

        TestCase {
            name: "MpvqcSwitchRow"
            when: windowShown

            SignalSpy {
                id: toggledSpy
                target: objectUnderTest
                signalName: "toggled"
            }

            function init() {
                objectUnderTest.newChecked = false;
                toggledSpy.clear();
            }

            function test_toggle() {
                verify(!objectUnderTest.checked);

                mouseClick(objectUnderTest.toggle);
                compare(toggledSpy.count, 1);
                verify(objectUnderTest.checked);

                mouseClick(objectUnderTest.toggle);
                compare(toggledSpy.count, 2);
                verify(!objectUnderTest.checked);
            }
        }
    }
}
