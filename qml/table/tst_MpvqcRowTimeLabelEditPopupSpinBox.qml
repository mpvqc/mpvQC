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

TestCase {
    id: testCase

    width: 180
    height: 60
    visible: true
    when: windowShown
    name: "MpvqcRowTimeLabelEditPopupSpinBox"

    Component {
        id: signalSpy
        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcRowTimeLabelEditPopupSpinBox {
            width: 180
            height: 60

            value: 10

            mpvqcApplication: QtObject {
                property var mpvqcMpvPlayerPropertiesPyObject: QtObject {
                    property int duration: 0
                }
                property var mpvqcUtilityPyObject: QtObject {
                    function formatTimeToStringShort(time) {
                        return `${time}`;
                    }
                    function formatTimeToStringLong(time) {
                        return `${time}`;
                    }
                }
            }
        }
    }

    function test_upperLimit() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.duration = 0;
        compare(control.to, 24 * 60 * 60 - 1);

        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.duration = 42;
        compare(control.to, 42);
    }

    function test_scroll() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const x = control.contentItem.width / 2;
        const y = control.contentItem.height / 2;
        const deltaX = 0;

        control.value = 10;
        mouseWheel(control.contentItem, x, y, deltaX, 1);
        compare(control.value, 11);

        control.value = 10;
        mouseWheel(control.contentItem, x, y, deltaX, -1);
        compare(control.value, 9);
    }

    function test_click() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.value = 10;
        mouseClick(control.up.indicator);
        compare(control.value, 11);

        control.value = 10;
        mouseClick(control.down.indicator);
        compare(control.value, 9);
    }

    function test_changeProgrammatically() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "valueModified"
        });
        verify(spy);

        spy.clear();
        control.value = 10;
        control.incrementValue();
        compare(control.value, 11);
        compare(spy.count, 1);

        spy.clear();
        control.value = 10;
        control.decrementValue();
        compare(control.value, 9);
        compare(spy.count, 1);
    }
}
