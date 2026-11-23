// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Python

QtObject {
    id: root

    required property TestCase suite

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}

    readonly property Component signalSpy: Component {
        SignalSpy {}
    }

    readonly property Component objectWithRealCommentTypes: Component {
        MpvqcTableView {
            id: _realCommentTypesControl

            backupEnabled: false

            height: root.suite.height
            width: root.suite.width

            Component.onCompleted: {
                root.bridge.importComments([
                    {
                        "time": 1 * 1000,
                        "commentType": "Comment Type 1",
                        "comment": "Comment 1"
                    }
                ]);
                _realCommentTypesControl.commentList.currentIndex = 0;
            }
        }
    }

    readonly property Component objectUnderTest: Component {
        MpvqcTableView {
            id: _mockVmControl

            function getItem(index: int, property: string): var {
                return root.bridge.comment(index)[property];
            }

            backupEnabled: false

            viewModel: MpvqcCommentTableViewModel {
                property int videoDuration: 10
                property var commentTypes: ["Comment Type 1", "Comment Type 2", "Comment Type 3", "Comment Type 4", "Comment Type 5"]
                property int lastJumpToTime: -1
                property int pauseCount: 0
                function jumpToTime(time) {
                    lastJumpToTime = time;
                }
                function pauseVideo() {
                    pauseCount += 1;
                }
            }

            height: root.suite.height
            width: root.suite.width

            Component.onCompleted: {
                root.bridge.importComments([
                    {
                        "time": 1 * 1000,
                        "commentType": "Comment Type 1",
                        "comment": "Comment 1"
                    },
                    {
                        "time": 2 * 1000,
                        "commentType": "Comment Type 2",
                        "comment": "Comment 2"
                    },
                    {
                        "time": 3 * 1000,
                        "commentType": "Comment Type 3",
                        "comment": "Comment 3"
                    },
                    {
                        "time": 4 * 1000,
                        "commentType": "Comment Type 4",
                        "comment": "Comment 4"
                    },
                    {
                        "time": 5 * 1000,
                        "commentType": "Comment Type 5",
                        "comment": "Comment 5"
                    },
                ]);
                _mockVmControl.commentList.currentIndex = 0;
            }
        }
    }

    readonly property var clickHelper: QtObject {
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
            return _centerOf(control, root.suite.findChild(delegate, "playButton"));
        }

        function topRightOfPlayButton(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _topRightOf(control, root.suite.findChild(delegate, "playButton"));
        }

        function centerOfTimeLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _centerOf(control, root.suite.findChild(delegate, "timeLabel"));
        }

        function centerOfCommentTypeLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _centerOf(control, root.suite.findChild(delegate, "commentTypeLabel"));
        }

        function centerOfCommentLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _centerOf(control, root.suite.findChild(delegate, "commentLabel"));
        }

        function topRightOfTimeLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _topRightOf(control, root.suite.findChild(delegate, "timeLabel"));
        }

        function topLeftOfTimeLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _topLeftOf(control, root.suite.findChild(delegate, "timeLabel"));
        }

        function topRightOfCommentTypeLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _topRightOf(control, root.suite.findChild(delegate, "commentTypeLabel"));
        }

        function topRightOfCommentLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _topRightOf(control, root.suite.findChild(delegate, "commentLabel"));
        }

        function topLeftOfCommentLabel(control: MpvqcTableView, row: int): point {
            const delegate = control.commentList.itemAtIndex(row);
            return _topLeftOf(control, root.suite.findChild(delegate, "commentLabel"));
        }

        function clickEditCommentAction(control: MpvqcTableView): void {
            const item = root.suite.findChild(control, "editCommentAction");
            root.suite.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickCopyCommentAction(control: MpvqcTableView): void {
            const item = root.suite.findChild(control, "copyCommentAction");
            root.suite.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickDeleteCommentAction(control: MpvqcTableView): void {
            const item = root.suite.findChild(control, "deleteCommentAction");
            root.suite.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickDecrementButton(control: MpvqcTableView): void {
            const item = root.suite.findChild(control, "decrementButton");
            root.suite.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickIncrementButton(control: MpvqcTableView): void {
            const item = root.suite.findChild(control, "incrementButton");
            root.suite.mouseClick(item, item.width / 2, item.height / 2);
        }

        function clickSearchNextButton(control: MpvqcTableView): void {
            const btn = root.find.searchNextButton(control);
            root.suite.mouseClick(btn, btn.width / 2, btn.height / 2);
        }

        function clickSearchPreviousButton(control: MpvqcTableView): void {
            const btn = root.find.searchPreviousButton(control);
            root.suite.mouseClick(btn, btn.width / 2, btn.height / 2);
        }

        function clickSearchCloseButton(control: MpvqcTableView): void {
            const btn = root.find.searchCloseButton(control);
            root.suite.mouseClick(btn, btn.width / 2, btn.height / 2);
        }

        function clickCommentTypeMenuItem(control: MpvqcTableView, commentType: string): void {
            const menu = root.suite.findChild(control, "editCommentTypeMenu");
            for (let i = 0; i < menu.count; i++) { // qmllint disable
                const item = menu.itemAt(i); // qmllint disable
                if (item && item.commentType === commentType) {
                    root.suite.mouseClick(item, item.width / 2, item.height / 2);
                    return;
                }
            }
        }
    }

    readonly property var expect: QtObject {
        id: _expect

        readonly property var _editorObjectNames: ({
                "timePopup": "editTimePopup",
                "commentTypeMenu": "editCommentTypeMenu",
                "commentPopup": "editCommentPopup"
            })

        function _anyEditorOpen(control: MpvqcTableView): bool {
            const tc = root.suite;
            for (const name of ["editTimePopup", "editCommentPopup", "editCommentTypeMenu"]) {
                const popup = tc.findChild(tc, name);
                if (popup && popup.opened) {
                    return true;
                }
            }
            return false;
        }

        function isNotEditing(control: MpvqcTableView): void {
            root.suite.verify(!_anyEditorOpen(control));
        }

        function isEventuallyNotEditing(control: MpvqcTableView): void {
            root.suite.tryVerify(() => !_anyEditorOpen(control));
        }

        function isEditing(control: MpvqcTableView): void {
            root.suite.tryVerify(() => _anyEditorOpen(control));
        }

        function isInteractive(control: MpvqcTableView): void {
            root.suite.verify(control.commentList.interactive);
        }

        function isNotInteractive(control: MpvqcTableView): void {
            root.suite.verify(!control.commentList.interactive);
        }

        function hasContextMenuOpen(control: MpvqcTableView): void {
            const menu = root.suite.findChild(control, "commentContextMenu");
            root.suite.verify(menu);
            root.suite.verify(menu.opened);
        }

        function hasContextMenuClosed(control: MpvqcTableView): void {
            const menu = root.suite.findChild(control, "commentContextMenu");
            root.suite.verify(!menu || !menu.opened);
        }

        function hasMessageBoxOpen(control: MpvqcTableView): void {
            const box = root.suite.findChild(control, "deleteConfirmationMessageBox");
            root.suite.verify(box);
            root.suite.verify(box.opened);
        }

        function hasMessageBoxClosed(control: MpvqcTableView): void {
            const box = root.suite.findChild(control, "deleteConfirmationMessageBox");
            root.suite.verify(!box || !box.opened);
        }

        function hasSearchBoxOpen(control: MpvqcTableView): void {
            const popup = root.suite.findChild(control, "searchBoxPopup");
            root.suite.verify(popup);
            root.suite.verify(popup.searchActive);
        }

        function hasSearchBoxClosed(control: MpvqcTableView): void {
            const popup = root.suite.findChild(control, "searchBoxPopup");
            root.suite.verify(!popup?.searchActive);
        }

        function isEventuallySearchBoxOpen(control: MpvqcTableView): void {
            root.suite.tryVerify(() => root.suite.findChild(control, "searchBoxPopup")?.searchActive);
        }

        function isEventuallySearchBoxClosed(control: MpvqcTableView): void {
            root.suite.tryVerify(() => !root.suite.findChild(control, "searchBoxPopup")?.searchActive);
        }

        function hasActiveFocus(control: MpvqcTableView): void {
            root.suite.tryVerify(() => control.commentList.activeFocus);
        }

        function hasCurrentIndex(control: MpvqcTableView, expected: int): void {
            root.suite.compare(control.commentList.currentIndex, expected);
        }

        function hasCount(control: MpvqcTableView, expected: int): void {
            root.suite.compare(control.commentCount, expected);
        }

        function hasEventuallyCount(control: MpvqcTableView, expected: int): void {
            root.suite.tryVerify(() => control.commentCount === expected);
        }

        function isEditorShowing(control: MpvqcTableView, editor: string): void {
            const name = _editorObjectNames[editor];
            root.suite.verify(name, `Unknown editor '${editor}'`);
            root.suite.tryVerify(() => {
                const popup = root.suite.findChild(control, name);
                return popup !== null && popup.opened;
            }, root.suite.timeout, `Expected editor '${editor}' (objectName='${name}') to be opened`);
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
            root.suite.compare(control.getItem(index, "time"), expected);
        }

        function hasItemCommentType(control: MpvqcTableView, index: int, expected: string): void {
            root.suite.compare(control.getItem(index, "commentType"), expected);
        }

        function hasItemComment(control: MpvqcTableView, index: int, expected: string): void {
            root.suite.compare(control.getItem(index, "comment"), expected);
        }

        function hasLastJumpedToTime(control: MpvqcTableView, expected: int): void {
            root.suite.compare(control.viewModel.lastJumpToTime, expected);
        }

        function hasPauseCount(control: MpvqcTableView, expected: int): void {
            root.suite.compare(control.viewModel.pauseCount, expected);
        }

        function describesRow(payload: string, control: MpvqcTableView, index: int): void {
            const comment = control.getItem(index, "comment");
            const commentType = control.getItem(index, "commentType");
            root.suite.verify(comment, `Row ${index} carries no comment text to look for`);
            root.suite.verify(commentType, `Row ${index} carries no comment type to look for`);
            root.suite.verify(payload.includes(comment), `Payload '${payload}' should contain comment text '${comment}'`);
            root.suite.verify(payload.includes(commentType), `Payload '${payload}' should contain comment type '${commentType}'`);
        }
    }

    readonly property var find: QtObject {
        id: _find

        function timeSpinBox(control: MpvqcTableView): Item {
            return root.suite.findChild(control, "timeSpinBox");
        }

        function commentTextArea(control: MpvqcTableView): Item {
            return root.suite.findChild(control, "commentTextArea");
        }

        function editCommentTypeMenu(control: MpvqcTableView): var {
            return root.suite.findChild(root.suite, "editCommentTypeMenu");
        }

        function commentLabel(delegate: Item): Item {
            return root.suite.findChild(delegate, "commentLabel");
        }

        function searchBoxPopup(control: MpvqcTableView): var {
            return root.suite.findChild(control, "searchBoxPopup");
        }

        function searchIconLabel(control: MpvqcTableView): Item {
            return root.suite.findChild(control, "searchIconLabel");
        }

        function searchStatusLabel(control: MpvqcTableView): Item {
            return root.suite.findChild(control, "statusLabel");
        }

        function searchPreviousButton(control: MpvqcTableView): Item {
            return root.suite.findChild(control, "previousButton");
        }

        function searchNextButton(control: MpvqcTableView): Item {
            return root.suite.findChild(control, "nextButton");
        }

        function searchCloseButton(control: MpvqcTableView): Item {
            return root.suite.findChild(control, "closeButton");
        }

        function searchTextField(control: MpvqcTableView): Item {
            return root.suite.findChild(control, "searchTextField");
        }

        function searchDragArea(control: MpvqcTableView): Item {
            return searchBoxPopup(control).contentItem;
        }
    }

    // wait.* helpers observe the same objectName-keyed state as expect.*
    // above. Keeping them in lock-step makes "wait for X" + "verify X"
    // never disagree.
    readonly property var wait: QtObject {
        function editControlOpened(control: MpvqcTableView): void {
            root.suite.tryVerify(() => root.expect._anyEditorOpen(control));
        }

        function editControlClosed(control: MpvqcTableView): void {
            root.suite.tryVerify(() => !root.expect._anyEditorOpen(control));
        }

        function contextMenuOpened(control: MpvqcTableView): void {
            root.suite.tryVerify(() => root.suite.findChild(control, "commentContextMenu")?.opened);
        }

        function contextMenuClosed(control: MpvqcTableView): void {
            root.suite.tryVerify(() => root.suite.findChild(control, "commentContextMenu") === null);
        }

        function messageBoxOpened(control: MpvqcTableView): void {
            root.suite.tryVerify(() => root.suite.findChild(control, "deleteConfirmationMessageBox")?.opened);
        }

        function messageBoxClosed(control: MpvqcTableView): void {
            root.suite.tryVerify(() => root.suite.findChild(control, "deleteConfirmationMessageBox") === null);
        }

        function searchBoxOpened(control: MpvqcTableView): void {
            root.suite.tryVerify(() => root.suite.findChild(control, "searchBoxPopup")?.searchActive);
            root.suite.tryVerify(() => root.suite.findChild(control, "searchBoxPopup")?.opened);
        }

        function searchBoxClosed(control: MpvqcTableView): void {
            root.suite.tryVerify(() => !root.suite.findChild(control, "searchBoxPopup")?.searchActive);
            root.suite.tryVerify(() => !root.suite.findChild(control, "searchBoxPopup")?.opened);
        }

        function highlightSettled(control: MpvqcTableView): void {
            const list = control.commentList;
            root.suite.tryVerify(() => root.bridge.nearlyEqual(list.highlightItem.y, list.currentItem.y) && root.bridge.nearlyEqual(list.highlightItem.height, list.currentItem.height), root.suite.timeout, "the highlight should settle on the selected row");
        }

        function framesUntil(control: MpvqcTableView, sample: var, action: var, until: var, message: string): list<var> {
            const window = control.Window.window;
            const frames = [];
            const record = () => frames.push(sample());
            window.afterAnimating.connect(record);
            try {
                action();
                root.suite.tryVerify(() => until(frames), root.suite.timeout, message);
            } finally {
                window.afterAnimating.disconnect(record);
            }
            return frames;
        }
    }

    function makeControl(): var {
        root.bridge.resetComments();
        const control = root.suite.createTemporaryObject(root.objectUnderTest, root.suite);
        root.suite.verify(control);
        root.suite.waitForRendering(control);
        return control;
    }

    function makeRealCommentTypesControl(): var {
        root.bridge.resetComments();
        const control = root.suite.createTemporaryObject(root.objectWithRealCommentTypes, root.suite);
        root.suite.verify(control);
        root.suite.waitForRendering(control);
        return control;
    }

    function typeWord(word: string): void {
        for (const c of word) {
            root.suite.keyClick(`${c}`);
        }
    }

    function getCommentTypeItems(control: MpvqcTableView): list<Item> {
        const menu = root.suite.findChild(control, "editCommentTypeMenu");
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
