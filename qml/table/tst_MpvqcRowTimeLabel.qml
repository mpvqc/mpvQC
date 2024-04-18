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

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: 'MpvqcRowTimeLabel'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcRowTimeLabel {
            property bool pauseCalled: false
            property bool jumpToCalled: false
            property int jumpToTime: -1

            time: 10
            rowSelected: false
            tableInEditMode: false
            focus: false

            mpvqcApplication: QtObject {
                property var mpvqcMpvPlayerPropertiesPyObject: QtObject {
                    property int duration: 0
                }
                property var mpvqcMpvPlayerPyObject: QtObject {
                    function pause() { pauseCalled = true }
                    function jump_to(time) { jumpToCalled = true; jumpToTime = time }
                }
                property var mpvqcUtilityPyObject: QtObject {
                    function formatTimeToStringShort(time) { return `${time}` }
                    function formatTimeToStringLong(time) { return `${time}` }
                }
            }
        }
    }

    function test_click() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        // row-selection/edit-mode
        control.rowSelected = true
        control.tableInEditMode = true
        verify(!control.focus)
        mouseClick(control)
        verify(control.focus)

        // row-selection/no-edit-mode
        const spy = signalSpy.createObject(control, {target: control, signalName: 'editingStarted'})
        verify(spy)

        control.rowSelected = true
        control.tableInEditMode = false
        compare(spy.count, 0)
        compare(control.pauseCalled, false)
        compare(control.jumpToCalled, false)
        compare(control.jumpToTime, -1)
        mouseClick(control)
        verify(control.popup)
        compare(spy.count, 1)
        compare(control.pauseCalled, true)
        compare(control.jumpToCalled, true)
        compare(control.jumpToTime, 10)
        spy.clear()
    }

    function createControlInEditMode(): Item {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)
        control.openPopup(0, 0)
        verify(control)
        return control
    }

    function test_stopEdit() {
        const control = createControlInEditMode()
        verify(control.popup)

        const spy = signalSpy.createObject(control, {target: control, signalName: 'editingStopped'})
        verify(spy)

        control.popup.closed()
        compare(spy.count, 1)
    }

    function test_edit() {
        const control = createControlInEditMode()
        verify(control.popup)

        const spy = signalSpy.createObject(control, {target: control, signalName: 'edited'})
        verify(spy)

        control.popup.edited(42)

        compare(spy.count, 1)
        compare(spy.signalArguments[0][0], 42)
    }

    function test_abortEdit() {
        const control = createControlInEditMode()
        verify(control.popup)

        control.popup.editingAborted()

        compare(control.jumpToCalled, true)
        compare(control.jumpToTime, 10)
    }

    function test_seek() {
        const control = createControlInEditMode()
        verify(control.popup)

        control.popup.valueChanged(42)

        compare(control.jumpToCalled, true)
        compare(control.jumpToTime, 42)
    }

}
