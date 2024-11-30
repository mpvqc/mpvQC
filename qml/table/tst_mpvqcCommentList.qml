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

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    QtObject {
        id: _clickHelper

        readonly property int rowHeight: 44
        readonly property int row1Center: rowHeight / 2
        readonly property int row2Center: row1Center + rowHeight * 1
        readonly property int row3Center: row1Center + rowHeight * 2
        readonly property int row4Center: row1Center + rowHeight * 3

        readonly property int columnPlayButton: 5
        readonly property int columnTime: columnPlayButton + 50
        readonly property int columnCommentType: columnTime + 100
        readonly property int columnComment: testCase.width - 100

        function onContextMenuOpen(tableRow: int): point {
            const xCoordinate = testCase.width - 200;
            const yCoordinate = row1Center + rowHeight * tableRow;
            return Qt.point(xCoordinate, yCoordinate);
        }

        function onContextMenuItem(index: int, tableRow: int): point {
            const contextMenuItemHeight = 34;

            const xCoordinate = testCase.width - 200 + 10;
            const yTableRow = (rowHeight / 2) + rowHeight * tableRow;
            const yContextMenuItem = yTableRow + contextMenuItemHeight * index;
            return Qt.point(xCoordinate, yContextMenuItem);
        }
    }

    readonly property int timeoutShort: 100
    readonly property int timeoutLong: 300

    width: 600
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcCommentList"

    Component {
        id: objectUnderTest

        MpvqcCommentList {
            id: __objectUnderTest

            height: testCase.height
            width: testCase.width

            property list<int> calledJumpToTimeArgs: []
            property int calledPauseVideoCounter: 0

            timeLabelWidth: 50
            commentTypeLabelWidth: 100

            backgroundColor: "#fff0ee"
            rowHighlightColor: "#904a42"
            rowHighlightTextColor: "#ffffff"
            rowBaseColor: backgroundColor
            rowBaseTextColor: "#534341"
            rowAlternateBaseColor: backgroundColor
            rowAlternateBaseTextColor: rowBaseTextColor

            timeFormatFunc: time => `00:00:0${time}`
            sanitizeTextFunc: text => text
            jumpToTimeFunc: time => calledJumpToTimeArgs.push(time)
            pauseVideoFunc: () => calledPauseVideoCounter++

            defaultTextValidator: RegularExpressionValidator {
                regularExpression: /.*/
            }
            messageBoxParent: testCase
            commentTypes: ["Comment Type 1", "Comment Type 2", "Comment Type 3", "Comment Type 4"]

            videoDuration: 10
            isCurrentlyFullScreen: false

            model: ListModel {
                property bool calledCopyToClipboard: false
                property bool calledRemoveRow: false

                property int selectedRow: -1

                function copy_to_clipboard(index: int): void {
                    calledCopyToClipboard = true;
                }

                function remove_row(index: int): void {
                    calledRemoveRow = true;
                }

                ListElement {
                    time: 1
                    commentType: "Comment Type 1"
                    comment: "Comment 1"
                }
                ListElement {
                    time: 2
                    commentType: "Comment Type 2"
                    comment: "Comment 2"
                }
                ListElement {
                    time: 3
                    commentType: "Comment Type 3"
                    comment: "Comment 3"
                }
                ListElement {
                    time: 4
                    commentType: "Comment Type 4"
                    comment: "Comment 4"
                }
            }
        }
    }

    function test_selectionWhileNotEditing_data(): list<var> {
        return [
            {
                tag: "on-other-row-play-button-clicked",
                column: _clickHelper.columnPlayButton
            },
            {
                tag: "on-other-row-time-label-clicked",
                column: _clickHelper.columnTime
            },
            {
                tag: "on-other-row-comment-type-label-clicked",
                column: _clickHelper.columnCommentType
            },
            {
                tag: "on-other-row-comment-label-clicked",
                column: _clickHelper.columnComment
            },
        ];
    }

    function test_selectionWhileNotEditing(data): void {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        waitForRendering(control, timeoutShort);

        mouseClick(control, data.column, _clickHelper.row2Center);
        tryVerify(() => control.isNotCurrentlyEditing, timeoutLong);

        compare(control.currentIndex, 1);
    }

    function test_selectionWhileEditingComment_data() {
        return [
            {
                tag: "on-same-row-play-button-clicked",
                columnClicked: _clickHelper.columnPlayButton,
                rowClicked: _clickHelper.row1Center,
                rowIndexExpected: 0
            },
            {
                tag: "on-same-row-time-label-clicked",
                columnClicked: _clickHelper.columnTime,
                rowClicked: _clickHelper.row1Center,
                rowIndexExpected: 0
            },
            {
                tag: "on-same-row-comment-type-label-clicked",
                columnClicked: _clickHelper.columnCommentType,
                rowClicked: _clickHelper.row1Center,
                rowIndexExpected: 0
            },
            {
                tag: "on-other-row-play-button-clicked",
                columnClicked: _clickHelper.columnPlayButton,
                rowClicked: _clickHelper.row2Center,
                rowIndexExpected: 1
            },
            {
                tag: "on-other-row-time-label-clicked",
                columnClicked: _clickHelper.columnTime,
                rowClicked: _clickHelper.row2Center,
                rowIndexExpected: 1
            },
            {
                tag: "on-other-row-comment-type-label-clicked",
                columnClicked: _clickHelper.columnCommentType,
                rowClicked: _clickHelper.row2Center,
                rowIndexExpected: 1
            },
            {
                tag: "on-other-row-comment-label-clicked",
                columnClicked: _clickHelper.columnComment,
                rowClicked: _clickHelper.row2Center,
                rowIndexExpected: 1
            },
        ];
    }

    function test_selectionWhileEditingComment(data) {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        waitForRendering(control, timeoutShort);

        keyPress(Qt.Key_Return);
        waitForRendering(control, timeoutShort);
        verify(control.isCurrentlyEditing);

        mouseClick(control, data.columnClicked, data.rowClicked);
        tryVerify(() => control.isNotCurrentlyEditing, timeoutLong);
        compare(control.currentIndex, data.rowIndexExpected);
    }

    function test_selectionWhileEditingTime() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        waitForRendering(control, timeoutShort);

        mouseClick(control, _clickHelper.columnTime, _clickHelper.row1Center);
        wait(timeoutShort);
        verify(control.isCurrentlyEditing);

        mouseClick(control, _clickHelper.columnComment, _clickHelper.row2Center);
        tryVerify(() => control.isNotCurrentlyEditing, timeoutLong);
        compare(control.currentIndex, 0);
    }

    function test_selectionWhileEditingCommentType() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        waitForRendering(control, timeoutShort);

        mouseClick(control, _clickHelper.columnCommentType, _clickHelper.row1Center);
        wait(timeoutShort);
        verify(control.isCurrentlyEditing);

        mouseClick(control, _clickHelper.columnComment, _clickHelper.row2Center);
        tryVerify(() => control.isNotCurrentlyEditing, timeoutLong);
        compare(control.currentIndex, 0);
    }

    function test_editComment_data() {
        return [
            {
                tag: "via-context-menu",
                exec: control => {
                    const openCtxMenuCoords = _clickHelper.onContextMenuOpen(1);
                    mouseClick(control, openCtxMenuCoords.x, openCtxMenuCoords.y, Qt.RightButton);
                    wait(timeoutLong);

                    const ctxMenuItemCoords = _clickHelper.onContextMenuItem(1, 1);
                    mouseClick(control, ctxMenuItemCoords.x, ctxMenuItemCoords.y);
                }
            },
            {
                tag: "via-shortcut-return",
                exec: control => keyPress(Qt.Key_Return)
            },
        ];
    }

    function test_editComment(data) {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        waitForRendering(control, timeoutShort);

        verify(!control.isCurrentlyEditing);
        data.exec(control);

        verify(control.isCurrentlyEditing);
    }

    function test_copyToClipboard_data() {
        return [
            {
                tag: "via-context-menu",
                exec: control => {
                    const openCtxMenuCoords = _clickHelper.onContextMenuOpen(1);
                    mouseClick(control, openCtxMenuCoords.x, openCtxMenuCoords.y, Qt.RightButton);
                    wait(timeoutLong);

                    const ctxMenuItemCoords = _clickHelper.onContextMenuItem(2, 1);
                    mouseClick(control, ctxMenuItemCoords.x, ctxMenuItemCoords.y);
                }
            },
            {
                tag: "via-shortcut",
                exec: control => {
                    keyPress(Qt.Key_C, Qt.ControlModifier);
                }
            },
        ];
    }

    function test_copyToClipboard(data) {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        waitForRendering(control, timeoutShort);

        data.exec(control);
        waitForRendering(control, timeoutShort);

        tryVerify(() => control.model.calledCopyToClipboard);
    }

    function test_deleteComment_data() {
        return [
            {
                tag: "via-context-menu",
                exec: control => {
                    const openCtxMenuCoords = _clickHelper.onContextMenuOpen(1);
                    mouseClick(control, openCtxMenuCoords.x, openCtxMenuCoords.y, Qt.RightButton);
                    wait(timeoutLong);

                    const ctxMenuItemCoords = _clickHelper.onContextMenuItem(3, 1);
                    mouseClick(control, ctxMenuItemCoords.x, ctxMenuItemCoords.y);
                }
            },
            {
                tag: "via-shortcut-backspace",
                exec: control => keyPress(Qt.Key_Backspace)
            },
            {
                tag: "via-shortcut-delete",
                exec: control => keyPress(Qt.Key_Delete)
            },
        ];
    }

    function test_deleteComment(data) {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        waitForRendering(control, timeoutShort);

        data.exec(control);
        wait(timeoutLong);
        keyPress(Qt.Key_Tab);
        keyPress(Qt.Key_Return);

        tryVerify(() => control.model.calledRemoveRow);
    }
}
