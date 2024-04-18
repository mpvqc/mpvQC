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
    name: 'MpvqcMenuMore'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcRowContextMenu {
            visible: true
        }
    }

    function test_editCommentClicked() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const spy = signalSpy.createObject(null, {target: control, signalName: 'editCommentClicked'})
        verify(spy)

        mouseClick(control.editItem)
        compare(spy.count, 1)
    }

    function test_copyCommentClicked() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const spy = signalSpy.createObject(null, {target: control, signalName: 'copyCommentClicked'})
        verify(spy)

        mouseClick(control.copyItem)
        compare(spy.count, 1)
    }

    function test_deleteCommentClicked() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const spy = signalSpy.createObject(null, {target: control, signalName: 'deleteCommentClicked'})
        verify(spy)

        mouseClick(control.deleteItem)
        compare(spy.count, 1)
    }

}
