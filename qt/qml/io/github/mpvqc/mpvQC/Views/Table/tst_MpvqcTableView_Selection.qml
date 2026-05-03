// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    readonly property int timeout: 2000

    TestHelpers {
        id: _helpers

        testCase: testCase
    }

    readonly property alias _clickHelper: _helpers.clickHelper
    readonly property alias _expect: _helpers.expect
    readonly property alias _find: _helpers.find
    readonly property alias _wait: _helpers.wait

    width: 600
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcTableView::Selection"

    function initTestCase(): void {
        _helpers.initTestCase();
    }

    property var control: null

    function init(): void {
        control = _helpers.makeControl();
        control.commentList.currentIndex = 2;
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
        _wait.editControlOpened(control);
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
        _wait.contextMenuOpened(control);
        _expect.hasCurrentIndex(control, data.expectedIndex);
    }

    function test_keyEventsAreHandled(): void {
        _expect.isInteractive(control);
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
        control.commentList.currentIndex = data.startIndex;
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
        control.commentList.currentIndex = data.startIndex;
        keyPress(Qt.Key_Up);
        _expect.hasCurrentIndex(control, data.expectedIndex);
    }

    function test_keyPressReturnOpensCommentEditor(): void {
        keyPress(Qt.Key_Return);
        _wait.editControlOpened(control);
        _expect.isEditing(control);
        _expect.isNotInteractive(control);
        _expect.isEditorShowingCommentPopup(control);
    }

    function test_keyPressBackspaceConfirmDeletesComment(): void {
        const countAtBeginning = control.commentCount;

        keyPress(Qt.Key_Backspace);
        _wait.messageBoxOpened(control);
        _expect.isNotInteractive(control);
        keyPress(Qt.Key_Tab);
        keyPress(Qt.Key_Return);

        _expect.hasEventuallyCount(control, countAtBeginning - 1);
        _expect.hasCurrentIndex(control, 2);
    }

    function test_keyPressDeleteConfirmDeletesComment(): void {
        const countAtBeginning = control.commentCount;

        keyPress(Qt.Key_Delete);
        _wait.messageBoxOpened(control);
        keyPress(Qt.Key_Tab);
        keyPress(Qt.Key_Return);

        _expect.hasEventuallyCount(control, countAtBeginning - 1);
        _expect.hasCurrentIndex(control, 2);
    }

    function test_keyPressDeleteCancelKeepsComment(): void {
        const countAtBeginning = control.commentCount;

        keyPress(Qt.Key_Delete);
        _wait.messageBoxOpened(control);
        keyPress(Qt.Key_Return);

        _wait.messageBoxClosed(control);
        _expect.hasCount(control, countAtBeginning);
        _expect.hasCurrentIndex(control, 2);
    }

    function test_messageBoxCanBeReopened(): void {
        keyPress(Qt.Key_Delete);
        _wait.messageBoxOpened(control);
        _expect.hasMessageBoxOpen(control);

        keyPress(Qt.Key_Return); // cancel
        _wait.messageBoxClosed(control);
        _expect.hasMessageBoxClosed(control);

        keyPress(Qt.Key_Delete);
        _wait.messageBoxOpened(control);
        _expect.hasMessageBoxOpen(control);
    }

    function test_importClosesMessageBox(): void {
        const countAtBeginning = control.commentCount;

        keyPress(Qt.Key_Delete);
        _wait.messageBoxOpened(control);
        _expect.hasMessageBoxOpen(control);

        control.commentList.model.import_comments([
            {
                "time": 99,
                "commentType": "Comment Type 1",
                "comment": "Imported"
            },
        ]);

        _wait.messageBoxClosed(control);
        _expect.hasMessageBoxClosed(control);
        _expect.hasCount(control, countAtBeginning + 1);
        _expect.hasActiveFocus(control);
    }

    function test_sequentialDeleteRemovesConsecutiveRows(): void {
        const countAtBeginning = control.commentCount;

        _expect.hasItemComment(control, 2, "Comment 3");

        keyPress(Qt.Key_Delete);
        _wait.messageBoxOpened(control);
        keyPress(Qt.Key_Tab);
        keyPress(Qt.Key_Return);
        _expect.hasEventuallyCount(control, countAtBeginning - 1);
        _expect.hasCurrentIndex(control, 2);

        _wait.messageBoxClosed(control);
        _expect.hasItemComment(control, 2, "Comment 4");

        keyPress(Qt.Key_Delete);
        _wait.messageBoxOpened(control);
        keyPress(Qt.Key_Tab);
        keyPress(Qt.Key_Return);
        _expect.hasEventuallyCount(control, countAtBeginning - 2);
        _expect.hasCurrentIndex(control, 2);

        _expect.hasItemComment(control, 2, "Comment 5");
    }

    function test_keyPressCtrlPlusCCopiesToClipboard(): void {
        const spy = createTemporaryObject(_helpers.signalSpy, control, {
            target: control.viewModel,
            signalName: "copiedToClipboard"
        });
        verify(spy);

        keyPress(Qt.Key_C, Qt.ControlModifier);

        tryVerify(() => spy.count === 1);
        const payload = spy.signalArguments[0][0];
        const selected = control.getItem(2, "comment");
        const selectedCommentType = control.getItem(2, "commentType");
        verify(payload.includes(selected), `Payload '${payload}' should contain comment text '${selected}'`);
        verify(payload.includes(selectedCommentType), `Payload '${payload}' should contain comment type '${selectedCommentType}'`);
    }

    function test_keyPressCtrlPlusFOpensSearch(): void {
        _expect.hasSearchBoxClosed(control);
        keyPress(Qt.Key_F, Qt.ControlModifier);
        _wait.searchBoxOpened(control);
        _expect.hasSearchBoxOpen(control);
    }

    function test_keyPressCtrlPlusShiftPlusZUndoRedo(): void {
        const countAtBeginning = control.commentCount;
        keyPress(Qt.Key_Z, Qt.ControlModifier); // undo import
        _expect.hasEventuallyCount(control, 0);
        keyPress(Qt.Key_Z, Qt.ControlModifier | Qt.ShiftModifier); // redo import
        _expect.hasEventuallyCount(control, countAtBeginning);
    }

    function test_addRowJumpsToRowAndOpensEditor(): void {
        const countBefore = control.commentCount;
        control.viewModel.addRow("Comment Type 1"); // time=0 in test env → sorts to index 0
        _expect.hasCount(control, countBefore + 1);
        _wait.editControlOpened(control);
        _expect.isEditing(control);
        _expect.isEditorShowingCommentPopup(control);
        _expect.hasCurrentIndex(control, 0);
    }

    function test_undoClearSelectsLastRow(): void {
        const countBeforeClear = control.commentCount;
        control.commentList.model.clear_comments();
        _expect.hasEventuallyCount(control, 0);
        keyPress(Qt.Key_Z, Qt.ControlModifier); // undo clear
        _expect.hasEventuallyCount(control, countBeforeClear);
        _expect.hasCurrentIndex(control, control.commentCount - 1);
    }

    function test_unknownCommentTypeAppearsInEditMenu(): void {
        control.commentList.model.import_comments([
            {
                "time": 10,
                "commentType": "Legacy Type",
                "comment": "Old"
            },
        ]);
        waitForRendering(control);

        const pt = _clickHelper.centerOfCommentTypeLabel(control, control.commentCount - 1);
        testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
        _wait.editControlOpened(control);

        const legacyItem = _helpers.getCommentTypeItems(control).find(item => item.commentType === "Legacy Type");
        verify(legacyItem);
        verify(legacyItem.checked);
    }

    function test_unknownCommentTypeAppearsAtBottomOfEditMenu(): void {
        control.commentList.model.import_comments([
            {
                "time": 10,
                "commentType": "Legacy Type",
                "comment": "Old"
            },
        ]);
        waitForRendering(control);

        const pt = _clickHelper.centerOfCommentTypeLabel(control, control.commentCount - 1);
        testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
        _wait.editControlOpened(control);

        const items = _helpers.getCommentTypeItems(control);
        const expected = ["Comment Type 1", "Comment Type 2", "Comment Type 3", "Comment Type 4", "Comment Type 5", "Legacy Type"];
        compare(items.map(item => item.commentType), expected);
    }
}
