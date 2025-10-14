// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import pyobjects

import "../../utility"

TestCase {
    id: testCase

    readonly property int timeout: 2000

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
            const yCoordinate = yTableRow + contextMenuItemHeight * index;
            return Qt.point(xCoordinate, yCoordinate);
        }

        function onEditTimeMenuSeekBack(tableRow: int): point {
            const xCoordinate = columnTime + 20;
            const yCoordinate = rowHeight * tableRow;
            return Qt.point(xCoordinate, yCoordinate);
        }

        function onEditTimeMenuSeekForward(tableRow: int): point {
            const xCoordinate = columnTime + 110;
            const yCoordinate = rowHeight * tableRow;
            return Qt.point(xCoordinate, yCoordinate);
        }

        function onEditCommentTypeMenu(index: int, tableRow: int): point {
            const contextMenuItemHeight = 34;
            const xCoordinate = columnCommentType + 20;
            const yTableRow = (rowHeight / 2) + rowHeight * (tableRow - 1);
            const yCoordinate = yTableRow + contextMenuItemHeight * index;
            return Qt.point(xCoordinate, yCoordinate);
        }
    }

    width: 600
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcCommentList"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcCommentList {
            viewModel: MpvqcCommentTableViewModel {
                model: MpvqcCommentModel {}
                property int videoDuration: 10
                function jumpToTime(time) {
                }
                function pauseVideo() {
                }
            }

            height: testCase.height
            width: testCase.width

            commentTypes: ["Comment Type 1", "Comment Type 2", "Comment Type 3", "Comment Type 4"]

            Component.onCompleted: {
                model.import_comments([
                    {
                        "time": 1,
                        "commentType": "Comment Type 1",
                        "comment": "Comment 1"
                    },
                    {
                        "time": 2,
                        "commentType": "Comment Type 2",
                        "comment": "Comment 2"
                    },
                    {
                        "time": 3,
                        "commentType": "Comment Type 3",
                        "comment": "Comment 3"
                    },
                    {
                        "time": 4,
                        "commentType": "Comment Type 4",
                        "comment": "Comment 4"
                    },
                ]);
                currentIndex = 0;
            }

            function getItem(index: int, property: string): variant {
                return model.comments()[index][property];
            }
        }
    }

    function initTestCase(): void {
        MpvqcLabelWidthCalculator.timeLabelWidth = 50;
        MpvqcLabelWidthCalculator.commentTypesLabelWidth = 100;
    }

    function makeControl(): var {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        waitForRendering(control);
        return control;
    }

    function waitUntilEditControlOpened(control: MpvqcCommentList): void {
        tryCompare(control.editLoader, "status", Loader.Ready, testCase.timeout);
        tryVerify(() => control.editLoader.item?.opened);
    }

    function waitUntilEditControlClosed(control: MpvqcCommentList): void {
        tryCompare(control.editLoader, "status", Loader.Ready, testCase.timeout);
        tryVerify(() => control.editLoader.item?.closed);
    }

    function waitUntilContextMenuOpened(control: MpvqcCommentList): void {
        tryCompare(control.contextMenuLoader, "status", Loader.Ready, testCase.timeout);
        tryVerify(() => control.contextMenuLoader.item?.opened);
    }

    function waitUntilMessageBoxOpened(control: MpvqcCommentList): void {
        tryCompare(control.messageBoxLoader, "status", Loader.Ready, testCase.timeout);
        tryVerify(() => control.messageBoxLoader.item?.opened);
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
        const control = makeControl();

        mouseClick(control, data.column, _clickHelper.row2Center);
        tryVerify(() => control.isNotCurrentlyEditing);

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
        const control = makeControl();

        keyPress(Qt.Key_Return);
        waitForRendering(control);
        verify(control.isCurrentlyEditing);

        mouseClick(control, data.columnClicked, data.rowClicked);
        tryVerify(() => control.isNotCurrentlyEditing);
        compare(control.currentIndex, data.rowIndexExpected);
    }

    function test_selectionWhileEditingTime() {
        const control = makeControl();

        mouseClick(control, _clickHelper.columnTime, _clickHelper.row1Center);
        waitUntilEditControlOpened(control);
        verify(control.isCurrentlyEditing);

        mouseClick(control, _clickHelper.columnComment, _clickHelper.row2Center);
        tryVerify(() => control.isNotCurrentlyEditing);
        compare(control.currentIndex, 0);
    }

    function test_selectionWhileEditingCommentType() {
        const control = makeControl();

        mouseClick(control, _clickHelper.columnCommentType, _clickHelper.row1Center);
        waitUntilEditControlOpened(control);
        verify(control.isCurrentlyEditing);

        mouseClick(control, _clickHelper.columnComment, _clickHelper.row2Center);
        tryVerify(() => control.isNotCurrentlyEditing);
        compare(control.currentIndex, 0);
    }

    function test_editCommentTrigger_data() {
        return [
            {
                tag: "via-context-menu",
                exec: control => {
                    const openCtxMenuCoords = _clickHelper.onContextMenuOpen(1);
                    mouseClick(control, openCtxMenuCoords.x, openCtxMenuCoords.y, Qt.RightButton);
                    waitUntilContextMenuOpened(control);

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

    function test_editCommentTrigger(data) {
        const control = makeControl();

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
                    waitUntilContextMenuOpened(control);

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
        const control = makeControl();

        const spy = createTemporaryObject(signalSpy, control, {
            target: control.viewModel,
            signalName: "copiedToClipboard"
        });
        verify(spy);

        data.exec(control);
        waitForRendering(control);

        tryVerify(() => spy.count === 1);
    }

    function test_deleteComment_data() {
        return [
            {
                tag: "via-context-menu",
                exec: control => {
                    const openCtxMenuCoords = _clickHelper.onContextMenuOpen(1);
                    mouseClick(control, openCtxMenuCoords.x, openCtxMenuCoords.y, Qt.RightButton);
                    waitUntilContextMenuOpened(control);

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
        const control = makeControl();

        data.exec(control);
        waitUntilMessageBoxOpened(control);
        keyPress(Qt.Key_Tab);
        keyPress(Qt.Key_Return);

        tryVerify(() => control.count === 3);
    }

    function test_editTimePrevious() {
        const control = makeControl();

        tryVerify(() => control.getItem(0, "time") === 1);

        mouseClick(control, _clickHelper.columnTime, _clickHelper.row1Center);
        waitUntilEditControlOpened(control);

        const btn = _clickHelper.onEditTimeMenuSeekBack(1);
        mouseClick(control, btn.x, btn.y);
        mouseClick(control, _clickHelper.columnComment, _clickHelper.row1Center);

        tryVerify(() => control.getItem(0, "time") === 0);
    }

    function test_editTimeNext() {
        const control = makeControl();

        tryVerify(() => control.getItem(0, "time") === 1);

        mouseClick(control, _clickHelper.columnTime, _clickHelper.row1Center);
        waitUntilEditControlOpened(control);

        const btn = _clickHelper.onEditTimeMenuSeekForward(1);
        mouseClick(control, btn.x, btn.y);
        mouseClick(control, _clickHelper.columnComment, _clickHelper.row1Center);

        tryVerify(() => control.getItem(0, "time") === 2);
    }

    function test_editTimeAborted() {
        const control = makeControl();

        tryVerify(() => control.getItem(0, "time") === 1);

        mouseClick(control, _clickHelper.columnTime, _clickHelper.row1Center);
        waitUntilEditControlOpened(control);

        const timeChangedSpy = createTemporaryObject(signalSpy, control, {
            target: control.editLoader.item,
            signalName: "timeTemporaryChanged"
        });
        verify(timeChangedSpy);

        const btn = _clickHelper.onEditTimeMenuSeekBack(1);
        mouseClick(control, btn.x, btn.y);

        tryCompare(timeChangedSpy, "count", 1);
        tryVerify(() => timeChangedSpy.signalArguments[0][0] === 0);

        keyPress(Qt.Key_Escape);
        waitUntilEditControlClosed(control);

        tryVerify(() => control.getItem(0, "time") === 1);
    }

    function test_editCommentTypeAborted(): void {
        const control = makeControl();

        mouseClick(control, _clickHelper.columnCommentType, _clickHelper.row1Center);
        waitUntilEditControlOpened(control);

        keyPress(Qt.Key_Escape);
        waitUntilEditControlClosed(control);

        compare(control.getItem(0, "commentType"), "Comment Type 1");
    }

    function test_editCommentType(): void {
        const control = makeControl();

        mouseClick(control, _clickHelper.columnCommentType, _clickHelper.row1Center);
        waitUntilEditControlOpened(control);

        const btn = _clickHelper.onEditCommentTypeMenu(3, 1);
        mouseClick(control, btn.x, btn.y);

        compare(control.getItem(0, "commentType"), "Comment Type 3");
    }

    function test_editComment(): void {
        const control = makeControl();

        mouseClick(control, _clickHelper.columnComment, _clickHelper.row1Center);
        waitUntilEditControlOpened(control);

        keyPress("h");
        keyPress("i");
        keyPress(Qt.Key_Return);
        compare(control.getItem(0, "comment"), "hi");
    }

    function test_editCommentAborted(): void {
        const control = makeControl();

        compare(control.getItem(0, "comment"), "Comment 1");

        mouseClick(control, _clickHelper.columnComment, _clickHelper.row1Center);
        waitUntilEditControlOpened(control);

        keyPress("h");
        keyPress("i");
        keyPress(Qt.Key_Escape);
        waitUntilEditControlClosed(control);
        compare(control.getItem(0, "comment"), "Comment 1");
    }

    function test_editCommentConfirmUnchanged(): void {
        const control = makeControl();

        compare(control.getItem(0, "comment"), "Comment 1");

        mouseClick(control, _clickHelper.columnComment, _clickHelper.row1Center);
        waitUntilEditControlOpened(control);

        keyPress(Qt.Key_Return);
        waitUntilEditControlClosed(control);
        compare(control.getItem(0, "comment"), "Comment 1");
    }
}
