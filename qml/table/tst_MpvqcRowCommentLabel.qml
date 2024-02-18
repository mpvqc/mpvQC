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
    name: 'MpvqcRowCommentLabel'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcRowCommentLabel {
            id: objectUnderTest

            rowSelected: false
            tableInEditMode: false
            comment: 'comment'
            searchQuery: 'query'
            backgroundColor: 'transparent'
            focus: false

            mpvqcApplication: QtObject {
                property var mpvqcLabelWidthCalculator: QtObject {
                    property int commentTypesLabelWidth: 120
                }
                property var mpvqcTimeFormatUtils: QtObject {
                    function formatTimeToStringLong(time) { return `${time}` }
                }
                property var mpvqcDefaultTextValidatorPyObject: RegularExpressionValidator {
                    regularExpression: /[0-9A-Z]+/
                }
                property var activeFocusItem
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
        control.delayEditingStoppedTimer.interval = 1
        control.openPopup()
        return control
    }

    function test_stopEditing() {
        const control = createControlInEditMode()

        const popup = control.loader.item
        verify(popup)

        const spy = signalSpy.createObject(control, {target: control, signalName: 'editingStopped'})
        popup.close()
        wait(25)

        verify(!control.loader.sourceComponent)
        compare(spy.count, 1)
    }

    function test_edit() {
        const control = createControlInEditMode()

        const popup = control.loader.item
        verify(popup)

        const spy = signalSpy.createObject(control, {target: control, signalName: 'edited'})
        popup.edited('New Comment')
        wait(25)

        verify(control.loader.sourceComponent)
        compare(spy.count, 1)
        compare(spy.signalArguments[0][0], 'New Comment')
    }

    function test_popupUpAndDownPressed() {
        const control = createControlInEditMode()

        const popup = control.loader.item
        verify(popup)

        let spy = signalSpy.createObject(control, {target: control, signalName: 'upPressed'})
        popup.upPressed()
        compare(spy.count, 1)

        spy = signalSpy.createObject(control, {target: control, signalName: 'downPressed'})
        popup.downPressed()
        compare(spy.count, 1)
    }

}
