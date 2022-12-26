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
    name: 'MpvqcRowTimeLabelEditPopup'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcRowTimeLabelEditPopup {
            id: objectUnderTest

            width: parent.width
            height: parent.height

            time: 10
            acceptValue: true

            mpvqcApplication: QtObject {
                property var mpvqcMpvPlayerPropertiesPyObject: QtObject {
                    property int duration: 0
                }
                property var mpvqcTimeFormatUtils: QtObject {
                    function formatTimeToString(time) { return `${time}` }
                }
            }
        }
    }

    function test_valueChanged_data() {
        return [
            { tag: 'accepting', accept: true },
            { tag: 'rejecting', accept: false },
        ]
    }

    function test_valueChanged(data) {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const valueChangedSpy = signalSpy.createObject(control, {target: control, signalName: 'valueChanged'})
        verify(valueChangedSpy)

        control.acceptValue = data.accept
        control.spinBox.incrementValue()

        compare(valueChangedSpy.count, data.accept ? 1 : 0)
    }


    function test_close_data() {
        return [
            { tag: 'accepting', accept: true },
            { tag: 'rejecting', accept: false },
        ]
    }

    function test_close(data) {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const editingAbortedSpy = signalSpy.createObject(control, {target: control, signalName: 'editingAborted'})
        verify(editingAbortedSpy)

        const editedSpy = signalSpy.createObject(control, {target: control, signalName: 'edited'})
        verify(editedSpy)

        control.acceptValue = data.accept
        control.close()

        compare(editedSpy.count, data.accept ? 1 : 0)
        compare(editingAbortedSpy.count, data.accept ? 0 : 1)

        verify(!control.visible)
    }

    function test_pressEscape() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const editingAbortedSpy = signalSpy.createObject(control, {target: control, signalName: 'editingAborted'})
        verify(editingAbortedSpy)

        const editedSpy = signalSpy.createObject(control, {target: control, signalName: 'edited'})
        verify(editedSpy)

        keyPress(Qt.Key_Escape)

        compare(editedSpy.count, 0)
        compare(editingAbortedSpy.count, 1)
        verify(!control.visible)
    }

    function test_pressArrowKeys() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.spinBox.value = 10
        keyPress(Qt.Key_Left)
        compare(control.spinBox.value, 9)

        control.spinBox.value = 10
        keyPress(Qt.Key_Right)
        compare(control.spinBox.value, 11)

        control.spinBox.value = 10
        keyPress(Qt.Key_Up)
        compare(control.spinBox.value, 11)

        control.spinBox.value = 10
        keyPress(Qt.Key_Down)
        compare(control.spinBox.value, 9)
    }

}
