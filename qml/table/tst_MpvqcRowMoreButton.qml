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
    name: 'MpvqcRowMoreButton'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcRowMoreButton {
            tableInEditMode: false
        }
    }

    function test_click() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.tableInEditMode = true
        verify(!control.focus)
        mouseClick(control)
        verify(control.focus)

        control.tableInEditMode = false
        verify(!control.menu)
        mouseClick(control)
        verify(control.menu)

    }

    function test_signals() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const copyCommentClickedSpy = signalSpy.createObject(null, {target: control, signalName: 'copyCommentClicked'})
        verify(copyCommentClickedSpy)

        const deleteCommentClickedSpy = signalSpy.createObject(null, {target: control, signalName: 'deleteCommentClicked'})
        verify(deleteCommentClickedSpy)

        const editCommentClickedSpy = signalSpy.createObject(null, {target: control, signalName: 'editCommentClicked'})
        verify(deleteCommentClickedSpy)

        control.openMenu()
        verify(control.menu)

        control.menu.copyCommentClicked()
        compare(copyCommentClickedSpy.count, 1)

        control.menu.deleteCommentClicked()
        compare(deleteCommentClickedSpy.count, 1)

        control.menu.editCommentClicked()
        compare(editCommentClickedSpy.count, 1)
    }

}
