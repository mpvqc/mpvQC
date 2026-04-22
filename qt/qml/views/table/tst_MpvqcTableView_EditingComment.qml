// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
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

    readonly property Component signalSpy: _helpers.signalSpy
    readonly property Component objectWithRealViewModel: _helpers.objectWithRealViewModel

    width: 600
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcTableView::EditingComment"

    function initTestCase(): void {
        _helpers.initTestCase();
    }

    function makeControl(): var {
        return _helpers.makeControl();
    }

    function waitUntilEditControlOpened(control: MpvqcTableView): void {
        _helpers.waitUntilEditControlOpened(control);
    }

    function waitUntilEditControlClosed(control: MpvqcTableView): void {
        _helpers.waitUntilEditControlClosed(control);
    }

    function waitUntilContextMenuOpened(control: MpvqcTableView): void {
        _helpers.waitUntilContextMenuOpened(control);
    }

    function waitUntilContextMenuClosed(control: MpvqcTableView): void {
        _helpers.waitUntilContextMenuClosed(control);
    }

    function waitUntilMessageBoxOpened(control: MpvqcTableView): void {
        _helpers.waitUntilMessageBoxOpened(control);
    }

    function waitUntilMessageBoxClosed(control: MpvqcTableView): void {
        _helpers.waitUntilMessageBoxClosed(control);
    }

    function waitUntilSearchBoxOpened(control: MpvqcTableView): void {
        _helpers.waitUntilSearchBoxOpened(control);
    }

    function waitUntilSearchBoxClosed(control: MpvqcTableView): void {
        _helpers.waitUntilSearchBoxClosed(control);
    }

    function getCommentTypeItems(control: MpvqcTableView): list<Item> {
        return _helpers.getCommentTypeItems(control);
    }

    function typeWord(word: string): void {
        _helpers.typeWord(word);
    }

    property var control: null

    function init(): void {
        control = testCase.makeControl();
        control.commentList.currentIndex = 2;
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
                expectedEditor: ""
            },
            {
                tag: "selected-row-time-label",
                clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 2),
                expectedIndex: 2,
                expectedEditor: "timePopup"
            },
            {
                tag: "selected-row-comment-type-label",
                clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 2),
                expectedIndex: 2,
                expectedEditor: "commentTypeMenu"
            },
            {
                tag: "other-row-play-button",
                clickPoint: c => _clickHelper.topRightOfPlayButton(c, 1),
                expectedIndex: 1,
                expectedEditor: ""
            },
            // "other-row-time-label" flakes roughly 1 in 10 full-suite runs
            // (commentPopup → timePopup transition on a real compositor).
            {
                tag: "other-row-time-label",
                clickPoint: c => _clickHelper.topLeftOfTimeLabel(c, 1),
                expectedIndex: 1,
                expectedEditor: "timePopup"
            },
            {
                tag: "other-row-comment-type-label",
                clickPoint: c => _clickHelper.topRightOfCommentTypeLabel(c, 1),
                expectedIndex: 1,
                expectedEditor: "commentTypeMenu"
            },
        ];
    }

    function test_doubleClick(data): void {
        const editedValue = "edited";
        typeWord(editedValue);
        const pt = data.clickPoint(control);
        testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
        waitForRendering(control);
        _expect.hasItemComment(control, 2, editedValue);
        _expect.hasCurrentIndex(control, data.expectedIndex);
        if (data.expectedEditor) {
            _expect.isEditorShowing(control, data.expectedEditor);
            _expect.isEditing(control);
        } else {
            _expect.isNotEditing(control);
        }
    }

    // Ticket #248: Comment line text disappears when switching lines via double-click while editing
    function test_doubleClickOtherRowCommentLabel(): void {
        const editedValue = "edited";
        typeWord(editedValue);

        const ptRow1 = _clickHelper.topRightOfCommentLabel(control, 1);
        testCase.mouseDoubleClickSequence(control, ptRow1.x, ptRow1.y);
        testCase.waitUntilEditControlOpened(control);

        compare(control.getItem(2, "comment"), editedValue);
        waitForRendering(control);

        // Verify editing is still active even after timeout
        _expect.isEditing(control);
        _expect.hasCurrentIndex(control, 1);
        // Verify content in editing mode is correct
        compare(_find.commentTextArea(control).text, "Comment 2");
        // Verify text below the editing popup is empty
        compare(control.commentList.itemAtIndex(1).commentLabel.text, "");

        const ptRow0 = _clickHelper.topRightOfCommentLabel(control, 0);
        testCase.mouseClick(control, ptRow0.x, ptRow0.y);

        // Verify text is displayed again
        tryCompare(control.commentList.itemAtIndex(1).commentLabel, "text", "Comment 2");
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
        waitForRendering(control);
        _expect.hasItemComment(control, 2, editedValue);
        _expect.hasCurrentIndex(control, 2);
        _expect.hasContextMenuClosed(control);
        _expect.isNotEditing(control);
    }

    function test_keyEventsAreNotHandled(): void {
        _expect.isNotInteractive(control);
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
