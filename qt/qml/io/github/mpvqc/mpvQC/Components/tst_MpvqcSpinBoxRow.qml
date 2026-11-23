// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

Item {
    id: testHelper

    width: 400
    height: 400

    MpvqcSpinBoxRow {
        id: objectUnderTest

        property int newValue: -1

        prefWidth: testHelper.width
        valueFrom: 15
        value: 30
        valueTo: 45

        onValueModified: value => {
            objectUnderTest.newValue = value;
        }

        TestCase {
            name: "MpvqcSpinBoxRow"
            when: windowShown

            function init() {
                valueModifiedSpy.clear();
                objectUnderTest.newValue = -1;
            }

            function test_spinBox_data() {
                return [
                    {
                        tag: "increase",
                        value: 31,
                        exec: () => objectUnderTest.spinBox.increase()
                    },
                ];
            }

            function test_spinBox(data) {
                data.exec();
                compare(objectUnderTest.newValue, data.value);
                compare(valueModifiedSpy.count, 1);
            }

            SignalSpy {
                id: valueModifiedSpy
                target: objectUnderTest
                signalName: "valueModified"
            }
        }
    }
}
