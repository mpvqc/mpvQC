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

    property int shortTime: 100
    property int longTime: 300

    property int columnPlayButton: 5
    property int columnTime: 50
    property int columnCommentType: 150
    property int columnComment: 400
    property int columnMenuMore: 490

    property int row1: 40 / 2
    property int row2: 40 / 2 + 40
    property int row3: 40 / 2 + 40 * 2
    property int row4: 40 / 2 + 40 * 3

    width: 500
    height: 400
    visible: true
    when: windowShown
    name: 'MpvqcTable'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcTable {
            id: this

            width: testCase.width
            height: testCase.height

            property string clipboardText: ''

            mpvqcApplication: QtObject {
                property bool fullscreen: false
                property var activeFocusItem
                property var mpvqcSettings: QtObject {
                    property var commentTypes: ['0', '1', '2', '3']
                }
                property var mpvqcMpvPlayerPyObject: QtObject {
                    function pause() {}
                    function jump_to(time) {}
                }
                property var mpvqcMpvPlayerPropertiesPyObject: QtObject {
                    property int duration: 60
                }
                property var mpvqcUtilityPyObject: QtObject {
                    function copyToClipboard(text) { clipboardText = text }
                    function formatTimeToStringLong(time) { return `${time}` }
                    function formatTimeToStringShort(time) { return `${time}` }
                }
                property var mpvqcCommentTable: this
                property var mpvqcLabelWidthCalculator: QtObject {
                    property int commentTypesLabelWidth: 150
                    property int timeLabelWidth: 30
                }
                property var mpvqcDefaultTextValidatorPyObject: RegularExpressionValidator {
                    regularExpression: /[0-9A-Z]+/

                    function replace_special_characters(s) { return s }
                }
            }

            searchQuery: 'search Query'

            model: ListModel {
                signal newItemAdded()
                signal timeUpdated()
                signal highlightRequested()
                signal commentsChanged()

                function update_time(index, time) {}
                function update_comment_type(index, comment_type) {}
                function update_comment(index, comment) {}

                function remove_row(index) { remove(index, 1) }

                ListElement {
                    time: 10
                    commentType: 'Comment Type 1'
                    comment: 'Comment 1'
                }
                ListElement {
                    time: 20
                    commentType: 'Comment Type 2'
                    comment: 'Comment 2'
                }
            }
        }
    }

    function test_selectionWhileNotEditing_data() {
        return [
            {tag: 'on-other-row-play-button-clicked', column: columnPlayButton},
            {tag: 'on-other-row-time-label-clicked', column: columnTime},
            {tag: 'on-other-row-comment-type-label-clicked', column: columnCommentType},
            {tag: 'on-other-row-comment-label-clicked', column: columnComment},
        ]
    }

    function test_selectionWhileNotEditing(data) {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)
        waitForRendering(control, shortTime)

        mouseClick(control, data.column, row2)
        wait(longTime)
        verify(!control.currentlyEditing)
        compare(control.currentIndex, 1)
    }

    function test_selectionWhileEditingComment_data() {
        return [
            {
                tag: 'on-same-row-play-button-clicked',
                columnClicked: columnPlayButton, rowClicked: row1, rowIndexExpected: 0
            },
            {
                tag: 'on-same-row-time-label-clicked',
                columnClicked: columnTime, rowClicked: row1, rowIndexExpected: 0
            },
            {
                tag: 'on-same-row-comment-type-label-clicked',
                columnClicked: columnCommentType, rowClicked: row1, rowIndexExpected: 0
            },
            {
                tag: 'on-other-row-play-button-clicked',
                columnClicked: columnPlayButton, rowClicked: row2, rowIndexExpected: 1
            },
            {
                tag: 'on-other-row-time-label-clicked',
                columnClicked: columnTime, rowClicked: row2, rowIndexExpected: 1
            },
            {
                tag: 'on-other-row-comment-type-label-clicked',
                columnClicked: columnCommentType, rowClicked: row2, rowIndexExpected: 1
            },
            {
                tag: 'on-other-row-comment-label-clicked',
                columnClicked: columnComment, rowClicked: row2, rowIndexExpected: 1
            },
        ]
    }

    function test_selectionWhileEditingComment(data) {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)
        waitForRendering(control, shortTime)
        keyPress(Qt.Key_Return)
        waitForRendering(control, shortTime)
        verify(control.currentlyEditing)

        mouseClick(control, data.columnClicked, data.rowClicked)
        wait(longTime)
        verify(!control.currentlyEditing)
        compare(control.currentIndex, data.rowIndexExpected)
    }

    function test_selectionWhileEditingTimeOnPressedOutside() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)
        waitForRendering(control, shortTime)
        mouseClick(control, columnTime, row1)
        waitForRendering(control, shortTime)
        verify(control.currentlyEditing)

        mouseClick(control, columnComment, row2)
        wait(longTime)
        verify(!control.currentlyEditing)
        compare(control.currentIndex, 0)
    }

    function test_selectionWhileEditingCommentTypeOnPressedOutside() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)
        waitForRendering(control, shortTime)
        mouseClick(control, columnCommentType, row1)
        waitForRendering(control, shortTime)
        verify(control.currentlyEditing)

        mouseClick(control, columnComment, row2)
        wait(longTime)
        verify(!control.currentlyEditing)
        compare(control.currentIndex, 0)
    }

    function test_editComment_data() {
        return [
            {
                tag: 'via-context-menu', exec: (control) => {
                    mouseClick(control, columnMenuMore / 2, row1, Qt.RightButton)
                    waitForRendering(control, shortTime)
                    mouseClick(control, columnMenuMore / 2, row2)
                }
            },
            {
                tag: 'via-shortcut-return', exec: (control) => keyPress(Qt.Key_Return)
            },
        ]
    }

    function test_editComment(data) {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)
        waitForRendering(control, shortTime)

        verify(!control.currentlyEditing)
        data.exec(control)
        verify(control.currentlyEditing)
    }

    function test_copyToClipboard_data() {
        return [
            {
                tag: 'via-context-menu', exec: (control) => {
                    mouseClick(control, columnMenuMore / 2, row1, Qt.RightButton)
                    waitForRendering(control, shortTime)
                    mouseClick(control, columnMenuMore / 2, row3)
                }
            },
            {
                tag: 'via-shortcut', exec: (control) => {
                    keyPress(Qt.Key_C, Qt.ControlModifier)
                }
            },
        ]
    }

    function test_copyToClipboard(data) {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)
        waitForRendering(control, shortTime)

        data.exec(control)
        waitForRendering(control, shortTime)

        compare(control.clipboardText, '[10] [Comment Type 1] Comment 1')
    }

    function test_deleteComment_data() {
        return [
            {
                tag: 'via-context-menu', exec: (control) => {
                    mouseClick(control, columnMenuMore / 2, row1, Qt.RightButton)
                    waitForRendering(control, shortTime)
                    mouseClick(control, columnMenuMore / 2, row4)
                }
            },
            {tag: 'via-shortcut-backspace', exec: (control) => keyPress(Qt.Key_Backspace)},
            {tag: 'via-shortcut-delete', exec: (control) => keyPress(Qt.Key_Delete)},
        ]
    }

    function test_deleteComment(data) {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)
        waitForRendering(control, shortTime)

        data.exec(control)
        waitForRendering(control, shortTime)
        verify(control.deleteCommentMessageBox)

        control.deleteCommentMessageBox.accepted()

        compare(control.count, 1)
    }

}
