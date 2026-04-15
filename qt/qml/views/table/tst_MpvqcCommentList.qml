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
            return _centerOf(control, testCase.findChild(delegate, "playButton"));
        }

        function topRightOfPlayButton(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _topRightOf(control, testCase.findChild(delegate, "playButton"));
        }

        function centerOfTimeLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _centerOf(control, testCase.findChild(delegate, "timeLabel"));
        }

        function centerOfCommentTypeLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _centerOf(control, testCase.findChild(delegate, "commentTypeLabel"));
        }

        function centerOfCommentLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _centerOf(control, testCase.findChild(delegate, "commentLabel"));
        }

        function topRightOfTimeLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _topRightOf(control, testCase.findChild(delegate, "timeLabel"));
        }

        function topLeftOfTimeLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _topLeftOf(control, testCase.findChild(delegate, "timeLabel"));
        }

        function topRightOfCommentTypeLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _topRightOf(control, testCase.findChild(delegate, "commentTypeLabel"));
        }

        function topRightOfCommentLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _topRightOf(control, testCase.findChild(delegate, "commentLabel"));
        }

        function topLeftOfCommentLabel(control: MpvqcCommentList, row: int): point {
            const delegate = control.itemAtIndex(row);
            return _topLeftOf(control, testCase.findChild(delegate, "commentLabel"));
        }

        function clickEditCommentAction(control: MpvqcCommentList): void {
            const item = testCase.findChild(control.contextMenuLoader.item, "editCommentAction");
            testCase.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickCopyCommentAction(control: MpvqcCommentList): void {
            const item = testCase.findChild(control.contextMenuLoader.item, "copyCommentAction");
            testCase.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickDeleteCommentAction(control: MpvqcCommentList): void {
            const item = testCase.findChild(control.contextMenuLoader.item, "deleteCommentAction");
            testCase.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickDecrementButton(control: MpvqcCommentList): void {
            const item = testCase.findChild(control.editLoader.item, "decrementButton");
            testCase.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickIncrementButton(control: MpvqcCommentList): void {
            const item = testCase.findChild(control.editLoader.item, "incrementButton");
            testCase.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickSearchNextButton(control: MpvqcCommentList): void {
            const btn = _find.searchNextButton(control);
            testCase.mouseClick(btn, btn.width / 2, btn.height / 2);
        }

        function clickSearchPreviousButton(control: MpvqcCommentList): void {
            const btn = _find.searchPreviousButton(control);
            testCase.mouseClick(btn, btn.width / 2, btn.height / 2);
        }

        function clickSearchCloseButton(control: MpvqcCommentList): void {
            const btn = _find.searchCloseButton(control);
            testCase.mouseClick(btn, btn.width / 2, btn.height / 2);
        }

        function clickCommentTypeMenuItem(control: MpvqcCommentList, commentType: string): void {
            const menu = control.editLoader.item;
            for (let i = 0; i < menu.count; i++) { // qmllint disable
                const item = menu.itemAt(i); // qmllint disable
                if (item && item.commentType === commentType) {
                    testCase.mouseClick(item, item.width / 2, item.height / 2);
                    return;
                }
            }
        }
    }

    QtObject {
        id: _expect

        function isNotEditing(control: MpvqcCommentList): void {
            testCase.verify(control.isNotCurrentlyEditing);
        }

        function isEventuallyNotEditing(control: MpvqcCommentList): void {
            testCase.tryVerify(() => control.isNotCurrentlyEditing);
        }

        function isEditing(control: MpvqcCommentList): void {
            testCase.verify(control.isCurrentlyEditing);
        }

        function isHandlingKeyEvents(control: MpvqcCommentList): void {
            testCase.verify(control.isHandleKeyEvents);
        }

        function isNotHandlingKeyEvents(control: MpvqcCommentList): void {
            testCase.verify(!control.isHandleKeyEvents);
        }

        function isInteractive(control: MpvqcCommentList): void {
            testCase.verify(control.interactive);
        }

        function isNotInteractive(control: MpvqcCommentList): void {
            testCase.verify(!control.interactive);
        }

        function hasContextMenuOpen(control: MpvqcCommentList): void {
            testCase.verify(control.contextMenuLoader.active);
            testCase.verify(control.contextMenuLoader.item);
        }

        function hasContextMenuClosed(control: MpvqcCommentList): void {
            testCase.verify(!control.contextMenuLoader.active);
            testCase.verify(!control.contextMenuLoader.item);
        }

        function hasMessageBoxOpen(control: MpvqcCommentList): void {
            testCase.verify(control.messageBoxLoader.active);
            testCase.verify(control.messageBoxLoader.item);
        }

        function hasMessageBoxClosed(control: MpvqcCommentList): void {
            testCase.verify(!control.messageBoxLoader.active);
            testCase.verify(!control.messageBoxLoader.item);
        }

        function hasSearchBoxOpen(control: MpvqcCommentList): void {
            testCase.verify(control.searchBoxLoader.active);
            testCase.verify(control.searchBoxLoader.item);
            testCase.verify(control.searchBoxLoader.item?.searchActive);
        }

        function hasSearchBoxClosed(control: MpvqcCommentList): void {
            testCase.verify(!control.searchBoxLoader.item?.searchActive);
        }

        function isEventuallySearchBoxOpen(control: MpvqcCommentList): void {
            testCase.tryVerify(() => control.searchBoxLoader.item?.searchActive);
        }

        function isEventuallySearchBoxClosed(control: MpvqcCommentList): void {
            testCase.tryVerify(() => !control.searchBoxLoader.item?.searchActive);
        }

        function hasActiveFocus(control: MpvqcCommentList): void {
            testCase.tryVerify(() => control.activeFocus);
        }

        function hasCurrentIndex(control: MpvqcCommentList, expected: int): void {
            testCase.compare(control.currentIndex, expected);
        }

        function hasCount(control: MpvqcCommentList, expected: int): void {
            testCase.compare(control.count, expected);
        }

        function hasEventuallyCount(control: MpvqcCommentList, expected: int): void {
            testCase.tryVerify(() => control.count === expected);
        }

        function isEditorShowing(control: MpvqcCommentList, editor: string): void {
            const expected = {
                "timePopup": control.editLoader.editTimePopup,
                "commentTypeMenu": control.editLoader.editCommentTypeMenu,
                "commentPopup": control.editLoader.editCommentPopup
            }[editor];
            testCase.compare(control.editLoader.source, expected);
        }

        function isEditorShowingTimePopup(control: MpvqcCommentList): void {
            isEditorShowing(control, "timePopup");
        }

        function isEditorShowingCommentTypeMenu(control: MpvqcCommentList): void {
            isEditorShowing(control, "commentTypeMenu");
        }

        function isEditorShowingCommentPopup(control: MpvqcCommentList): void {
            isEditorShowing(control, "commentPopup");
        }

        function hasItemTime(control: MpvqcCommentList, index: int, expected: int): void {
            testCase.compare(control.getItem(index, "time"), expected);
        }

        function hasItemCommentType(control: MpvqcCommentList, index: int, expected: string): void {
            testCase.compare(control.getItem(index, "commentType"), expected);
        }

        function hasItemComment(control: MpvqcCommentList, index: int, expected: string): void {
            testCase.compare(control.getItem(index, "comment"), expected);
        }

        function hasLastJumpedToTime(control: MpvqcCommentList, expected: int): void {
            testCase.compare(control.viewModel.lastJumpToTime, expected);
        }
    }

    QtObject {
        id: _find

        function timeSpinBox(control: MpvqcCommentList): Item {
            return testCase.findChild(control.editLoader.item, "timeSpinBox");
        }

        function commentTextArea(control: MpvqcCommentList): Item {
            return testCase.findChild(control, "commentTextArea");
        }

        function commentLabel(delegate: Item): Item {
            return testCase.findChild(delegate, "commentLabel");
        }

        function searchBoxPopup(control: MpvqcCommentList): var {
            return testCase.findChild(control, "searchBoxPopup");
        }

        function searchIconLabel(control: MpvqcCommentList): Item {
            return testCase.findChild(searchBoxPopup(control), "searchIconLabel");
        }

        function searchStatusLabel(control: MpvqcCommentList): Item {
            return testCase.findChild(control.searchBoxLoader.item, "statusLabel");
        }

        function searchPreviousButton(control: MpvqcCommentList): Item {
            return testCase.findChild(control.searchBoxLoader.item, "previousButton");
        }

        function searchNextButton(control: MpvqcCommentList): Item {
            return testCase.findChild(control.searchBoxLoader.item, "nextButton");
        }

        function searchCloseButton(control: MpvqcCommentList): Item {
            return testCase.findChild(control.searchBoxLoader.item, "closeButton");
        }

        function searchTextField(control: MpvqcCommentList): Item {
            return testCase.findChild(control.searchBoxLoader.item, "searchTextField");
        }

        function searchDragArea(control: MpvqcCommentList): Item {
            return searchBoxPopup(control).contentItem;
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
        id: objectWithRealViewModel

        MpvqcCommentList {
            viewModel: MpvqcCommentTableViewModel {}

            height: testCase.height
            width: testCase.width

            Component.onCompleted: {
                model.import_comments([
                    {
                        "time": 1,
                        "commentType": "Comment Type 1",
                        "comment": "Comment 1"
                    }
                ]);
                currentIndex = 0;
            }
        }
    }

    Component {
        id: objectUnderTest

        MpvqcCommentList {
            viewModel: MpvqcCommentTableViewModel {
                property int videoDuration: 10
                property var commentTypes: ["Comment Type 1", "Comment Type 2", "Comment Type 3", "Comment Type 4", "Comment Type 5"]
                property int lastJumpToTime: -1
                function jumpToTime(time) {
                    lastJumpToTime = time;
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
                    {
                        "time": 5,
                        "commentType": "Comment Type 5",
                        "comment": "Comment 5"
                    },
                ]);
                currentIndex = 0;
            }

            function getItem(index: int, property: string): var {
                return model.comments()[index][property];
            }
        }
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

    function waitUntilContextMenuClosed(control: MpvqcCommentList): void {
        tryVerify(() => !control.contextMenuLoader.item);
    }

    function waitUntilMessageBoxOpened(control: MpvqcCommentList): void {
        tryCompare(control.messageBoxLoader, "status", Loader.Ready, testCase.timeout);
        tryVerify(() => control.messageBoxLoader.item?.opened);
    }

    function waitUntilMessageBoxClosed(control: MpvqcCommentList): void {
        tryVerify(() => !control.messageBoxLoader.item);
    }

    function waitUntilSearchBoxOpened(control: MpvqcCommentList): void {
        tryCompare(control.searchBoxLoader, "status", Loader.Ready, testCase.timeout);
        tryVerify(() => control.searchBoxLoader.item?.searchActive);
        tryVerify(() => control.searchBoxLoader.item?.opened);
    }

    function waitUntilSearchBoxClosed(control: MpvqcCommentList): void {
        tryVerify(() => !control.searchBoxLoader.item.searchActive);
        tryVerify(() => !control.searchBoxLoader.item?.opened);
    }

    function waitUntilEventsProcessed(): void {
        wait(0);
    }

    function getCommentTypeItems(control: MpvqcCommentList): list<Item> {
        const menu = control.editLoader.item;
        const items = [];
        for (let i = 0; i < menu.count; i++) { // qmllint disable
            const item = menu.itemAt(i); // qmllint disable
            if (item && item.commentType) {
                items.push(item);
            }
        }
        return items;
    }

    function initTestCase(): void {
        MpvqcLabelWidthCalculator.timeLabelWidth = 50;
        MpvqcLabelWidthCalculator.commentTypesLabelWidth = 150;
    }

    function typeWord(word: string): void {
        for (const c of word) {
            keyPress(`${c}`);
        }
    }

    function test_commentTypeMenuReceivesPythonCommentTypes(): void {
        const control = createTemporaryObject(objectWithRealViewModel, testCase);
        verify(control);
        waitForRendering(control);

        const expected = control.viewModel.commentTypes;
        verify(expected.length > 0);

        const pt = _clickHelper.centerOfCommentTypeLabel(control, 0);
        testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
        waitUntilEditControlOpened(control);

        const menu = control.editLoader.item;
        verify(menu.commentTypes.length >= expected.length);

        for (const commentType of expected) {
            verify(menu.commentTypes.includes(commentType), `Missing comment type: ${commentType}. Menu has types: ${menu.commentTypes.join(", ")} includes`);
        }
    }

    TestCase {
        name: "MpvqcCommentList::NotEditing"

        property var control: null

        function initTestCase(): void {
            testCase.initTestCase();
        }

        function init(): void {
            control = testCase.makeControl();
            control.currentIndex = 2;
            waitForRendering(control);
            _expect.isNotEditing(control);
            _expect.isInteractive(control);
            _expect.hasContextMenuClosed(control);
            _expect.hasMessageBoxClosed(control);
        }

        function cleanup(): void {
            control.destroy();
            control = null;
        }

        function test_singleClick_data(): list<var> {
            return [
                {
                    tag: "selected-row-play-button",
                    clickPoint: c => _clickHelper.centerOfPlayButton(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-time-label",
                    clickPoint: c => _clickHelper.centerOfTimeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-type-label",
                    clickPoint: c => _clickHelper.centerOfCommentTypeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-label",
                    clickPoint: c => _clickHelper.centerOfCommentLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-play-button",
                    clickPoint: c => _clickHelper.centerOfPlayButton(c, 1),
                    expectedIndex: 1
                },
                {
                    tag: "other-row-time-label",
                    clickPoint: c => _clickHelper.centerOfTimeLabel(c, 1),
                    expectedIndex: 1
                },
                {
                    tag: "other-row-comment-type-label",
                    clickPoint: c => _clickHelper.centerOfCommentTypeLabel(c, 1),
                    expectedIndex: 1
                },
                {
                    tag: "other-row-comment-label",
                    clickPoint: c => _clickHelper.centerOfCommentLabel(c, 1),
                    expectedIndex: 1
                },
            ];
        }

        function test_singleClick(data): void {
            const pt = data.clickPoint(control);
            testCase.mouseClick(control, pt.x, pt.y);
            _expect.isEventuallyNotEditing(control);
            _expect.hasCurrentIndex(control, data.expectedIndex);
        }

        function test_playButtonJumpsToTime_data(): list<var> {
            return [
                {
                    tag: "selected-row",
                    row: 2,
                    expectedTime: 3
                },
                {
                    tag: "other-row",
                    row: 1,
                    expectedTime: 2
                },
            ];
        }

        function test_playButtonJumpsToTime(data): void {
            const pt = _clickHelper.centerOfPlayButton(control, data.row);
            testCase.mouseClick(control, pt.x, pt.y);
            _expect.hasLastJumpedToTime(control, data.expectedTime);
        }

        function test_doubleClickOpensEditor_data(): list<var> {
            return [
                {
                    tag: "selected-row-time-label",
                    clickPoint: c => _clickHelper.centerOfTimeLabel(c, 2),
                    expectedIndex: 2,
                    expectedEditor: "timePopup"
                },
                {
                    tag: "selected-row-comment-type-label",
                    clickPoint: c => _clickHelper.centerOfCommentTypeLabel(c, 2),
                    expectedIndex: 2,
                    expectedEditor: "commentTypeMenu"
                },
                {
                    tag: "selected-row-comment-label",
                    clickPoint: c => _clickHelper.centerOfCommentLabel(c, 2),
                    expectedIndex: 2,
                    expectedEditor: "commentPopup"
                },
                {
                    tag: "other-row-time-label",
                    clickPoint: c => _clickHelper.centerOfTimeLabel(c, 1),
                    expectedIndex: 1,
                    expectedEditor: "timePopup"
                },
                {
                    tag: "other-row-comment-type-label",
                    clickPoint: c => _clickHelper.centerOfCommentTypeLabel(c, 1),
                    expectedIndex: 1,
                    expectedEditor: "commentTypeMenu"
                },
                {
                    tag: "other-row-comment-label",
                    clickPoint: c => _clickHelper.centerOfCommentLabel(c, 1),
                    expectedIndex: 1,
                    expectedEditor: "commentPopup"
                },
            ];
        }

        function test_doubleClickOpensEditor(data): void {
            const pt = data.clickPoint(control);
            testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
            testCase.waitUntilEditControlOpened(control);
            _expect.isEditing(control);
            _expect.isEditorShowing(control, data.expectedEditor);
            _expect.hasCurrentIndex(control, data.expectedIndex);
        }

        function test_rightClickOpensContextMenu_data(): list<var> {
            return [
                {
                    tag: "selected-row",
                    clickPoint: c => _clickHelper.centerOfCommentLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "other-row",
                    clickPoint: c => _clickHelper.centerOfCommentLabel(c, 1),
                    expectedIndex: 1
                },
            ];
        }

        function test_rightClickOpensContextMenu(data): void {
            const pt = data.clickPoint(control);
            testCase.mouseClick(control, pt.x, pt.y, Qt.RightButton);
            testCase.waitUntilContextMenuOpened(control);
            _expect.hasCurrentIndex(control, data.expectedIndex);
        }

        function test_keyEventsAreHandled(): void {
            _expect.isHandlingKeyEvents(control);
        }

        function test_keyPressDownArrowIncrementsIndex_data(): list<var> {
            return [
                {
                    tag: "middle",
                    startIndex: 2,
                    expectedIndex: 3
                },
                {
                    tag: "boundary",
                    startIndex: 4,
                    expectedIndex: 4
                },
            ];
        }

        function test_keyPressDownArrowIncrementsIndex(data): void {
            control.currentIndex = data.startIndex;
            keyPress(Qt.Key_Down);
            _expect.hasCurrentIndex(control, data.expectedIndex);
        }

        function test_keyPressUpArrowDecrementsIndex_data(): list<var> {
            return [
                {
                    tag: "middle",
                    startIndex: 2,
                    expectedIndex: 1
                },
                {
                    tag: "boundary",
                    startIndex: 0,
                    expectedIndex: 0
                },
            ];
        }

        function test_keyPressUpArrowDecrementsIndex(data): void {
            control.currentIndex = data.startIndex;
            keyPress(Qt.Key_Up);
            _expect.hasCurrentIndex(control, data.expectedIndex);
        }

        function test_keyPressReturnOpensCommentEditor(): void {
            keyPress(Qt.Key_Return);
            testCase.waitUntilEditControlOpened(control);
            _expect.isEditing(control);
            _expect.isNotHandlingKeyEvents(control);
            _expect.isEditorShowingCommentPopup(control);
        }

        function test_keyPressBackspaceConfirmDeletesComment(): void {
            const countAtBeginning = control.count;

            keyPress(Qt.Key_Backspace);
            testCase.waitUntilMessageBoxOpened(control);
            _expect.isNotHandlingKeyEvents(control);
            keyPress(Qt.Key_Tab);
            keyPress(Qt.Key_Return);

            _expect.hasEventuallyCount(control, countAtBeginning - 1);
            _expect.hasCurrentIndex(control, 2);
        }

        function test_keyPressDeleteConfirmDeletesComment(): void {
            const countAtBeginning = control.count;

            keyPress(Qt.Key_Delete);
            testCase.waitUntilMessageBoxOpened(control);
            keyPress(Qt.Key_Tab);
            keyPress(Qt.Key_Return);

            _expect.hasEventuallyCount(control, countAtBeginning - 1);
            _expect.hasCurrentIndex(control, 2);
        }

        function test_keyPressDeleteCancelKeepsComment(): void {
            const countAtBeginning = control.count;

            keyPress(Qt.Key_Delete);
            testCase.waitUntilMessageBoxOpened(control);
            keyPress(Qt.Key_Return);

            testCase.waitUntilMessageBoxClosed(control);
            _expect.hasCount(control, countAtBeginning);
            _expect.hasCurrentIndex(control, 2);
        }

        function test_messageBoxCanBeReopened(): void {
            keyPress(Qt.Key_Delete);
            testCase.waitUntilMessageBoxOpened(control);
            _expect.hasMessageBoxOpen(control);

            keyPress(Qt.Key_Return); // cancel
            testCase.waitUntilMessageBoxClosed(control);
            _expect.hasMessageBoxClosed(control);

            keyPress(Qt.Key_Delete);
            testCase.waitUntilMessageBoxOpened(control);
            _expect.hasMessageBoxOpen(control);
        }

        function test_importClosesMessageBox(): void {
            const countAtBeginning = control.count;

            keyPress(Qt.Key_Delete);
            testCase.waitUntilMessageBoxOpened(control);
            _expect.hasMessageBoxOpen(control);

            control.model.import_comments([
                {
                    "time": 99,
                    "commentType": "Comment Type 1",
                    "comment": "Imported"
                },
            ]);

            testCase.waitUntilMessageBoxClosed(control);
            _expect.hasMessageBoxClosed(control);
            _expect.hasCount(control, countAtBeginning + 1);
            _expect.hasActiveFocus(control);
        }

        function test_sequentialDeleteRemovesConsecutiveRows(): void {
            const countAtBeginning = control.count;

            _expect.hasItemComment(control, 2, "Comment 3");

            keyPress(Qt.Key_Delete);
            testCase.waitUntilMessageBoxOpened(control);
            keyPress(Qt.Key_Tab);
            keyPress(Qt.Key_Return);
            _expect.hasEventuallyCount(control, countAtBeginning - 1);
            _expect.hasCurrentIndex(control, 2);

            testCase.waitUntilMessageBoxClosed(control);
            _expect.hasItemComment(control, 2, "Comment 4");

            keyPress(Qt.Key_Delete);
            testCase.waitUntilMessageBoxOpened(control);
            keyPress(Qt.Key_Tab);
            keyPress(Qt.Key_Return);
            _expect.hasEventuallyCount(control, countAtBeginning - 2);
            _expect.hasCurrentIndex(control, 2);

            _expect.hasItemComment(control, 2, "Comment 5");
        }

        function test_keyPressCtrlPlusCCopiesToClipboard(): void {
            const spy = createTemporaryObject(signalSpy, control, {
                target: control.viewModel,
                signalName: "copiedToClipboard"
            });
            verify(spy);

            keyPress(Qt.Key_C, Qt.ControlModifier);

            tryVerify(() => spy.count === 1);
            compare(spy.signalArguments[0][0], "[00:00:03] [Comment Type 3] Comment 3");
        }

        function test_keyPressCtrlPlusFOpensSearch(): void {
            _expect.hasSearchBoxClosed(control);
            keyPress(Qt.Key_F, Qt.ControlModifier);
            testCase.waitUntilSearchBoxOpened(control);
            _expect.hasSearchBoxOpen(control);
        }

        function test_keyPressCtrlPlusShiftPlusZUndoRedo(): void {
            const countAtBeginning = control.count;
            keyPress(Qt.Key_Z, Qt.ControlModifier); // undo import
            _expect.hasEventuallyCount(control, 0);
            keyPress(Qt.Key_Z, Qt.ControlModifier | Qt.ShiftModifier); // redo import
            _expect.hasEventuallyCount(control, countAtBeginning);
        }

        function test_addRowJumpsToRowAndOpensEditor(): void {
            const countBefore = control.count;
            control.viewModel.addRow("Comment Type 1"); // time=0 in test env → sorts to index 0
            _expect.hasCount(control, countBefore + 1);
            testCase.waitUntilEditControlOpened(control);
            _expect.isEditing(control);
            _expect.isEditorShowingCommentPopup(control);
            _expect.hasCurrentIndex(control, 0);
        }

        function test_undoClearSelectsLastRow(): void {
            const countBeforeClear = control.count;
            control.model.clear_comments();
            _expect.hasEventuallyCount(control, 0);
            keyPress(Qt.Key_Z, Qt.ControlModifier); // undo clear
            _expect.hasEventuallyCount(control, countBeforeClear);
            _expect.hasCurrentIndex(control, control.count - 1);
        }

        function test_unknownCommentTypeAppearsInEditMenu(): void {
            control.model.import_comments([
                {
                    "time": 10,
                    "commentType": "Legacy Type",
                    "comment": "Old"
                },
            ]);
            waitForRendering(control);

            const pt = _clickHelper.centerOfCommentTypeLabel(control, control.count - 1);
            testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
            testCase.waitUntilEditControlOpened(control);

            const legacyItem = testCase.getCommentTypeItems(control).find(item => item.commentType === "Legacy Type");
            verify(legacyItem);
            verify(legacyItem.checked);
        }
    }

    TestCase {
        name: "MpvqcCommentList::EditingTime"

        property var control: null

        function initTestCase(): void {
            testCase.initTestCase();
        }

        function init(): void {
            control = testCase.makeControl();
            control.currentIndex = 2;
            waitForRendering(control);
            const pt = _clickHelper.centerOfTimeLabel(control, 2);
            testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
            testCase.waitUntilEditControlOpened(control);
            _expect.isEditing(control);
            _expect.isNotInteractive(control);
            _expect.isEditorShowingTimePopup(control);
            _expect.hasCurrentIndex(control, 2);
        }

        function cleanup(): void {
            control.destroy();
            control = null;
        }

        function test_singleClick_data(): list<var> {
            return [
                {
                    tag: "selected-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-label",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-comment-label",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 1),
                    expectedIndex: 2
                },
            ];
        }

        function test_singleClick(data): void {
            _expect.hasItemTime(control, 2, 3);
            _clickHelper.clickDecrementButton(control);
            const pt = data.clickPoint(control);
            testCase.mouseClick(control, pt.x, pt.y);
            testCase.waitUntilEditControlClosed(control);
            _expect.hasItemTime(control, 2, 2);
            _expect.hasCurrentIndex(control, data.expectedIndex);
            _expect.isNotEditing(control);
        }

        function test_doubleClick_data(): list<var> {
            return [
                {
                    tag: "selected-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-label",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-comment-label",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 1),
                    expectedIndex: 2
                },
            ];
        }

        function test_doubleClick(data): void {
            _expect.hasItemTime(control, 2, 3);
            _clickHelper.clickDecrementButton(control);
            const pt = data.clickPoint(control);
            testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
            testCase.waitUntilEditControlClosed(control);
            _expect.hasItemTime(control, 2, 2);
            _expect.hasCurrentIndex(control, data.expectedIndex);
            _expect.isNotEditing(control);
        }

        function test_rightClick_data(): list<var> {
            return [
                {
                    tag: "selected-row",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 2)
                },
                {
                    tag: "other-row",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 1)
                },
            ];
        }

        function test_rightClick(data): void {
            _expect.hasItemTime(control, 2, 3);
            _clickHelper.clickDecrementButton(control);
            const pt = data.clickPoint(control);
            testCase.mouseClick(control, pt.x, pt.y, Qt.RightButton);
            testCase.waitUntilEditControlClosed(control);
            _expect.hasItemTime(control, 2, 2);
            _expect.hasCurrentIndex(control, 2);
            _expect.hasContextMenuClosed(control);
            _expect.isNotEditing(control);
        }

        function test_keyEventsAreNotHandled(): void {
            _expect.isNotHandlingKeyEvents(control);
        }

        function test_playButtonDoesNotJumpToTime(): void {
            const timeBefore = control.viewModel.lastJumpToTime;
            const pt = _clickHelper.centerOfPlayButton(control, 2);
            testCase.mouseClick(control, pt.x, pt.y);
            _expect.hasLastJumpedToTime(control, timeBefore);
        }

        function test_decrementsTime_data(): list<var> {
            return [
                {
                    tag: "button",
                    action: c => _clickHelper.clickDecrementButton(c)
                },
                {
                    tag: "key-left",
                    action: c => keyPress(Qt.Key_Left)
                },
                {
                    tag: "key-down",
                    action: c => keyPress(Qt.Key_Down)
                },
                {
                    tag: "scroll-wheel",
                    action: c => {
                        const sb = _find.timeSpinBox(c);
                        mouseWheel(sb, sb.width / 2, sb.height / 2, 0, -120);
                    }
                },
            ];
        }

        function test_decrementsTime(data): void {
            _expect.hasItemTime(control, 2, 3);
            data.action(control);
            _expect.hasLastJumpedToTime(control, 2);
            const pt = _clickHelper.topRightOfCommentLabel(control, 2);
            testCase.mouseClick(control, pt.x, pt.y);
            testCase.waitUntilEditControlClosed(control);
            _expect.isNotEditing(control);
            _expect.hasItemTime(control, 2, 2);
        }

        function test_incrementsTime_data(): list<var> {
            return [
                {
                    tag: "button",
                    action: c => _clickHelper.clickIncrementButton(c)
                },
                {
                    tag: "key-right",
                    action: c => keyPress(Qt.Key_Right)
                },
                {
                    tag: "key-up",
                    action: c => keyPress(Qt.Key_Up)
                },
                {
                    tag: "scroll-wheel",
                    action: c => {
                        const sb = _find.timeSpinBox(c);
                        mouseWheel(sb, sb.width / 2, sb.height / 2, 0, 120);
                    }
                },
            ];
        }

        function test_incrementsTime(data): void {
            _expect.hasItemTime(control, 2, 3);
            data.action(control);
            _expect.hasLastJumpedToTime(control, 4);
            const pt = _clickHelper.topRightOfCommentLabel(control, 2);
            testCase.mouseClick(control, pt.x, pt.y);
            testCase.waitUntilEditControlClosed(control);
            _expect.isNotEditing(control);
            _expect.hasItemTime(control, 2, 4);
        }

        function test_escapeAbortsEdit(): void {
            _expect.hasItemTime(control, 2, 3);
            _clickHelper.clickDecrementButton(control);
            _expect.hasLastJumpedToTime(control, 2);
            keyPress(Qt.Key_Escape);
            testCase.waitUntilEditControlClosed(control);
            _expect.isNotEditing(control);
            _expect.hasItemTime(control, 2, 3);
            _expect.hasLastJumpedToTime(control, 3);
            _expect.hasActiveFocus(control);
        }

        function test_importAbortsEdit(): void {
            _expect.hasItemTime(control, 2, 3);
            _clickHelper.clickDecrementButton(control);
            _expect.hasLastJumpedToTime(control, 2);

            control.model.import_comments([
                {
                    "time": 99,
                    "commentType": "Comment Type 1",
                    "comment": "Imported"
                },
            ]);
            testCase.waitUntilEditControlClosed(control);

            _expect.isNotEditing(control);
            _expect.hasItemTime(control, 2, 3);
            _expect.hasLastJumpedToTime(control, 3);
            _expect.hasActiveFocus(control);
        }

        function test_decrementClampsAtZero(): void {
            for (let expected = 2; expected >= 0; expected--) {
                keyPress(Qt.Key_Down);
                _expect.hasLastJumpedToTime(control, expected);
            }
            keyPress(Qt.Key_Down);
            _expect.hasLastJumpedToTime(control, 0);
        }

        function test_incrementClampsAtVideoDuration(): void {
            const duration = control.viewModel.videoDuration;
            for (let expected = 4; expected <= duration; expected++) {
                keyPress(Qt.Key_Up);
                _expect.hasLastJumpedToTime(control, expected);
            }
            keyPress(Qt.Key_Up);
            _expect.hasLastJumpedToTime(control, duration);
        }

        function test_timeEditReordersAndSelectionFollows(): void {
            _expect.hasCurrentIndex(control, 2);
            _expect.hasItemTime(control, 2, 3);

            keyPress(Qt.Key_Up);
            _expect.hasLastJumpedToTime(control, 4);
            keyPress(Qt.Key_Up);
            _expect.hasLastJumpedToTime(control, 5);
            keyPress(Qt.Key_Up);
            _expect.hasLastJumpedToTime(control, 6);

            const pt = _clickHelper.topRightOfCommentLabel(control, 2);
            testCase.mouseClick(control, pt.x, pt.y);
            testCase.waitUntilEditControlClosed(control);
            _expect.isNotEditing(control);

            tryVerify(() => control.currentIndex === 4);
            _expect.hasItemComment(control, 4, "Comment 3");
        }
    }

    TestCase {
        name: "MpvqcCommentList::EditingCommentType"

        property var control: null

        function initTestCase(): void {
            testCase.initTestCase();
        }

        function init(): void {
            control = testCase.makeControl();
            control.currentIndex = 2;
            waitForRendering(control);
            const pt = _clickHelper.centerOfCommentTypeLabel(control, 2);
            testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
            testCase.waitUntilEditControlOpened(control);
            _expect.isEditing(control);
            _expect.isNotInteractive(control);
            _expect.isEditorShowingCommentTypeMenu(control);
            _expect.hasCurrentIndex(control, 2);
        }

        function cleanup(): void {
            control.destroy();
            control = null;
        }

        function test_singleClick_data(): list<var> {
            return [
                {
                    tag: "selected-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-label",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-comment-label",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 1),
                    expectedIndex: 2
                },
            ];
        }

        function test_singleClick(data): void {
            const currentValue = control.getItem(2, "commentType");
            const pt = data.clickPoint(control);
            testCase.mouseClick(control, pt.x, pt.y);
            testCase.waitUntilEditControlClosed(control);
            _expect.hasItemCommentType(control, 2, currentValue);
            _expect.hasCurrentIndex(control, data.expectedIndex);
            _expect.isNotEditing(control);
        }

        function test_doubleClick_data(): list<var> {
            return [
                {
                    tag: "selected-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-label",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-comment-label",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 1),
                    expectedIndex: 2
                },
            ];
        }

        function test_doubleClick(data): void {
            const currentValue = control.getItem(2, "commentType");
            const pt = data.clickPoint(control);
            testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
            testCase.waitUntilEditControlClosed(control);
            _expect.hasItemCommentType(control, 2, currentValue);
            _expect.hasCurrentIndex(control, data.expectedIndex);
            _expect.isNotEditing(control);
        }

        function test_rightClick_data(): list<var> {
            return [
                {
                    tag: "selected-row",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 2)
                },
                {
                    tag: "other-row",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 1)
                },
            ];
        }

        function test_rightClick(data): void {
            const currentValue = control.getItem(2, "commentType");
            const pt = data.clickPoint(control);
            testCase.mouseClick(control, pt.x, pt.y, Qt.RightButton);
            testCase.waitUntilEditControlClosed(control);
            _expect.hasItemCommentType(control, 2, currentValue);
            _expect.hasCurrentIndex(control, 2);
            _expect.hasContextMenuClosed(control);
            _expect.isNotEditing(control);
        }

        function test_keyEventsAreNotHandled(): void {
            _expect.isNotHandlingKeyEvents(control);
        }

        function test_playButtonDoesNotJumpToTime(): void {
            const timeBefore = control.viewModel.lastJumpToTime;
            const pt = _clickHelper.centerOfPlayButton(control, 2);
            testCase.mouseClick(control, pt.x, pt.y);
            _expect.hasLastJumpedToTime(control, timeBefore);
        }

        function test_selectTypeSavesNewType(): void {
            _expect.hasItemCommentType(control, 2, "Comment Type 3");
            _clickHelper.clickCommentTypeMenuItem(control, "Comment Type 5");
            testCase.waitUntilEditControlClosed(control);
            _expect.isNotEditing(control);
            _expect.hasItemCommentType(control, 2, "Comment Type 5");
        }

        function test_escapeAbortsEdit(): void {
            _expect.hasItemCommentType(control, 2, "Comment Type 3");
            keyPress(Qt.Key_Escape);
            testCase.waitUntilEditControlClosed(control);
            _expect.isNotEditing(control);
            _expect.hasItemCommentType(control, 2, "Comment Type 3");
            _expect.hasActiveFocus(control);
        }

        function test_importAbortsEdit(): void {
            _expect.hasItemCommentType(control, 2, "Comment Type 3");

            control.model.import_comments([
                {
                    "time": 99,
                    "commentType": "Comment Type 1",
                    "comment": "Imported"
                },
            ]);

            testCase.waitUntilEditControlClosed(control);
            _expect.isNotEditing(control);
            _expect.hasItemCommentType(control, 2, "Comment Type 3");
            _expect.hasActiveFocus(control);
        }
    }

    TestCase {
        name: "MpvqcCommentList::EditingComment"

        property var control: null

        function initTestCase(): void {
            testCase.initTestCase();
        }

        function init(): void {
            control = testCase.makeControl();
            control.currentIndex = 2;
            waitForRendering(control);
            const pt = _clickHelper.centerOfCommentLabel(control, 2);
            testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
            testCase.waitUntilEditControlOpened(control);
            _expect.isEditing(control);
            _expect.isNotInteractive(control);
            _expect.isEditorShowingCommentPopup(control);
            _expect.hasCurrentIndex(control, 2);
        }

        function cleanup(): void {
            control.destroy();
            control = null;
        }

        function test_editorOpensWithCurrentCommentSelectedAndReady(): void {
            const textField = _find.commentTextArea(control);
            compare(textField.text, "Comment 3");
            compare(textField.selectedText, "Comment 3");
        }

        function test_singleClick_data(): list<var> {
            return [
                {
                    tag: "selected-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 1),
                    expectedIndex: 1
                },
                {
                    tag: "other-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 1),
                    expectedIndex: 1
                },
                {
                    tag: "other-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 1),
                    expectedIndex: 1
                },
                {
                    tag: "other-row-comment-label",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 1),
                    expectedIndex: 1
                },
            ];
        }

        function test_singleClick(data): void {
            const editedValue = "edited";
            typeWord(editedValue);
            const pt = data.clickPoint(control);
            testCase.mouseClick(control, pt.x, pt.y);
            testCase.waitUntilEditControlClosed(control);
            _expect.hasItemComment(control, 2, editedValue);
            _expect.hasCurrentIndex(control, data.expectedIndex);
            _expect.isNotEditing(control);
        }

        function test_doubleClick_data(): list<var> {
            return [
                {
                    tag: "selected-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 2),
                    expectedIndex: 2,
                    expectedSource: c => null
                },
                {
                    tag: "selected-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 2),
                    expectedIndex: 2,
                    expectedSource: c => c.editLoader.editTimePopup
                },
                {
                    tag: "selected-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 2),
                    expectedIndex: 2,
                    expectedSource: c => c.editLoader.editCommentTypeMenu
                },
                {
                    tag: "other-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 1),
                    expectedIndex: 1,
                    expectedSource: c => null
                },
                {
                    tag: "other-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 1),
                    expectedIndex: 1,
                    expectedSource: c => c.editLoader.editTimePopup
                },
                {
                    tag: "other-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 1),
                    expectedIndex: 1,
                    expectedSource: c => c.editLoader.editCommentTypeMenu
                },
            ];
        }

        function test_doubleClick(data): void {
            const editedValue = "edited";
            typeWord(editedValue);
            const pt = data.clickPoint(control);
            testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
            testCase.waitUntilEventsProcessed();
            _expect.hasItemComment(control, 2, editedValue);
            _expect.hasCurrentIndex(control, data.expectedIndex);
            const expectedSrc = data.expectedSource(control);
            if (expectedSrc) {
                compare(control.editLoader.source, expectedSrc);
            }
            expectedSrc ? _expect.isEditing(control) : _expect.isNotEditing(control);
        }

        // Ticket #248: Comment line text disappears when switching lines via double-click while editing
        function test_doubleClickOtherRowCommentLabel(): void {
            const editedValue = "edited";
            typeWord(editedValue);

            const ptRow1 = _clickHelper.topRightOfCommentLabel(control, 1);
            testCase.mouseDoubleClickSequence(control, ptRow1.x, ptRow1.y);
            testCase.waitUntilEditControlOpened(control);

            compare(control.getItem(2, "comment"), editedValue);
            testCase.waitUntilEventsProcessed();

            // Verify editing is still active even after timeout
            _expect.isEditing(control);
            verify(control.editLoader.item);
            _expect.hasCurrentIndex(control, 1);
            // Verify content in editing mode is correct
            compare(control.editLoader.item.textField.text, "Comment 2");
            // Verify text below the editing popup is empty
            compare(control.itemAtIndex(1).commentLabel.text, "");

            const ptRow0 = _clickHelper.topRightOfCommentLabel(control, 0);
            testCase.mouseClick(control, ptRow0.x, ptRow0.y);

            // Verify text is displayed again
            tryCompare(control.itemAtIndex(1).commentLabel, "text", "Comment 2");
        }

        function test_rightClick_data(): list<var> {
            return [
                {
                    tag: "selected-row",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 2)
                },
                {
                    tag: "other-row",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 1)
                },
            ];
        }

        function test_rightClick(data): void {
            const editedValue = "edited";
            typeWord(editedValue);
            const pt = data.clickPoint(control);
            testCase.mouseClick(control, pt.x, pt.y, Qt.RightButton);
            testCase.waitUntilEditControlClosed(control);
            waitUntilEventsProcessed();
            _expect.hasItemComment(control, 2, editedValue);
            _expect.hasCurrentIndex(control, 2);
            _expect.hasContextMenuClosed(control);
            _expect.isNotEditing(control);
        }

        function test_keyEventsAreNotHandled(): void {
            _expect.isNotHandlingKeyEvents(control);
        }

        function test_playButtonDoesNotJumpToTime(): void {
            const timeBefore = control.viewModel.lastJumpToTime;
            const pt = _clickHelper.centerOfPlayButton(control, 2);
            testCase.mouseClick(control, pt.x, pt.y);
            _expect.hasLastJumpedToTime(control, timeBefore);
        }

        function test_arrowKeysDoNotChangeRow_data(): list<var> {
            return [
                {
                    tag: "up",
                    key: Qt.Key_Up
                },
                {
                    tag: "down",
                    key: Qt.Key_Down
                },
            ];
        }

        function test_arrowKeysDoNotChangeRow(data): void {
            _expect.hasCurrentIndex(control, 2);
            keyPress(data.key);
            _expect.hasCurrentIndex(control, 2);
            _expect.isEditing(control);
        }

        function test_selectOtherRowCommitsEdit(): void {
            const editedValue = "edited";
            typeWord(editedValue);
            const pt = _clickHelper.topRightOfCommentLabel(control, 1);
            testCase.mouseClick(control, pt.x, pt.y);
            testCase.waitUntilEditControlClosed(control);
            _expect.hasItemComment(control, 2, editedValue);
            _expect.hasCurrentIndex(control, 1);
            _expect.isNotEditing(control);
        }

        function test_returnCommitsComment(): void {
            const editedValue = "edited";
            typeWord(editedValue);
            keyPress(Qt.Key_Return);
            testCase.waitUntilEditControlClosed(control);
            _expect.hasItemComment(control, 2, editedValue);
            _expect.hasCurrentIndex(control, 2);
            _expect.isNotEditing(control);
        }

        function test_returnCommitsCommentUnchanged(): void {
            const currentValue = control.getItem(2, "comment");
            keyPress(Qt.Key_Return);
            testCase.waitUntilEditControlClosed(control);
            _expect.hasItemComment(control, 2, currentValue);
            _expect.hasCurrentIndex(control, 2);
            _expect.isNotEditing(control);
        }

        function test_escapeAbortsEdit(): void {
            const currentValue = control.getItem(2, "comment");
            typeWord("edited");
            keyPress(Qt.Key_Escape);
            testCase.waitUntilEditControlClosed(control);
            _expect.hasItemComment(control, 2, currentValue);
            _expect.hasCurrentIndex(control, 2);
            _expect.isNotEditing(control);
        }

        function test_focusLossCommitsEdit(): void {
            const editedValue = "edited";
            typeWord(editedValue);
            control.forceActiveFocus(); // ideally simulate click outside the window
            testCase.waitUntilEditControlClosed(control);
            _expect.hasItemComment(control, 2, editedValue);
            _expect.hasCurrentIndex(control, 2);
            _expect.isNotEditing(control);
        }

        function test_editorCanBeReopened(): void {
            keyPress(Qt.Key_Escape);
            testCase.waitUntilEditControlClosed(control);
            _expect.isNotEditing(control);

            keyPress(Qt.Key_Return);
            testCase.waitUntilEditControlOpened(control);
            _expect.isEditing(control);
        }
    }

    TestCase {
        name: "MpvqcCommentList::ContextMenu"

        property var control: null

        function initTestCase(): void {
            testCase.initTestCase();
        }

        function init(): void {
            control = testCase.makeControl();
            control.currentIndex = 2;
            waitForRendering(control);
            const pt = _clickHelper.topLeftOfCommentLabel(control, 2);
            testCase.mouseClick(control, pt.x, pt.y, Qt.RightButton);
            testCase.waitUntilContextMenuOpened(control);
            _expect.isNotEditing(control);
            _expect.hasCurrentIndex(control, 2);
        }

        function cleanup(): void {
            control.destroy();
            control = null;
        }

        function test_singleClick_data(): list<var> {
            return [
                {
                    tag: "selected-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-label",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-comment-label",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 1),
                    expectedIndex: 2
                },
            ];
        }

        function test_singleClick(data): void {
            const pt = data.clickPoint(control);
            testCase.mouseClick(control, pt.x, pt.y);
            testCase.waitUntilContextMenuClosed(control);
            _expect.hasCurrentIndex(control, data.expectedIndex);
            _expect.isNotEditing(control);
            _expect.hasContextMenuClosed(control);
        }

        function test_doubleClick_data(): list<var> {
            return [
                {
                    tag: "selected-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "selected-row-comment-label",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-play-button",
                    clickPoint: c => _clickHelper.topRightOfPlayButton(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-time-label",
                    clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-comment-type-label",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 1),
                    expectedIndex: 2
                },
                {
                    tag: "other-row-comment-label",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 1),
                    expectedIndex: 2
                },
            ];
        }

        function test_doubleClick(data): void {
            const pt = data.clickPoint(control);
            testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
            testCase.waitUntilContextMenuClosed(control);
            _expect.hasCurrentIndex(control, data.expectedIndex);
            _expect.isNotEditing(control);
            _expect.hasContextMenuClosed(control);
        }

        function test_rightClick_data(): list<var> {
            return [
                {
                    tag: "selected-row",
                    clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 2),
                    expectedIndex: 2
                },
                {
                    tag: "other-row",
                    clickPoint: c => _clickHelper.topRightOfCommentLabel(c, 1),
                    expectedIndex: 2
                },
            ];
        }

        function test_rightClick(data): void {
            const pt = data.clickPoint(control);
            testCase.mouseClick(control, pt.x, pt.y, Qt.RightButton);
            testCase.waitUntilContextMenuClosed(control);
            _expect.hasCurrentIndex(control, data.expectedIndex);
            _expect.isNotEditing(control);
            _expect.hasContextMenuClosed(control);
        }

        function test_keyEventsAreNotHandled(): void {
            _expect.isNotHandlingKeyEvents(control);
        }

        function test_selectEditComment(): void {
            _clickHelper.clickEditCommentAction(control);
            testCase.waitUntilContextMenuClosed(control);
            testCase.waitUntilEditControlOpened(control);
            _expect.isEditing(control);
            _expect.hasContextMenuClosed(control);
        }

        function test_selectCopyToClipboard(): void {
            const spy = createTemporaryObject(signalSpy, control, {
                target: control.viewModel,
                signalName: "copiedToClipboard"
            });
            verify(spy);

            _clickHelper.clickCopyCommentAction(control);
            testCase.waitUntilContextMenuClosed(control);
            _expect.hasContextMenuClosed(control);

            tryVerify(() => spy.count === 1);
            compare(spy.signalArguments[0][0], "[00:00:03] [Comment Type 3] Comment 3");
            _expect.isNotEditing(control);
        }

        function test_selectDeleteComment(): void {
            const countAtBeginning = control.count;
            _clickHelper.clickDeleteCommentAction(control);
            testCase.waitUntilMessageBoxOpened(control);
            _expect.hasContextMenuClosed(control);

            keyPress(Qt.Key_Tab);
            keyPress(Qt.Key_Return);

            tryVerify(() => control.count === countAtBeginning - 1);
        }

        function test_escapeClosesMenu(): void {
            keyPress(Qt.Key_Escape);

            testCase.waitUntilContextMenuClosed(control);
            _expect.hasCurrentIndex(control, 2);
            _expect.isNotEditing(control);
            _expect.hasContextMenuClosed(control);
        }

        function test_contextMenuCanBeReopened(): void {
            keyPress(Qt.Key_Escape);
            testCase.waitUntilContextMenuClosed(control);
            _expect.hasContextMenuClosed(control);
            _expect.hasActiveFocus(control);

            const pt = _clickHelper.centerOfCommentLabel(control, 2);
            testCase.mouseClick(control, pt.x, pt.y, Qt.RightButton);
            testCase.waitUntilContextMenuOpened(control);
            _expect.hasContextMenuOpen(control);

            keyPress(Qt.Key_Escape);
            testCase.waitUntilContextMenuClosed(control);
            _expect.hasContextMenuClosed(control);
            _expect.hasActiveFocus(control);
        }

        function test_importClosesContextMenu(): void {
            _expect.hasContextMenuOpen(control);

            control.model.import_comments([
                {
                    "time": 99,
                    "commentType": "Comment Type 1",
                    "comment": "Imported"
                },
            ]);

            testCase.waitUntilContextMenuClosed(control);
            _expect.hasContextMenuClosed(control);
            _expect.hasActiveFocus(control);
        }
    }

    TestCase {
        name: "MpvqcCommentList::SearchBox"

        property var control: null

        function initTestCase(): void {
            testCase.initTestCase();
        }

        function init(): void {
            control = testCase.makeControl();
            control.currentIndex = 0;
            waitForRendering(control);

            control.model.import_comments([
                {
                    "time": 0,
                    "commentType": "Comment Type 1",
                    "comment": "needs review"
                },
                {
                    "time": 3,
                    "commentType": "Comment Type 2",
                    "comment": "please review this"
                },
                {
                    "time": 6,
                    "commentType": "Comment Type 3",
                    "comment": "review again"
                },
            ]);
            waitForRendering(control);

            keyPress(Qt.Key_F, Qt.ControlModifier);
            testCase.waitUntilSearchBoxOpened(control);
            _expect.hasSearchBoxOpen(control);
        }

        function cleanup(): void {
            control.destroy();
            control = null;
        }

        function _reviewRows(): list<int> {
            const comments = control.model.comments();
            return comments.map((_c, i) => i).filter(i => comments[i].comment.includes("review"));
        }

        function test_selectNext_data(): list<var> {
            return [
                {
                    tag: "return",
                    action: _c => keyPress(Qt.Key_Return),
                    expected: [
                        {
                            index: 1,
                            label: "2/3"
                        }
                    ]
                },
                {
                    tag: "down",
                    action: _c => keyPress(Qt.Key_Down),
                    expected: [
                        {
                            index: 1,
                            label: "2/3"
                        }
                    ]
                },
                {
                    tag: "next-button",
                    action: c => _clickHelper.clickSearchNextButton(c),
                    expected: [
                        {
                            index: 1,
                            label: "2/3"
                        }
                    ]
                },
                {
                    tag: "wraps-forward",
                    action: _c => keyPress(Qt.Key_Return),
                    expected: [
                        {
                            index: 1,
                            label: "2/3"
                        },
                        {
                            index: 2,
                            label: "3/3"
                        },
                        {
                            index: 0,
                            label: "1/3"
                        },
                    ]
                },
            ];
        }

        function test_selectNext(data): void {
            const reviewRows = _reviewRows();
            const statusLabel = _find.searchStatusLabel(control);

            typeWord("review");
            tryVerify(() => control.currentIndex === reviewRows[0]);
            compare(statusLabel.text, "1/3");

            for (const step of data.expected) {
                data.action(control);
                tryVerify(() => control.currentIndex === reviewRows[step.index]);
                compare(statusLabel.text, step.label);
            }
        }

        function test_selectPrevious_data(): list<var> {
            return [
                {
                    tag: "shift-return",
                    action: _c => keyPress(Qt.Key_Return, Qt.ShiftModifier),
                    expected: [
                        {
                            index: 2,
                            label: "3/3"
                        }
                    ]
                },
                {
                    tag: "up",
                    action: _c => keyPress(Qt.Key_Up),
                    expected: [
                        {
                            index: 2,
                            label: "3/3"
                        }
                    ]
                },
                {
                    tag: "prev-button",
                    action: c => _clickHelper.clickSearchPreviousButton(c),
                    expected: [
                        {
                            index: 2,
                            label: "3/3"
                        }
                    ]
                },
                {
                    tag: "wraps-backward",
                    action: _c => keyPress(Qt.Key_Return, Qt.ShiftModifier),
                    expected: [
                        {
                            index: 2,
                            label: "3/3"
                        },
                        {
                            index: 1,
                            label: "2/3"
                        },
                        {
                            index: 0,
                            label: "1/3"
                        },
                        {
                            index: 2,
                            label: "3/3"
                        },
                    ]
                },
            ];
        }

        function test_selectPrevious(data): void {
            const reviewRows = _reviewRows();
            const statusLabel = _find.searchStatusLabel(control);

            typeWord("review");
            tryVerify(() => control.currentIndex === reviewRows[0]);
            compare(statusLabel.text, "1/3");

            for (const step of data.expected) {
                data.action(control);
                tryVerify(() => control.currentIndex === reviewRows[step.index]);
                compare(statusLabel.text, step.label);
            }
        }

        function test_close_data(): list<var> {
            return [
                {
                    tag: "escape",
                    action: _c => keyPress(Qt.Key_Escape)
                },
                {
                    tag: "close-button",
                    action: c => _clickHelper.clickSearchCloseButton(c)
                },
            ];
        }

        function test_close(data): void {
            data.action(control);

            testCase.waitUntilSearchBoxClosed(control);
            _expect.hasSearchBoxClosed(control);
            _expect.isEventuallySearchBoxClosed(control);
            _expect.hasActiveFocus(control);
        }

        function test_search_highlightFocusAndRestore(): void {
            typeWord("review");

            tryVerify(() => control.searchBoxLoader.searchQuery === "review");

            const delegate = control.itemAtIndex(control.currentIndex);
            const commentLabel = _find.commentLabel(delegate);
            tryVerify(() => commentLabel.text.includes("<b><u>"));

            keyPress(Qt.Key_Escape);
            testCase.waitUntilSearchBoxClosed(control);
            _expect.hasSearchBoxClosed(control);
            tryVerify(() => !commentLabel.text.includes("<b><u>"));

            _expect.isEventuallySearchBoxClosed(control);
            _expect.hasActiveFocus(control);

            keyPress(Qt.Key_F, Qt.ControlModifier);
            testCase.waitUntilSearchBoxOpened(control);
            _expect.hasSearchBoxOpen(control);

            tryVerify(() => commentLabel.text.includes("<b><u>"));
        }

        function test_zeroResults(): void {
            const statusLabel = _find.searchStatusLabel(control);
            const prevButton = _find.searchPreviousButton(control);
            const nextButton = _find.searchNextButton(control);

            typeWord("nomatch");

            tryVerify(() => statusLabel.text === "0/0");
            verify(!prevButton.enabled);
            verify(!nextButton.enabled);
        }

        function test_deleteKeyDoesNotOpenMessageBox(): void {
            typeWord("review");
            keyPress(Qt.Key_Delete);
            _expect.hasMessageBoxClosed(control);
            _expect.hasSearchBoxOpen(control);

            const textField = _find.searchTextField(control);
            tryVerify(() => textField.activeFocus);
        }

        function test_rightClickOpensContextMenuThenEscapeClosesMenuThenSearch(): void {
            typeWord("review");
            tryVerify(() => control.currentIndex === _reviewRows()[0]);

            const pt = _clickHelper.centerOfCommentLabel(control, control.currentIndex);
            testCase.mouseClick(control, pt.x, pt.y, Qt.RightButton);
            testCase.waitUntilContextMenuOpened(control);
            _expect.hasContextMenuOpen(control);
            _expect.hasSearchBoxOpen(control);

            keyPress(Qt.Key_Escape);
            testCase.waitUntilContextMenuClosed(control);
            _expect.hasContextMenuClosed(control);
            _expect.isEventuallySearchBoxOpen(control);
            _expect.hasActiveFocus(control);

            keyPress(Qt.Key_Escape);
            testCase.waitUntilSearchBoxClosed(control);
            _expect.hasSearchBoxClosed(control);
            _expect.isEventuallySearchBoxClosed(control);
            _expect.hasActiveFocus(control);
        }

        function test_ctrlFWhileOpenRefocusesAndSelectsText(): void {
            typeWord("review");
            tryVerify(() => control.searchBoxLoader.searchQuery === "review");

            const textField = _find.searchTextField(control);

            control.forceActiveFocus();
            tryVerify(() => !textField.activeFocus);

            keyPress(Qt.Key_F, Qt.ControlModifier);

            tryVerify(() => textField.activeFocus);
            compare(textField.selectedText, "review");
        }

        function test_escapeClosesEditorThenSearch(): void {
            const reviewRows = _reviewRows();

            typeWord("review");
            tryVerify(() => control.currentIndex === reviewRows[0]);

            const pt = _clickHelper.centerOfCommentLabel(control, control.currentIndex);
            testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
            testCase.waitUntilEditControlOpened(control);

            keyPress(Qt.Key_Escape);
            testCase.waitUntilEditControlClosed(control);
            _expect.isEventuallySearchBoxOpen(control);
            testCase.waitUntilEventsProcessed();

            keyPress(Qt.Key_Escape);
            testCase.waitUntilSearchBoxClosed(control);
            _expect.hasSearchBoxClosed(control);
            _expect.isEventuallySearchBoxClosed(control);
            _expect.hasActiveFocus(control);
        }

        function test_searchBoxCanBeReopened(): void {
            keyPress(Qt.Key_Escape);
            testCase.waitUntilSearchBoxClosed(control);
            _expect.hasSearchBoxClosed(control);
            _expect.isEventuallySearchBoxClosed(control);
            _expect.hasActiveFocus(control);

            keyPress(Qt.Key_F, Qt.ControlModifier);
            testCase.waitUntilSearchBoxOpened(control);
            _expect.hasSearchBoxOpen(control);
        }
    }

    TestCase {
        name: "MpvqcCommentList::SearchBoxPosition"
        visible: true
        when: windowShown

        property var control: null

        function initTestCase(): void {
            testCase.initTestCase();
        }

        function init(): void {
            control = testCase.makeControl();
            control.currentIndex = 0;
            waitForRendering(control);

            control.model.import_comments([
                {
                    "time": 0,
                    "commentType": "Comment Type 1",
                    "comment": "some comment"
                },
            ]);
            waitForRendering(control);

            keyPress(Qt.Key_F, Qt.ControlModifier);
            testCase.waitUntilSearchBoxOpened(control);
            _expect.hasSearchBoxOpen(control);
        }

        function cleanup(): void {
            control.destroy();
            control = null;
        }

        function _bottomY(): real {
            const popup = _find.searchBoxPopup(control);
            return control.height - popup.height - popup.edgeMarginVertical;
        }

        function test_initialPositionIsAtBottom(): void {
            const popup = _find.searchBoxPopup(control);
            fuzzyCompare(popup.y, _bottomY(), 1);
        }

        function test_sticksToBottomWhenParentShrinks(): void {
            const popup = _find.searchBoxPopup(control);

            control.height = control.height - 100;
            waitForRendering(control);

            tryVerify(() => Math.abs(popup.y - _bottomY()) <= 1);
        }

        function test_sticksToBottomWhenParentGrows(): void {
            const popup = _find.searchBoxPopup(control);

            control.height = control.height + 100;
            waitForRendering(control);

            tryVerify(() => Math.abs(popup.y - _bottomY()) <= 1);
        }

        function test_sticksToBottomThroughMultipleResizes(): void {
            const popup = _find.searchBoxPopup(control);

            for (const h of [300, 500, 200, 600]) {
                control.height = h;
                waitForRendering(control);
                tryVerify(() => Math.abs(popup.y - _bottomY()) <= 1);
            }
        }

        function test_reopenedAtBottomAfterResize(): void {
            keyPress(Qt.Key_Escape);
            testCase.waitUntilSearchBoxClosed(control);
            _expect.hasActiveFocus(control);

            control.height = 300;
            waitForRendering(control);

            keyPress(Qt.Key_F, Qt.ControlModifier);
            testCase.waitUntilSearchBoxOpened(control);

            const popup = _find.searchBoxPopup(control);
            tryVerify(() => Math.abs(popup.y - _bottomY()) <= 1);
        }

        function test_isDraggable(): void {
            const popup = _find.searchBoxPopup(control);
            const dragArea = _find.searchDragArea(control);
            const initialY = popup.y;

            mouseDrag(dragArea, dragArea.width / 2, dragArea.height / 2, 0, -80);
            waitForRendering(control);

            verify(popup.y < initialY - 20);
        }

        function test_snapsToBottomWhenShrunkPastDragPosition(): void {
            const popup = _find.searchBoxPopup(control);
            const dragArea = _find.searchDragArea(control);

            // Drag the popup away from the bottom
            mouseDrag(dragArea, dragArea.width / 2, dragArea.height / 2, 0, -80);
            waitForRendering(control);
            const draggedY = popup.y;
            verify(draggedY < _bottomY() - 20);

            // Shrink the parent so the popup's dragged position would be out of bounds
            control.height = draggedY + popup.height + popup.edgeMarginVertical - 10;
            waitForRendering(control);

            tryVerify(() => Math.abs(popup.y - _bottomY()) <= 1);
        }

        function test_cursorBehavior_data(): list<var> {
            return [
                {
                    tag: "search-icon",
                    widget: () => _find.searchIconLabel(control),
                    cursorHandler: _widget => testCase.findChild(_find.searchBoxPopup(control), "popupBackgroundCursorHandler"),
                    hoverCursor: Qt.OpenHandCursor,
                    pressCursor: Qt.ClosedHandCursor,
                    scalesOnPress: true
                },
                {
                    tag: "text-field",
                    widget: () => _find.searchTextField(control),
                    cursorHandler: widget => testCase.findChild(widget, "searchTextFieldCursorHandler"),
                    hoverCursor: Qt.IBeamCursor,
                    pressCursor: Qt.IBeamCursor,
                    scalesOnPress: false
                },
                {
                    tag: "status-label",
                    widget: () => _find.searchStatusLabel(control),
                    cursorHandler: _widget => testCase.findChild(_find.searchBoxPopup(control), "popupBackgroundCursorHandler"),
                    hoverCursor: Qt.OpenHandCursor,
                    pressCursor: Qt.ClosedHandCursor,
                    scalesOnPress: true
                },
                {
                    tag: "previous-button-disabled",
                    widget: () => _find.searchPreviousButton(control),
                    cursorHandler: widget => testCase.findChild(widget.parent, "previousButtonDisabledCursorHandler"),
                    hoverCursor: Qt.OpenHandCursor,
                    pressCursor: Qt.ClosedHandCursor,
                    scalesOnPress: true
                },
                {
                    tag: "next-button-disabled",
                    widget: () => _find.searchNextButton(control),
                    cursorHandler: widget => testCase.findChild(widget.parent, "nextButtonDisabledCursorHandler"),
                    hoverCursor: Qt.OpenHandCursor,
                    pressCursor: Qt.ClosedHandCursor,
                    scalesOnPress: true
                },
            ];
        }

        function test_cursorBehavior(data): void {
            const popup = _find.searchBoxPopup(control);
            const dragArea = _find.searchDragArea(control);
            const widget = data.widget();
            const cursorHandler = data.cursorHandler(widget);

            // Map widget center to dragArea coordinates
            const widgetCenter = widget.mapToItem(dragArea, widget.width / 2, widget.height / 2);
            const cx = widgetCenter.x;
            const cy = widgetCenter.y;

            // Hover → expected cursor, no scale
            mouseMove(dragArea, cx, cy);
            compare(cursorHandler.cursorShape, data.hoverCursor, "hover");
            fuzzyCompare(popup.scale, 1, 0.02, "hover-scale");

            // Press → cursor depends on widget, scale depends on widget
            mousePress(dragArea, cx, cy);
            compare(cursorHandler.cursorShape, data.pressCursor, "press");
            if (data.scalesOnPress) {
                tryVerify(() => popup.scale > 1.037, 500, "press-scale-up");
            } else {
                fuzzyCompare(popup.scale, 1, 0.02, "press-no-scale");
            }

            // Release without moving → back to hover cursor and scale 1
            mouseRelease(dragArea, cx, cy);
            compare(cursorHandler.cursorShape, data.hoverCursor, "release");
            if (data.scalesOnPress) {
                tryVerify(() => Math.abs(popup.scale - 1) < 0.01, 500, "release-scale-down");
            }

            // Drag → closed hand throughout, scaled up
            mousePress(dragArea, cx, cy);
            waitForRendering(control);
            compare(cursorHandler.cursorShape, data.pressCursor, "drag-press");

            mouseMove(dragArea, cx, cy - 100);
            waitForRendering(control);
            compare(cursorHandler.cursorShape, Qt.ClosedHandCursor, "drag-move");
            tryVerify(() => popup.scale > 1.037, 500, "drag-scale-up");

            mouseRelease(dragArea, cx, cy - 100);
            compare(cursorHandler.cursorShape, data.hoverCursor, "drag-release");
            tryVerify(() => Math.abs(popup.scale - 1) < 0.01, 2000, "drag-release-scale-down");
        }

        function test_cursorBehaviorNavButtonsEnabled_data(): list<var> {
            return [
                {
                    tag: "previous-button-enabled",
                    widget: () => _find.searchPreviousButton(control),
                    cursorHandler: widget => testCase.findChild(widget, "previousButtonEnabledCursorHandler"),
                    needsMultipleResults: true
                },
                {
                    tag: "next-button-enabled",
                    widget: () => _find.searchNextButton(control),
                    cursorHandler: widget => testCase.findChild(widget, "nextButtonEnabledCursorHandler"),
                    needsMultipleResults: true
                },
                {
                    tag: "close-button",
                    widget: () => _find.searchCloseButton(control),
                    cursorHandler: widget => testCase.findChild(widget, "closeButtonCursorHandler"),
                    needsMultipleResults: false
                },
            ];
        }

        function test_cursorBehaviorNavButtonsEnabled(data): void {
            if (data.needsMultipleResults) {
                // Import additional comments so search yields multiple results
                control.model.import_comments([
                    {
                        "time": 1,
                        "commentType": "Comment Type 1",
                        "comment": "some comment"
                    },
                    {
                        "time": 2,
                        "commentType": "Comment Type 1",
                        "comment": "some comment"
                    },
                ]);
                waitForRendering(control);

                // Type a query that matches multiple comments
                const textField = _find.searchTextField(control);
                mouseClick(textField);
                testCase.typeWord("some");
                waitForRendering(control);
            }

            const popup = _find.searchBoxPopup(control);
            const dragArea = _find.searchDragArea(control);
            const widget = data.widget();
            const cursorHandler = data.cursorHandler(widget);

            verify(widget.enabled, "button should be enabled");

            const widgetCenter = widget.mapToItem(dragArea, widget.width / 2, widget.height / 2);
            const cx = widgetCenter.x;
            const cy = widgetCenter.y;

            // Hover → arrow cursor
            mouseMove(dragArea, cx, cy);
            compare(cursorHandler.cursorShape, Qt.ArrowCursor, "hover-enabled");

            // Press → arrow cursor
            mousePress(dragArea, cx, cy);
            compare(cursorHandler.cursorShape, Qt.ArrowCursor, "press-enabled");
            fuzzyCompare(popup.scale, 1, 0.02, "press-no-scale");

            // Release
            mouseRelease(dragArea, cx, cy);
            compare(cursorHandler.cursorShape, Qt.ArrowCursor, "release-enabled");

            // Drag → closed hand
            mousePress(dragArea, cx, cy);
            waitForRendering(control);
            mouseMove(dragArea, cx, cy - 100);
            waitForRendering(control);
            compare(cursorHandler.cursorShape, Qt.ClosedHandCursor, "drag-move-enabled");

            mouseRelease(dragArea, cx, cy - 100);
            compare(cursorHandler.cursorShape, Qt.ArrowCursor, "drag-release-enabled");
        }
    }
}
