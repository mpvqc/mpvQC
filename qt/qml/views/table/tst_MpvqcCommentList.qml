// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

import pyobjects

import "../../utility"

TestCase {
    id: testCase

    readonly property int timeout: 2000

    property bool enableDebugging: false

    QtObject {
        id: _clickHelper

        function _centerOf(control: MpvqcCommentList, item: Item): point {
            const globalPt = item.mapToGlobal(item.width / 2, item.height / 2);
            return control.mapFromGlobal(globalPt.x, globalPt.y);
        }

        function _topRightOf(control: MpvqcCommentList, item: Item): point {
            const globalPt = item.mapToGlobal(item.width - 3, 3);
            return control.mapFromGlobal(globalPt.x, globalPt.y);
        }

        function _topLeftOf(control: MpvqcCommentList, item: Item): point {
            const globalPt = item.mapToGlobal(3, 3);
            return control.mapFromGlobal(globalPt.x, globalPt.y);
        }

        function centerOfPlayButton(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _centerOf(control, findChild(delegate, "playButton"));
        }

        function centerOfTimeLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _centerOf(control, findChild(delegate, "timeLabel"));
        }

        function centerOfCommentTypeLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _centerOf(control, findChild(delegate, "commentTypeLabel"));
        }

        function centerOfCommentLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _centerOf(control, findChild(delegate, "commentLabel"));
        }

        function topRightOfTimeLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _topRightOf(control, findChild(delegate, "timeLabel"));
        }

        function topLeftOfTimeLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _topLeftOf(control, findChild(delegate, "timeLabel"));
        }

        function topRightOfCommentTypeLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _topRightOf(control, findChild(delegate, "commentTypeLabel"));
        }

        function topRightOfCommentLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _topRightOf(control, findChild(delegate, "commentLabel"));
        }

        function clickContextMenuItem(control: MpvqcCommentList, name: string): void {
            const item = findChild(control.contextMenuLoader.item, name);
            _mouse.click(item, item.width / 2, item.height / 2);
        }

        function clickEditPopupItem(control: MpvqcCommentList, name: string): void {
            const item = findChild(control.editLoader.item, name);
            _mouse.click(item, item.width / 2, item.height / 2);
        }

        function clickCommentTypeMenuItem(control: MpvqcCommentList, commentType: string): void {
            const menu = control.editLoader.item;
            for (let i = 0; i < menu.count; i++) {
                const item = menu.itemAt(i);
                if (item && item.commentType === commentType) {
                    _mouse.click(item, item.width / 2, item.height / 2);
                    return;
                }
            }
        }
    }

    QtObject {
        id: _mouse

        function click(item: Item, x: real, y: real, button, modifiers, delay): void {
            let dot = null;
            if (testCase.enableDebugging) {
                const overlay = item.Overlay.overlay;
                const scenePt = item.mapToItem(null, x, y);
                const overlayPt = overlay.mapFromItem(null, scenePt.x, scenePt.y);
                dot = Qt.createQmlObject(`
                    import QtQuick
                    Rectangle {
                        color: "red"; opacity: 0.8; radius: 8
                        width: 16; height: 16
                        z: 999
                    }`, overlay);
                dot.x = overlayPt.x - 8;
                dot.y = overlayPt.y - 8;
                wait(100);
            }
            mouseClick(item, x, y, button, modifiers, delay);
            if (testCase.enableDebugging) {
                wait(1000);
                dot?.destroy();
            }
        }

        function doubleClick(item: Item, x: real, y: real, button, modifiers, delay): void {
            let ring = null;
            if (testCase.enableDebugging) {
                const overlay = item.Overlay.overlay;
                const scenePt = item.mapToItem(null, x, y);
                const overlayPt = overlay.mapFromItem(null, scenePt.x, scenePt.y);
                ring = Qt.createQmlObject(`
                    import QtQuick
                    Rectangle {
                        color: "transparent"; opacity: 0.9; radius: 10
                        width: 20; height: 20
                        border.color: "black"; border.width: 3
                        z: 999
                    }`, overlay);
                ring.x = overlayPt.x - 10;
                ring.y = overlayPt.y - 10;
                wait(100);
            }
            mouseDoubleClickSequence(item, x, y, button, modifiers, delay);
            if (testCase.enableDebugging) {
                wait(1000);
                ring?.destroy();
            }
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
                property int videoDuration: 10
                property var commentTypes: ["Comment Type 1", "Comment Type 2", "Comment Type 3", "Comment Type 4"]
                function jumpToTime(time) {
                }
                function pauseVideo() {
                }
            }

            height: testCase.height
            width: testCase.width

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

            function getItem(index: int, property: string): var {
                return model.comments()[index][property];
            }
        }
    }

    function initTestCase(): void {
        MpvqcLabelWidthCalculator.timeLabelWidth = 50;
        MpvqcLabelWidthCalculator.commentTypesLabelWidth = 100;
    }

    function cleanup(): void {
        testCase.enableDebugging = false;
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
        tryVerify(() => !control.editLoader.item);
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
                tag: "on-same-row-time-label-clicked",
                centerPoint: control => _clickHelper.centerOfTimeLabel(control, 0),
                rowIndexExpected: 0
            },
            {
                tag: "on-same-row-comment-type-label-clicked",
                centerPoint: control => _clickHelper.centerOfCommentTypeLabel(control, 0),
                rowIndexExpected: 0
            },
            {
                tag: "on-same-row-comment-label-clicked",
                centerPoint: control => _clickHelper.centerOfCommentLabel(control, 0),
                rowIndexExpected: 0
            },
            {
                tag: "on-other-row-play-button-clicked",
                centerPoint: control => _clickHelper.centerOfPlayButton(control, 1),
                rowIndexExpected: 1
            },
            {
                tag: "on-other-row-time-label-clicked",
                centerPoint: control => _clickHelper.centerOfTimeLabel(control, 1),
                rowIndexExpected: 1
            },
            {
                tag: "on-other-row-comment-type-label-clicked",
                centerPoint: control => _clickHelper.centerOfCommentTypeLabel(control, 1),
                rowIndexExpected: 1
            },
            {
                tag: "on-other-row-comment-label-clicked",
                centerPoint: control => _clickHelper.centerOfCommentLabel(control, 1),
                rowIndexExpected: 1
            },
        ];
    }

    function test_selectionWhileNotEditing(data): void {
        const control = makeControl();

        const pt = data.centerPoint(control);
        _mouse.click(control, pt.x, pt.y);
        tryVerify(() => control.isNotCurrentlyEditing);

        compare(control.currentIndex, data.rowIndexExpected);
    }

    function test_selectionWhileEditingComment_data() {
        return [
            {
                tag: "on-same-row-play-button-clicked",
                centerPoint: control => _clickHelper.centerOfPlayButton(control, 0),
                rowIndexExpected: 0
            },
            {
                tag: "on-same-row-time-label-clicked",
                centerPoint: control => _clickHelper.centerOfTimeLabel(control, 0),
                rowIndexExpected: 0
            },
            {
                tag: "on-same-row-comment-type-label-clicked",
                centerPoint: control => _clickHelper.centerOfCommentTypeLabel(control, 0),
                rowIndexExpected: 0
            },
            {
                tag: "on-other-row-play-button-clicked",
                centerPoint: control => _clickHelper.centerOfPlayButton(control, 1),
                rowIndexExpected: 1
            },
            {
                tag: "on-other-row-time-label-clicked",
                centerPoint: control => _clickHelper.centerOfTimeLabel(control, 1),
                rowIndexExpected: 1
            },
            {
                tag: "on-other-row-comment-type-label-clicked",
                centerPoint: control => _clickHelper.centerOfCommentTypeLabel(control, 1),
                rowIndexExpected: 1
            },
            {
                tag: "on-other-row-comment-label-clicked",
                centerPoint: control => _clickHelper.centerOfCommentLabel(control, 1),
                rowIndexExpected: 1
            },
        ];
    }

    function test_selectionWhileEditingComment(data) {
        const control = makeControl();

        keyPress(Qt.Key_Return);
        waitForRendering(control);
        verify(control.isCurrentlyEditing);

        const pt = data.centerPoint(control);
        _mouse.click(control, pt.x, pt.y);
        tryVerify(() => control.isNotCurrentlyEditing);
        compare(control.currentIndex, data.rowIndexExpected);
    }

    function test_selectionWhileEditingTime() {
        const control = makeControl();

        const timeLabel = _clickHelper.centerOfTimeLabel(control, 0);
        _mouse.doubleClick(control, timeLabel.x, timeLabel.y);
        waitUntilEditControlOpened(control);
        verify(control.isCurrentlyEditing);

        const commentLabel = _clickHelper.centerOfCommentLabel(control, 1);
        _mouse.click(control, commentLabel.x, commentLabel.y);
        tryVerify(() => control.isNotCurrentlyEditing);
        compare(control.currentIndex, 0);
    }

    function test_doubleClickWhileEditingTime_data() {
        return [
            {
                tag: "on-same-row-time-label",
                centerPoint: control => _clickHelper.topLeftOfTimeLabel(control, 0)
            },
            {
                tag: "on-same-row-comment-type-label",
                centerPoint: control => _clickHelper.topRightOfCommentTypeLabel(control, 0)
            },
            {
                tag: "on-same-row-comment-label",
                centerPoint: control => _clickHelper.topRightOfCommentLabel(control, 0)
            },
            {
                tag: "on-other-row-time-label",
                centerPoint: control => _clickHelper.topLeftOfTimeLabel(control, 1)
            },
            {
                tag: "on-other-row-comment-type-label",
                centerPoint: control => _clickHelper.topRightOfCommentTypeLabel(control, 1)
            },
            {
                tag: "on-other-row-comment-label",
                centerPoint: control => _clickHelper.topRightOfCommentLabel(control, 1)
            },
        ];
    }

    function test_doubleClickWhileEditingTime(data) {
        const control = makeControl();

        const timeLabel = _clickHelper.centerOfTimeLabel(control, 0);
        _mouse.doubleClick(control, timeLabel.x, timeLabel.y);
        waitUntilEditControlOpened(control);
        verify(control.isCurrentlyEditing);

        const pt = data.centerPoint(control);
        _mouse.doubleClick(control, pt.x, pt.y);
        tryVerify(() => control.isNotCurrentlyEditing);
        compare(control.currentIndex, 0);
    }

    function test_selectionWhileEditingCommentType() {
        const control = makeControl();

        const commentTypeLabel = _clickHelper.centerOfCommentTypeLabel(control, 0);
        _mouse.doubleClick(control, commentTypeLabel.x, commentTypeLabel.y);
        waitUntilEditControlOpened(control);
        verify(control.isCurrentlyEditing);

        const commentLabel = _clickHelper.centerOfCommentLabel(control, 1);
        _mouse.click(control, commentLabel.x, commentLabel.y);
        tryVerify(() => control.isNotCurrentlyEditing);
        compare(control.currentIndex, 0);
    }

    function test_doubleClickWhileEditingCommentType_data() {
        return [
            {
                tag: "on-same-row-time-label",
                centerPoint: control => _clickHelper.topLeftOfTimeLabel(control, 0)
            },
            {
                tag: "on-same-row-comment-type-label",
                centerPoint: control => _clickHelper.topRightOfCommentTypeLabel(control, 0)
            },
            {
                tag: "on-same-row-comment-label",
                centerPoint: control => _clickHelper.topRightOfCommentLabel(control, 0)
            },
            {
                tag: "on-other-row-time-label",
                centerPoint: control => _clickHelper.topLeftOfTimeLabel(control, 1)
            },
            {
                tag: "on-other-row-comment-type-label",
                centerPoint: control => _clickHelper.topRightOfCommentTypeLabel(control, 1)
            },
            {
                tag: "on-other-row-comment-label",
                centerPoint: control => _clickHelper.topRightOfCommentLabel(control, 1)
            },
        ];
    }

    function test_doubleClickWhileEditingCommentType(data) {
        const control = makeControl();

        const commentTypeLabel = _clickHelper.centerOfCommentTypeLabel(control, 0);
        _mouse.doubleClick(control, commentTypeLabel.x, commentTypeLabel.y);
        waitUntilEditControlOpened(control);
        verify(control.isCurrentlyEditing);

        const pt = data.centerPoint(control);
        _mouse.doubleClick(control, pt.x, pt.y);
        tryVerify(() => control.isNotCurrentlyEditing);
        compare(control.currentIndex, 0);
    }

    function test_editCommentTrigger_data() {
        return [
            {
                tag: "via-context-menu",
                exec: control => {
                    const pt = _clickHelper.centerOfCommentLabel(control, 1);
                    _mouse.click(control, pt.x, pt.y, Qt.RightButton);
                    waitUntilContextMenuOpened(control);

                    _clickHelper.clickContextMenuItem(control, "editCommentAction");
                }
            },
            {
                tag: "via-shortcut-return",
                exec: control => keyPress(Qt.Key_Return)
            },
            {
                tag: "via-double-click-on-selected-row",
                exec: control => {
                    const pt = _clickHelper.centerOfCommentLabel(control, 0);
                    _mouse.doubleClick(control, pt.x, pt.y);
                }
            },
            {
                tag: "via-double-click-on-unselected-row",
                exec: control => {
                    const pt = _clickHelper.centerOfCommentLabel(control, 1);
                    _mouse.doubleClick(control, pt.x, pt.y);
                }
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
                    const pt = _clickHelper.centerOfCommentLabel(control, 1);
                    _mouse.click(control, pt.x, pt.y, Qt.RightButton);
                    waitUntilContextMenuOpened(control);

                    _clickHelper.clickContextMenuItem(control, "copyCommentAction");
                },
                expected: "[00:00:02] [Comment Type 2] Comment 2"
            },
            {
                tag: "via-shortcut",
                exec: control => {
                    keyPress(Qt.Key_C, Qt.ControlModifier);
                },
                expected: "[00:00:01] [Comment Type 1] Comment 1"
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
        compare(spy.signalArguments[0][0], data.expected);
    }

    function test_deleteComment_data() {
        return [
            {
                tag: "via-context-menu",
                exec: control => {
                    const pt = _clickHelper.centerOfCommentLabel(control, 0);
                    _mouse.click(control, pt.x, pt.y, Qt.RightButton);
                    waitUntilContextMenuOpened(control);

                    _clickHelper.clickContextMenuItem(control, "deleteCommentAction");
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

        const timeLabel = _clickHelper.centerOfTimeLabel(control, 0);
        _mouse.doubleClick(control, timeLabel.x, timeLabel.y);
        waitUntilEditControlOpened(control);

        _clickHelper.clickEditPopupItem(control, "decrementButton");

        const commentLabel = _clickHelper.centerOfCommentLabel(control, 0);
        _mouse.click(control, commentLabel.x, commentLabel.y);

        tryVerify(() => control.getItem(0, "time") === 0);
    }

    function test_editTimeNext() {
        const control = makeControl();

        tryVerify(() => control.getItem(0, "time") === 1);

        const timeLabel = _clickHelper.centerOfTimeLabel(control, 0);
        _mouse.doubleClick(control, timeLabel.x, timeLabel.y);
        waitUntilEditControlOpened(control);

        _clickHelper.clickEditPopupItem(control, "incrementButton");

        const commentLabel = _clickHelper.centerOfCommentLabel(control, 0);
        _mouse.click(control, commentLabel.x, commentLabel.y);

        tryVerify(() => control.getItem(0, "time") === 2);
    }

    function test_editTimeAborted() {
        const control = makeControl();

        tryVerify(() => control.getItem(0, "time") === 1);

        const timeLabel = _clickHelper.centerOfTimeLabel(control, 0);
        _mouse.doubleClick(control, timeLabel.x, timeLabel.y);
        waitUntilEditControlOpened(control);

        const timeChangedSpy = createTemporaryObject(signalSpy, control, {
            target: control.editLoader.item,
            signalName: "timeTemporaryChanged"
        });
        verify(timeChangedSpy);

        _clickHelper.clickEditPopupItem(control, "decrementButton");
        tryVerify(() => timeChangedSpy.signalArguments[0][0] === 0);

        keyPress(Qt.Key_Escape);
        waitUntilEditControlClosed(control);

        tryVerify(() => control.getItem(0, "time") === 1);
    }

    function test_editCommentType(): void {
        const control = makeControl();

        const commentTypeLabel = _clickHelper.centerOfCommentTypeLabel(control, 0);
        _mouse.doubleClick(control, commentTypeLabel.x, commentTypeLabel.y);
        waitUntilEditControlOpened(control);

        _clickHelper.clickCommentTypeMenuItem(control, "Comment Type 3");

        compare(control.getItem(0, "commentType"), "Comment Type 3");
    }

    function test_editCommentTypeAborted(): void {
        const control = makeControl();

        const commentTypeLabel = _clickHelper.centerOfCommentTypeLabel(control, 0);
        _mouse.doubleClick(control, commentTypeLabel.x, commentTypeLabel.y);
        waitUntilEditControlOpened(control);

        keyPress(Qt.Key_Escape);
        waitUntilEditControlClosed(control);

        compare(control.getItem(0, "commentType"), "Comment Type 1");
    }

    function test_editComment(): void {
        const control = makeControl();

        const commentLabel = _clickHelper.centerOfCommentLabel(control, 0);
        _mouse.doubleClick(control, commentLabel.x, commentLabel.y);
        waitUntilEditControlOpened(control);

        keyPress("h");
        keyPress("i");
        keyPress(Qt.Key_Return);
        compare(control.getItem(0, "comment"), "hi");
    }

    function test_editCommentAborted(): void {
        const control = makeControl();

        compare(control.getItem(0, "comment"), "Comment 1");

        const commentLabel = _clickHelper.centerOfCommentLabel(control, 0);
        _mouse.doubleClick(control, commentLabel.x, commentLabel.y);
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

        const commentLabel = _clickHelper.centerOfCommentLabel(control, 0);
        _mouse.doubleClick(control, commentLabel.x, commentLabel.y);
        waitUntilEditControlOpened(control);

        keyPress(Qt.Key_Return);
        waitUntilEditControlClosed(control);
        compare(control.getItem(0, "comment"), "Comment 1");
    }

    function test_editCommentThenDoubleClickAnother(): void {
        const control = makeControl();

        // Start editing first comment
        const commentLabel0 = _clickHelper.centerOfCommentLabel(control, 0);
        _mouse.doubleClick(control, commentLabel0.x, commentLabel0.y);
        waitUntilEditControlOpened(control);

        // Type some text
        keyPress("h");
        keyPress("i");

        // Double-click on second comment
        const commentLabel1 = _clickHelper.centerOfCommentLabel(control, 1);
        _mouse.doubleClick(control, commentLabel1.x, commentLabel1.y);
        waitUntilEditControlOpened(control);

        // Verify editing was successful
        compare(control.getItem(0, "comment"), "hi");

        wait(testCase.timeout);

        // Verify editing is still active even after timeout
        verify(control.isCurrentlyEditing);
        verify(control.editLoader.item);
        compare(control.currentIndex, 1);
        // Verify content in editing mode is correct
        compare(control.editLoader.item.textField.text, "Comment 2");
        // Verify text below the editing popup is empty
        compare(control.itemAtIndex(1).commentLabel.text, "");

        _mouse.click(control, commentLabel0.x, commentLabel0.y);
        // Verify text is displayed again
        tryCompare(control.itemAtIndex(1).commentLabel, "text", "Comment 2");
    }
}
