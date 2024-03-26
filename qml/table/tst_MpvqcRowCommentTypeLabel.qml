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
                    property var commentTypes: ListModel {
                        ListElement {type: '1'}
                        ListElement {type: '2'}
                        ListElement {type: '3'}
                        ListElement {type: '4'}
                        ListElement {type: '5'}
                        ListElement {type: '6'}
                        ListElement {type: '7'}

                        function items(): list<string> {
                            const marshalled = []
                            for (let i = 0; i < count; i++) {
                                marshalled.push(this.get(i)?.type)
                            }
                            return marshalled
                        }
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
        compare(spy.count, 0)
        mouseClick(control)
        compare(spy.count, 1)
        spy.clear()
    }

    function createControlInEditMode(): Item {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)
        verify(!control.menu)
        control.openMenu()
        verify(control.menu)
        return control
    }

    function test_stopEdit() {
        const control = createControlInEditMode()

        mouseClick(control)
        const editingStoppedSpy = signalSpy.createObject(control, {target: control, signalName: 'editingStopped'})

        control.menu.closed()
        compare(editingStoppedSpy.count, 1)
    }

    function test_edit() {
        const control = createControlInEditMode()

        const editedSpy = signalSpy.createObject(control, {target: control, signalName: 'edited'})

        control.menu.itemClicked('newCommentType')

        compare(editedSpy.count, 1)
        compare(editedSpy.signalArguments[0][0], 'newCommentType')
    }

}
