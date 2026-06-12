// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    readonly property int timeout: 2000

    readonly property alias _clickHelper: _helpers.clickHelper
    readonly property alias _expect: _helpers.expect
    readonly property alias _find: _helpers.find
    readonly property alias _wait: _helpers.wait

    TestHelpers {
        id: _helpers

        testCase: testCase
    }

    QtObject {
        id: _undoHelpers

        function importMixedComments(count: int): void {
            const longText = "lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.";
            const filler = [];
            for (let i = 0; i < count; i++) {
                const isLong = i % 10 === 0;
                filler.push({
                    "time": 100 + i,
                    "commentType": "Comment Type 1",
                    "comment": isLong ? `Row ${i}: ${longText}` : `Row ${i}`
                });
            }
            testCase.control.viewModel.importComments(filler);
            testCase.waitForRendering(testCase.control);
        }

        function editComment(row: int, newText: string): string {
            const originalText = testCase.control.viewModel.comments()[row].comment;
            testCase.control.commentList.currentIndex = row;
            testCase.waitForRendering(testCase.control);
            testCase.control.viewModel.updateComment(row, newText);
            testCase.waitForRendering(testCase.control);
            testCase.compare(testCase.control.viewModel.comments()[row].comment, newText);
            return originalText;
        }

        function editTime(srcRow: int, newTime: int): var {
            const original = testCase.control.viewModel.comments()[srcRow];
            testCase.control.commentList.currentIndex = srcRow;
            testCase.waitForRendering(testCase.control);
            testCase.control.viewModel.updateTime(srcRow, newTime);
            testCase.tryVerify(() => testCase.control.viewModel.selection.selectedRowVisible === true);
            const dstRow = testCase.control.commentList.currentIndex;
            testCase.compare(testCase.control.viewModel.comments()[dstRow].time, newTime);
            return {
                "dstRow": dstRow,
                "originalTime": original.time,
                "originalComment": original.comment
            };
        }

        function scrollSelectionOffscreen(): void {
            const list = testCase.control.commentList;
            for (let i = 0; i < 20; i++) {
                if (!testCase.control.viewModel.selection.selectedRowVisible) {
                    break;
                }
                testCase.mouseWheel(list, list.width / 2, list.height / 2, 0, -120, Qt.NoButton, Qt.NoModifier);
            }
            testCase.waitForRendering(testCase.control);
            testCase.tryVerify(() => testCase.control.viewModel.selection.selectedRowVisible === false);
        }
    }

    width: 600
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcTableView::Undo"

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

    function test_undoIsNoopWithEmptyHistory(): void {
        // Drain the initial ImportComments command from history so the next
        // undo finds nothing to do.
        control.viewModel.undo();
        _expect.hasEventuallyCount(control, 0);

        const before = JSON.stringify(control.viewModel.comments());

        control.viewModel.undo();
        waitForRendering(control);

        compare(JSON.stringify(control.viewModel.comments()), before);
    }

    function test_redoIsNoopWithEmptyRedoStack(): void {
        _undoHelpers.editComment(1, "edited");
        const after = JSON.stringify(control.viewModel.comments());

        // Fresh edit clears the redo stack; redo should now be a no-op.
        control.viewModel.redo();
        waitForRendering(control);

        compare(JSON.stringify(control.viewModel.comments()), after);
    }

    function test_undoCommentEditRevertsWhenSelectionMatches(): void {
        const originalText = _undoHelpers.editComment(1, "edited");

        control.viewModel.undo();

        tryVerify(() => control.viewModel.comments()[1].comment === originalText);
    }

    function test_redoCommentEditReappliesWhenSelectionMatches(): void {
        _undoHelpers.editComment(1, "edited");
        control.viewModel.undo();
        waitForRendering(control);

        control.viewModel.redo();

        tryVerify(() => control.viewModel.comments()[1].comment === "edited");
    }

    function test_undoCommentEditMovesSelectionThenRevertsWhenSelectionElsewhere(): void {
        const originalText = _undoHelpers.editComment(1, "edited");
        control.commentList.currentIndex = 4;

        control.viewModel.undo();
        tryVerify(() => control.commentList.currentIndex === 1);
        compare(control.viewModel.comments()[1].comment, "edited");

        control.viewModel.undo();
        tryVerify(() => control.viewModel.comments()[1].comment === originalText);
    }

    function test_redoCommentEditMovesSelectionThenReappliesWhenSelectionElsewhere(): void {
        const originalText = _undoHelpers.editComment(1, "edited");
        control.viewModel.undo();
        waitForRendering(control);
        control.commentList.currentIndex = 4;

        control.viewModel.redo();
        tryVerify(() => control.commentList.currentIndex === 1);
        compare(control.viewModel.comments()[1].comment, originalText);

        control.viewModel.redo();
        tryVerify(() => control.viewModel.comments()[1].comment === "edited");
    }

    function test_undoCommentEditScrollsToRowThenRevertsWhenSelectionOffscreen(): void {
        _undoHelpers.importMixedComments(50);
        const originalText = _undoHelpers.editComment(0, "edited");
        _undoHelpers.scrollSelectionOffscreen();

        control.viewModel.undo();
        tryVerify(() => control.viewModel.selection.selectedRowVisible === true);
        waitForRendering(control);
        compare(control.viewModel.comments()[0].comment, "edited");

        control.viewModel.undo();
        tryVerify(() => control.viewModel.comments()[0].comment === originalText);
    }

    function test_undoTimeEditRevertsWhenSelectionMatches(): void {
        _undoHelpers.importMixedComments(495);
        const edit = _undoHelpers.editTime(250, 5);
        verify(edit.dstRow !== 250);

        control.viewModel.undo();

        tryVerify(() => {
            const c = control.viewModel.comments()[250];
            return c.time === edit.originalTime && c.comment === edit.originalComment;
        });
    }

    function test_redoTimeEditReappliesWhenSelectionMatches(): void {
        _undoHelpers.importMixedComments(495);
        const edit = _undoHelpers.editTime(250, 5);
        control.viewModel.undo();
        waitForRendering(control);

        tryVerify(() => control.viewModel.selection.selectedRowVisible === true);

        control.viewModel.redo();

        tryVerify(() => control.viewModel.comments()[edit.dstRow].time === 5);
    }

    function test_undoTimeEditMovesSelectionThenRevertsWhenSelectionElsewhere(): void {
        _undoHelpers.importMixedComments(495);
        const edit = _undoHelpers.editTime(250, 5);

        control.commentList.currentIndex = edit.dstRow + 10;
        waitForRendering(control);

        control.viewModel.undo();
        tryVerify(() => control.commentList.currentIndex === edit.dstRow && control.viewModel.selection.selectedRowVisible === true);
        compare(control.viewModel.comments()[edit.dstRow].time, 5);

        control.viewModel.undo();
        tryVerify(() => {
            const c = control.viewModel.comments()[250];
            return c.time === edit.originalTime && c.comment === edit.originalComment;
        });
    }

    function test_redoTimeEditMovesSelectionThenReappliesWhenSelectionElsewhere(): void {
        _undoHelpers.importMixedComments(495);
        const edit = _undoHelpers.editTime(250, 5);
        control.viewModel.undo();
        waitForRendering(control);

        // Position srcRow into view, then move selection to a nearby visible
        // row so the mismatch isn't tangled up with a not-visible condition.
        control.commentList.positionViewAtIndex(250, ListView.Center);
        waitForRendering(control);
        control.commentList.currentIndex = 253;
        waitForRendering(control);

        control.viewModel.redo();
        tryVerify(() => control.commentList.currentIndex === 250);
        compare(control.viewModel.comments()[250].time, edit.originalTime);

        control.viewModel.redo();
        tryVerify(() => control.viewModel.comments()[edit.dstRow].time === 5);
    }

    function test_undoTimeEditScrollsToRowThenRevertsWhenSelectionOffscreen(): void {
        _undoHelpers.importMixedComments(495);
        const edit = _undoHelpers.editTime(250, 5);
        _undoHelpers.scrollSelectionOffscreen();

        control.viewModel.undo();
        tryVerify(() => control.viewModel.selection.selectedRowVisible === true);
        waitForRendering(control);
        compare(control.viewModel.comments()[edit.dstRow].time, 5);

        control.viewModel.undo();
        tryVerify(() => {
            const c = control.viewModel.comments()[250];
            return c.time === edit.originalTime && c.comment === edit.originalComment;
        });
    }

    function test_redoTimeEditScrollsToRowThenReappliesWhenSelectionOffscreen(): void {
        _undoHelpers.importMixedComments(495);
        const edit = _undoHelpers.editTime(250, 5);
        control.viewModel.undo();
        waitForRendering(control);
        tryVerify(() => control.commentList.currentIndex === 250);

        _undoHelpers.scrollSelectionOffscreen();

        control.viewModel.redo();
        tryVerify(() => control.viewModel.selection.selectedRowVisible === true);
        waitForRendering(control);
        compare(control.viewModel.comments()[250].time, edit.originalTime);

        control.viewModel.redo();
        tryVerify(() => control.viewModel.comments()[edit.dstRow].time === 5);
    }

    function test_undoTimeEditScrollsBackToOriginalPosition(): void {
        _undoHelpers.importMixedComments(50);
        control.commentList.currentIndex = 6;
        waitForRendering(control);

        const startTime = control.viewModel.comments()[6].time;
        _undoHelpers.editTime(6, startTime + 1000000);

        control.viewModel.undo();
        waitForRendering(control);

        tryVerify(() => control.viewModel.comments()[6].time === startTime);
        tryVerify(() => control.viewModel.selection.selectedRowVisible === true, 2000, "view did not follow the row after undoing the time change");
    }

    function test_userJourneyAddEditUndoRedoRoundTrips(): void {
        // Add A: opens the comment popup; cancel it, then commit the text via
        // a direct updateComment which fuses with the armed AddComment.
        control.viewModel.addRow("Comment Type 1");
        _wait.editControlOpened(control);
        keyClick(Qt.Key_Escape);
        _wait.editControlClosed(control);
        control.viewModel.updateComment(0, "first");
        tryVerify(() => control.viewModel.comments()[0].comment === "first");
        compare(control.commentCount, 6);

        // Add B the same way (also time 0, seq tie-break places it at index 1).
        control.viewModel.addRow("Comment Type 1");
        _wait.editControlOpened(control);
        keyClick(Qt.Key_Escape);
        _wait.editControlClosed(control);
        control.viewModel.updateComment(1, "second");
        tryVerify(() => control.viewModel.comments()[1].comment === "second");
        compare(control.commentCount, 7);

        // Select A — disarms the merge so the next text edit is its own command.
        control.commentList.currentIndex = 0;
        waitForRendering(control);

        // Edit A's text — separate UpdateComment, not fused.
        control.viewModel.updateComment(0, "first edited");
        compare(control.viewModel.comments()[0].comment, "first edited");

        // Select B and re-time it past the init rows; B moves from 1 to 6.
        control.commentList.currentIndex = 1;
        waitForRendering(control);
        control.viewModel.updateTime(1, 8 * 1000);
        tryVerify(() => control.viewModel.comments()[6].comment === "second");
        compare(control.viewModel.comments()[6].time, 8 * 1000);

        // Undo time move — focused on B at dst index 6.
        tryVerify(() => control.commentList.currentIndex === 6);
        control.viewModel.undo();
        tryVerify(() => control.viewModel.comments()[1].comment === "second");
        compare(control.viewModel.comments()[1].time, 0);

        // Re-focus A; undo the text edit.
        control.commentList.currentIndex = 0;
        waitForRendering(control);
        control.viewModel.undo();
        tryVerify(() => control.viewModel.comments()[0].comment === "first");

        // Redo the text edit — still focused on A.
        control.viewModel.redo();
        tryVerify(() => control.viewModel.comments()[0].comment === "first edited");

        // Re-focus B; redo the time move and verify the round-trip state.
        control.commentList.currentIndex = 1;
        waitForRendering(control);
        control.viewModel.redo();
        tryVerify(() => control.viewModel.comments()[6].comment === "second");
        compare(control.viewModel.comments()[6].time, 8 * 1000);
        compare(control.viewModel.comments()[0].comment, "first edited");
    }
}
