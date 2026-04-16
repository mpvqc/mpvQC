// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

import pyobjects

import "../../utility"

QtObject {
    id: root

    required property TestCase testCase

    readonly property Component signalSpy: Component {
        SignalSpy {}
    }

    readonly property Component objectWithRealViewModel: Component {
        MpvqcTableView {
            id: _realVmControl

            backupEnabled: false

            height: root.testCase.height
            width: root.testCase.width

            Component.onCompleted: {
                _realVmControl.commentList.model.import_comments([
                    {
                        "time": 1,
                        "commentType": "Comment Type 1",
                        "comment": "Comment 1"
                    }
                ]);
                _realVmControl.commentList.currentIndex = 0;
            }
        }
    }

    readonly property Component objectUnderTest: Component {
        MpvqcTableView {
            id: _mockVmControl

            backupEnabled: false

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

            height: root.testCase.height
            width: root.testCase.width

            Component.onCompleted: {
                _mockVmControl.commentList.model.import_comments([
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
                _mockVmControl.commentList.currentIndex = 0;
            }

            function getItem(index: int, property: string): var {
                return commentList.model.comments()[index][property];
            }
        }
    }

    function initTestCase(): void {
        MpvqcLabelWidthCalculator.timeLabelWidth = 50;
        MpvqcLabelWidthCalculator.commentTypesLabelWidth = 150;
    }

    function makeControl(): var {
        const control = root.testCase.createTemporaryObject(root.objectUnderTest, root.testCase);
        root.testCase.verify(control);
        root.testCase.waitForRendering(control);
        return control;
    }

    readonly property QtObject clickHelper: QtObject {
        id: _clickHelper

        function _centerOf(control: MpvqcTableView, item: Item): point {
            const globalPt = item.mapToGlobal(item.width / 2, item.height / 2);
            return control.mapFromGlobal(globalPt.x, globalPt.y);
        }

        function _topRightOf(control: MpvqcTableView, item: Item): point {
            const globalPt = item.mapToGlobal(item.width - 3, 3);
            return control.mapFromGlobal(globalPt.x, globalPt.y);
        }

        function _topLeftOf(control: MpvqcTableView, item: Item): point {
            const globalPt = item.mapToGlobal(3, 3);
            return control.mapFromGlobal(globalPt.x, globalPt.y);
        }

        function centerOfPlayButton(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _centerOf(control, root.testCase.findChild(delegate, "playButton"));
        }

        function topRightOfPlayButton(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _topRightOf(control, root.testCase.findChild(delegate, "playButton"));
        }

        function centerOfTimeLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _centerOf(control, root.testCase.findChild(delegate, "timeLabel"));
        }

        function centerOfCommentTypeLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _centerOf(control, root.testCase.findChild(delegate, "commentTypeLabel"));
        }

        function centerOfCommentLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _centerOf(control, root.testCase.findChild(delegate, "commentLabel"));
        }

        function topRightOfTimeLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _topRightOf(control, root.testCase.findChild(delegate, "timeLabel"));
        }

        function topLeftOfTimeLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _topLeftOf(control, root.testCase.findChild(delegate, "timeLabel"));
        }

        function topRightOfCommentTypeLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _topRightOf(control, root.testCase.findChild(delegate, "commentTypeLabel"));
        }

        function topRightOfCommentLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _topRightOf(control, root.testCase.findChild(delegate, "commentLabel"));
        }

        function topLeftOfCommentLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _topLeftOf(control, root.testCase.findChild(delegate, "commentLabel"));
        }

        function clickEditCommentAction(control: MpvqcTableView): void {
            const item = root.testCase.findChild(control, "editCommentAction");
            root.testCase.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickCopyCommentAction(control: MpvqcTableView): void {
            const item = root.testCase.findChild(control, "copyCommentAction");
            root.testCase.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickDeleteCommentAction(control: MpvqcTableView): void {
            const item = root.testCase.findChild(control, "deleteCommentAction");
            root.testCase.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickDecrementButton(control: MpvqcTableView): void {
            const item = root.testCase.findChild(control, "decrementButton");
            root.testCase.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickIncrementButton(control: MpvqcTableView): void {
            const item = root.testCase.findChild(control, "incrementButton");
            root.testCase.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickSearchNextButton(control: MpvqcTableView): void {
            const btn = root.find.searchNextButton(control);
            root.testCase.mouseClick(btn, btn.width / 2, btn.height / 2);
        }

        function clickSearchPreviousButton(control: MpvqcTableView): void {
            const btn = root.find.searchPreviousButton(control);
            root.testCase.mouseClick(btn, btn.width / 2, btn.height / 2);
        }

        function clickSearchCloseButton(control: MpvqcTableView): void {
            const btn = root.find.searchCloseButton(control);
            root.testCase.mouseClick(btn, btn.width / 2, btn.height / 2);
        }

        function clickCommentTypeMenuItem(control: MpvqcTableView, commentType: string): void {
            const menu = root.testCase.findChild(control, "editCommentTypeMenu");
            for (let i = 0; i < menu.count; i++) { // qmllint disable
                const item = menu.itemAt(i); // qmllint disable
                if (item && item.commentType === commentType) {
                    root.testCase.mouseClick(item, item.width / 2, item.height / 2);
                    return;
                }
            }
        }
    }

    readonly property QtObject expect: QtObject {
        id: _expect

        function _anyEditorOpen(control: MpvqcTableView): bool {
            const tc = root.testCase;
            return tc.findChild(tc, "timeSpinBox") !== null || tc.findChild(tc, "commentTextArea") !== null || tc.findChild(tc, "editCommentTypeMenu") !== null;
        }

        function isNotEditing(control: MpvqcTableView): void {
            root.testCase.verify(!_anyEditorOpen(control));
        }

        function isEventuallyNotEditing(control: MpvqcTableView): void {
            root.testCase.tryVerify(() => !_anyEditorOpen(control));
        }

        function isEditing(control: MpvqcTableView): void {
            root.testCase.tryVerify(() => _anyEditorOpen(control));
        }

        function isInteractive(control: MpvqcTableView): void {
            root.testCase.verify(control.commentList.interactive);
        }

        function isNotInteractive(control: MpvqcTableView): void {
            root.testCase.verify(!control.commentList.interactive);
        }

        function hasContextMenuOpen(control: MpvqcTableView): void {
            const menu = root.testCase.findChild(control, "commentContextMenu");
            root.testCase.verify(menu);
            root.testCase.verify(menu.opened);
        }

        function hasContextMenuClosed(control: MpvqcTableView): void {
            const menu = root.testCase.findChild(control, "commentContextMenu");
            root.testCase.verify(!menu || !menu.opened);
        }

        function hasMessageBoxOpen(control: MpvqcTableView): void {
            const box = root.testCase.findChild(control, "deleteConfirmationMessageBox");
            root.testCase.verify(box);
            root.testCase.verify(box.opened);
        }

        function hasMessageBoxClosed(control: MpvqcTableView): void {
            const box = root.testCase.findChild(control, "deleteConfirmationMessageBox");
            root.testCase.verify(!box || !box.opened);
        }

        function hasSearchBoxOpen(control: MpvqcTableView): void {
            const popup = root.testCase.findChild(control, "searchBoxPopup");
            root.testCase.verify(popup);
            root.testCase.verify(popup.searchActive);
        }

        function hasSearchBoxClosed(control: MpvqcTableView): void {
            const popup = root.testCase.findChild(control, "searchBoxPopup");
            root.testCase.verify(!popup?.searchActive);
        }

        function isEventuallySearchBoxOpen(control: MpvqcTableView): void {
            root.testCase.tryVerify(() => root.testCase.findChild(control, "searchBoxPopup")?.searchActive);
        }

        function isEventuallySearchBoxClosed(control: MpvqcTableView): void {
            root.testCase.tryVerify(() => !root.testCase.findChild(control, "searchBoxPopup")?.searchActive);
        }

        function hasActiveFocus(control: MpvqcTableView): void {
            root.testCase.tryVerify(() => control.commentList.activeFocus);
        }

        function hasCurrentIndex(control: MpvqcTableView, expected: int): void {
            root.testCase.compare(control.commentList.currentIndex, expected);
        }

        function hasCount(control: MpvqcTableView, expected: int): void {
            root.testCase.compare(control.commentCount, expected);
        }

        function hasEventuallyCount(control: MpvqcTableView, expected: int): void {
            root.testCase.tryVerify(() => control.commentCount === expected);
        }

        readonly property var _editorObjectNames: ({
                "timePopup": "timeSpinBox",
                "commentTypeMenu": "editCommentTypeMenu",
                "commentPopup": "commentTextArea"
            })

        function isEditorShowing(control: MpvqcTableView, editor: string): void {
            const name = _editorObjectNames[editor];
            root.testCase.verify(name, `Unknown editor '${editor}'`);
            root.testCase.tryVerify(() => root.testCase.findChild(control, name) !== null, root.testCase.timeout, `Expected editor '${editor}' (objectName='${name}') to be present`);
        }

        function isEditorShowingTimePopup(control: MpvqcTableView): void {
            isEditorShowing(control, "timePopup");
        }

        function isEditorShowingCommentTypeMenu(control: MpvqcTableView): void {
            isEditorShowing(control, "commentTypeMenu");
        }

        function isEditorShowingCommentPopup(control: MpvqcTableView): void {
            isEditorShowing(control, "commentPopup");
        }

        function hasItemTime(control: MpvqcTableView, index: int, expected: int): void {
            root.testCase.compare(control.getItem(index, "time"), expected);
        }

        function hasItemCommentType(control: MpvqcTableView, index: int, expected: string): void {
            root.testCase.compare(control.getItem(index, "commentType"), expected);
        }

        function hasItemComment(control: MpvqcTableView, index: int, expected: string): void {
            root.testCase.compare(control.getItem(index, "comment"), expected);
        }

        function hasLastJumpedToTime(control: MpvqcTableView, expected: int): void {
            root.testCase.compare(control.viewModel.lastJumpToTime, expected);
        }
    }

    readonly property QtObject find: QtObject {
        id: _find

        function timeSpinBox(control: MpvqcTableView): Item {
            return root.testCase.findChild(control, "timeSpinBox");
        }

        function commentTextArea(control: MpvqcTableView): Item {
            return root.testCase.findChild(control, "commentTextArea");
        }

        function editCommentTypeMenu(control: MpvqcTableView): var {
            return root.testCase.findChild(root.testCase, "editCommentTypeMenu");
        }

        function commentLabel(delegate: Item): Item {
            return root.testCase.findChild(delegate, "commentLabel");
        }

        function searchBoxPopup(control: MpvqcTableView): var {
            return root.testCase.findChild(control, "searchBoxPopup");
        }

        function searchIconLabel(control: MpvqcTableView): Item {
            return root.testCase.findChild(control, "searchIconLabel");
        }

        function searchStatusLabel(control: MpvqcTableView): Item {
            return root.testCase.findChild(control, "statusLabel");
        }

        function searchPreviousButton(control: MpvqcTableView): Item {
            return root.testCase.findChild(control, "previousButton");
        }

        function searchNextButton(control: MpvqcTableView): Item {
            return root.testCase.findChild(control, "nextButton");
        }

        function searchCloseButton(control: MpvqcTableView): Item {
            return root.testCase.findChild(control, "closeButton");
        }

        function searchTextField(control: MpvqcTableView): Item {
            return root.testCase.findChild(control, "searchTextField");
        }

        function searchDragArea(control: MpvqcTableView): Item {
            return searchBoxPopup(control).contentItem;
        }
    }

    // --- waitUntil* helpers all observe the same objectName-keyed state used
    // by the `_expect.*` assertions above. Keeping them in lock-step makes
    // "wait for X" + "verify X" never disagree.

    function waitUntilEditControlOpened(control: MpvqcTableView): void {
        root.testCase.tryVerify(() => root.expect._anyEditorOpen(control));
    }

    function waitUntilEditControlClosed(control: MpvqcTableView): void {
        root.testCase.tryVerify(() => !root.expect._anyEditorOpen(control));
    }

    function waitUntilContextMenuOpened(control: MpvqcTableView): void {
        root.testCase.tryVerify(() => root.testCase.findChild(control, "commentContextMenu")?.opened);
    }

    function waitUntilContextMenuClosed(control: MpvqcTableView): void {
        root.testCase.tryVerify(() => root.testCase.findChild(control, "commentContextMenu") === null);
    }

    function waitUntilMessageBoxOpened(control: MpvqcTableView): void {
        root.testCase.tryVerify(() => root.testCase.findChild(control, "deleteConfirmationMessageBox")?.opened);
    }

    function waitUntilMessageBoxClosed(control: MpvqcTableView): void {
        root.testCase.tryVerify(() => root.testCase.findChild(control, "deleteConfirmationMessageBox") === null);
    }

    function waitUntilSearchBoxOpened(control: MpvqcTableView): void {
        root.testCase.tryVerify(() => root.testCase.findChild(control, "searchBoxPopup")?.searchActive);
        root.testCase.tryVerify(() => root.testCase.findChild(control, "searchBoxPopup")?.opened);
    }

    function waitUntilSearchBoxClosed(control: MpvqcTableView): void {
        root.testCase.tryVerify(() => !root.testCase.findChild(control, "searchBoxPopup")?.searchActive);
        root.testCase.tryVerify(() => !root.testCase.findChild(control, "searchBoxPopup")?.opened);
    }

    function typeWord(word: string): void {
        for (const c of word) {
            root.testCase.keyClick(`${c}`);
        }
    }

    function getCommentTypeItems(control: MpvqcTableView): list<Item> {
        const menu = root.testCase.findChild(control, "editCommentTypeMenu");
        const items = [];
        for (let i = 0; i < menu.count; i++) { // qmllint disable
            const item = menu.itemAt(i); // qmllint disable
            if (item && item.commentType) {
                items.push(item);
            }
        }
        return items;
    }
}
