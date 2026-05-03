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

        prefWidth: testHelper.width
        valueFrom: 15
        value: 30
        valueTo: 45

        property int newValue: -1

        onValueModified: value => {
            objectUnderTest.newValue = value;
        }

        TestCase {
            name: "MpvqcSpinBoxRow"
            when: windowShown

            SignalSpy {
                id: valueModifiedSpy
                target: objectUnderTest
                signalName: "valueModified"
            }

            function init() {
                valueModifiedSpy.clear();
                objectUnderTest.newValue = -1;
            }

            function test_spinBox_data() {
                return [
                    {
                        tag: "increase",
                        value: 31,
                        exec: () => {
                            // Workaround for QTBUG-145174: SpinBox.increase() is not a function in Qt 6.11
                            const spinBox = objectUnderTest.spinBox;
                            spinBox.value = Math.min(spinBox.to, spinBox.value + spinBox.stepSize);
                        }
                    },
                ];
            }

            function test_spinBox(data) {
                data.exec();
                compare(objectUnderTest.newValue, data.value);
                compare(valueModifiedSpy.count, 1);
            }
        }
    }
}
