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

import models


TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: 'MpvqcNewCommentMenu'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcNewCommentMenu {
            id: objectUnderTest

            property bool disableFullScreenCalled: false
            property bool pauseCalled: false
            property bool popupCalled: false

            property bool addNewCommentCalled: false
            property string addNewCommentCommentType: ''

            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject {
                    property var commentTypes: ['1', '2', '3']
                }
                property var mpvqcMpvPlayerPyObject: QtObject {
                    function pause() { pauseCalled = true }
                }
                property var mpvqcCommentTable: QtObject {
                    function addNewComment(commentType) {
                        addNewCommentCalled = true
                        addNewCommentCommentType = commentType
                    }
                }
                property var mpvqcMouseCursorPyObject: QtObject {
                    property point cursor_pos: Qt.point(0, 0)
                }
                function disableFullScreen() { disableFullScreenCalled = true }
            }

            function popup() { popupCalled = true }
        }
    }

    function test_popup() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        verify(!control.pauseCalled)
        verify(!control.popupCalled)

        control.popupMenu()

        verify(control.pauseCalled)
        verify(control.popupCalled)
    }

    function test_click() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        verify(!control.disableFullScreenCalled)
        verify(!control.addNewCommentCalled)

        const item = control.repeater.itemAt(0)
        item.triggered()
        control.closed()

        verify(control.disableFullScreenCalled)
        verify(control.addNewCommentCalled)

        const actual = control.addNewCommentCommentType
        const expected = control.mpvqcApplication.mpvqcSettings.commentTypes[0]
        compare(actual, expected)
    }

}
