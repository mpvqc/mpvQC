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
                property var mpvqcTimeFormatUtils: QtObject {
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
        const editingStartedSpy = signalSpy.createObject(control, {target: control, signalName: 'editingStarted'})
        control.rowSelected = true
        control.tableInEditMode = false
        verify(!control.loader.sourceComponent)
        compare(editingStartedSpy.count, 0)
        compare(control.pauseCalled, false)
        compare(control.jumpToCalled, false)
        compare(control.jumpToTime, -1)
        mouseClick(control)
        verify(control.loader.sourceComponent)
        compare(editingStartedSpy.count, 1)
        compare(control.pauseCalled, true)
        compare(control.jumpToCalled, true)
        compare(control.jumpToTime, 10)
        editingStartedSpy.clear()

        // no-row-selection/edit-mode
        const clickedSpy = signalSpy.createObject(control, {target: control, signalName: 'clicked'})
        control.rowSelected = false
        control.tableInEditMode = true
        compare(clickedSpy.count, 0)
        mouseClick(control)
        compare(clickedSpy.count, 1)
        clickedSpy.clear()

        // no-row-selection/no-edit-mode
        control.rowSelected = false
        control.tableInEditMode = false
        compare(clickedSpy.count, 0)
        mouseClick(control)
        compare(clickedSpy.count, 1)
        clickedSpy.clear()
    }

    function createControlInEditMode(): Item {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)
        control.loader.asynchronous = false
        control.openPopup()
        verify(control)
        return control
    }

    function test_stopEdit() {
        const control = createControlInEditMode()

        const popup = control.loader.item
        verify(popup)

        const editingStoppedSpy = signalSpy.createObject(control, {target: control, signalName: 'editingStopped'})
        popup.closed()
        verify(!control.loader.sourceComponent)
        compare(editingStoppedSpy.count, 1)
    }

    function test_edit() {
        const control = createControlInEditMode()

        const popup = control.loader.item
        verify(popup)

        const editedSpy = signalSpy.createObject(control, {target: control, signalName: 'edited'})
        popup.edited(42)
        compare(editedSpy.count, 1)
        compare(editedSpy.signalArguments[0][0], 42)
    }

    function test_abortEdit() {
        const control = createControlInEditMode()

        const popup = control.loader.item
        verify(popup)

        popup.editingAborted()
        compare(control.jumpToCalled, true)
        compare(control.jumpToTime, 10)
    }

    function test_seek() {
        const control = createControlInEditMode()

        const popup = control.loader.item
        verify(popup)

        popup.valueChanged(42)
        compare(control.jumpToCalled, true)
        compare(control.jumpToTime, 42)
    }

}
