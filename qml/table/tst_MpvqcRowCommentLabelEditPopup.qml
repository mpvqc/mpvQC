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
    name: 'MpvqcRowCommentLabelEditPopup'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcRowCommentLabelEditPopup {
            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject {
                    property var commentTypes: QtObject {
                        function items() { return ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'] }
                    }
                }
                property var mpvqcSpecialCharacterValidatorPyObject: RegularExpressionValidator {
                    regularExpression: /[0-9A-Z]+/
                }
                property var activeFocusItem: undefined
            }
            paddingAround: 4
            currentComment: 'Corrent comment'

        }
    }

    function test_alwaysFocused() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.contentItem.focus = false
        verify(control.contentItem.focus)
    }

    function test_textFieldAccepted() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        let editedSpy = signalSpy.createObject(control, {target: control, signalName: 'edited'})
        verify(editedSpy)

        let closedSpy = signalSpy.createObject(control, {target: control, signalName: 'closed'})
        verify(closedSpy)

        control.contentItem.accepted()

        compare(editedSpy.count, 1)
        compare(closedSpy.count, 1)
    }

    function test_arrowUpPressed() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        let editedSpy = signalSpy.createObject(control, {target: control, signalName: 'edited'})
        verify(editedSpy)

        let closedSpy = signalSpy.createObject(control, {target: control, signalName: 'closed'})
        verify(closedSpy)

        let upSpy = signalSpy.createObject(control, {target: control, signalName: 'upPressed'})
        verify(upSpy)

        keyPress(Qt.Key_Up)

        compare(editedSpy.count, 1)
        compare(closedSpy.count, 1)
        compare(upSpy.count, 1)
    }

    function test_arrowDownPressed() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        let editedSpy = signalSpy.createObject(control, {target: control, signalName: 'edited'})
        verify(editedSpy)

        let closedSpy = signalSpy.createObject(control, {target: control, signalName: 'closed'})
        verify(closedSpy)

        let downSpy = signalSpy.createObject(control, {target: control, signalName: 'downPressed'})
        verify(downSpy)

        keyPress(Qt.Key_Down)

        compare(editedSpy.count, 1)
        compare(closedSpy.count, 1)
        compare(downSpy.count, 1)
    }

    function test_escapePressed() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        let editedSpy = signalSpy.createObject(control, {target: control, signalName: 'edited'})
        verify(editedSpy)

        let closedSpy = signalSpy.createObject(control, {target: control, signalName: 'closed'})
        verify(closedSpy)

        keyPress(Qt.Key_Escape)

        compare(editedSpy.count, 0)
        compare(closedSpy.count, 1)
    }

    function test_clickedOutsideApplication() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        let spy = signalSpy.createObject(control, {target: control, signalName: 'closed'})
        verify(spy)

        control.mpvqcApplication.activeFocusItem = null
        compare(spy.count, 1)
    }

}
