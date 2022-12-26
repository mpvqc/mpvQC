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


Item {
    id: testHelper

    width: 400
    height: 400

    property bool disableFullScreenCalled: false
    property bool pauseCalled: false
    property bool popupCalled: false

    property bool addNewCommentCalled: false
    property string addNewCommentCommentType: ''

    MpvqcNewCommentMenu {
        id: objectUnderTest

        mpvqcApplication: QtObject {
            property var mpvqcSettings: QtObject {
                property MpvqcCommentTypesModel commentTypes: MpvqcCommentTypesModel {}
            }
            property var mpvqcMpvPlayerPyObject: QtObject {
                function pause() { pauseCalled = true }
            }
            property var mpvqcCommentTable: QtObject {
                function addNewComment(commentType) { addNewCommentCalled = true; addNewCommentCommentType = commentType }
            }
            function disableFullScreen() { testHelper.disableFullScreenCalled = true }
        }

        function popup() { popupCalled = true }
    }

    TestCase {
        name: "MpvqcNewCommentMenu"
        when: windowShown

        function init() {
            testHelper.disableFullScreenCalled = false
            testHelper.pauseCalled = false
            testHelper.popupCalled = false
            testHelper.addNewCommentCalled = false
            testHelper.addNewCommentCommentType = ''
        }

        function test_popupMenu() {
            objectUnderTest.popupMenu()
            verify(disableFullScreenCalled)
            verify(pauseCalled)
            verify(popupCalled)
        }

        function test_click() {
            const item = objectUnderTest.repeater.itemAt(0)
            item.triggered()
            verify(testHelper.addNewCommentCalled)

            const actual = testHelper.addNewCommentCommentType
            const expected = objectUnderTest.mpvqcApplication.mpvqcSettings.commentTypes.get(0).type
            compare(actual, expected)
        }

    }

}
