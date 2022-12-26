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
import QtQuick.Controls
import QtTest


TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: 'MpvqcRowCommentTypeLabel'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcRowCommentTypeLabel {

            commentType: 'comment type'
            rowSelected: false
            tableInEditMode: false
            focus: false

            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject {
                    property var commentTypes: QtObject {
                        function items() { return ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'] }
                    }
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
        let spy = signalSpy.createObject(control, {target: control, signalName: 'editingStarted'})
        verify(spy)
        control.rowSelected = true
        control.tableInEditMode = false
        verify(!control.loader.sourceComponent)
        compare(spy.count, 0)
        mouseClick(control)
        verify(control.loader.sourceComponent)
        compare(spy.count, 1)
        spy.clear()

        // no-row-selection/edit-mode
        spy = signalSpy.createObject(control, {target: control, signalName: 'clicked'})
        verify(spy)
        control.rowSelected = false
        control.tableInEditMode = true
        compare(spy.count, 0)
        mouseClick(control)
        compare(spy.count, 1)
        spy.clear()

        // no-row-selection/no-edit-mode
        control.rowSelected = false
        control.tableInEditMode = false
        compare(spy.count, 0)
        mouseClick(control)
        compare(spy.count, 1)
        spy.clear()
    }

    function createControlInEditMode(): Item {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)
        control.loader.asynchronous = false
        control.openMenu()
        verify(control)
        return control
    }

    function test_stopEdit() {
        const control = createControlInEditMode()

        const menu = control.loader.item
        verify(menu)

        const editingStoppedSpy = signalSpy.createObject(control, {target: control, signalName: 'editingStopped'})
        menu.closed()
        verify(!control.loader.sourceComponent)
        compare(editingStoppedSpy.count, 1)
    }

    function test_edit() {
        const control = createControlInEditMode()

        const menu = control.loader.item
        verify(menu)

        const editedSpy = signalSpy.createObject(control, {target: control, signalName: 'edited'})
        menu.itemClicked('newCommentType')
        compare(editedSpy.count, 1)
        compare(editedSpy.signalArguments[0][0], 'newCommentType')
    }

}
