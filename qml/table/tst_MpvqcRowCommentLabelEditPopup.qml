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
    name: 'MpvqcRowCommentLabelEditPopup'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcRowCommentLabelEditPopup {
            mpvqcSpecialCharacterValidator: RegularExpressionValidator {
                regularExpression: /[0-9A-Z]+/
            }
            currentComment: 'Corrent comment'
            backgroundColor: 'transparent'
        }
    }

    Component {
        id: otherItem

        Label {}
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
        verify(closedSpy.count > 0)
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
        verify(closedSpy.count > 0)
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
        verify(closedSpy.count > 0)
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
        verify(closedSpy.count > 0)
    }

    function test_clickedOutsideApplication() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const controlOther = createTemporaryObject(otherItem, testCase)
        verify(controlOther)

        let spy = signalSpy.createObject(control, {target: control, signalName: 'closed'})
        verify(spy)

        controlOther.forceActiveFocus()
        compare(spy.count, 1)
    }

}
