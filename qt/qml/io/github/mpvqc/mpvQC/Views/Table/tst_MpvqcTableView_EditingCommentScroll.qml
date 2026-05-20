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
    name: "MpvqcTableView::EditingCommentScroll"

    function initTestCase(): void {
        _helpers.initTestCase();
    }

    property var control: null

    readonly property string _longComment: "This is a very long comment that should wrap across multiple lines and force the inline editor to grow significantly larger than its initial single-line height, exercising the scroll-on-grow behaviour for the row being edited."

    function init(): void {
        control = _helpers.makeControl();

        // Match the live repro: enough rows that ListView actively pools
        // delegates instead of keeping every instance alive in the cache buffer.
        const extra = [];
        for (let i = 6; i <= 2000; i++) {
            extra.push({
                "time": i,
                "commentType": "Comment Type 1",
                "comment": `Comment ${i}`
            });
        }
        control.commentList.model.import_comments(extra);
        waitForRendering(control);
    }

    function cleanup(): void {
        control.destroy();
        control = null;
    }

    function _delegateBottomInViewport(list: var, index: int): real {
        const delegate = list.itemAtIndex(index);
        return delegate.y - list.contentY + delegate.height;
    }

    function _openEditorAt(index: int): void {
        const pt = _clickHelper.centerOfCommentLabel(control, index);
        testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
        _wait.editControlOpened(control);
        waitForRendering(control);
    }

    function test_listRequiresScrolling(): void {
        verify(control.commentList.contentHeight > control.commentList.height, `Precondition: contentHeight (${control.commentList.contentHeight}) must exceed viewport (${control.commentList.height})`);
    }

    function test_lastDelegateBottomStaysVisibleWhenEditorGrows(): void {
        const list = control.commentList;
        const lastIndex = control.commentCount - 1;

        list.positionViewAtEnd();
        waitForRendering(control);

        _openEditorAt(lastIndex);
        const heightBefore = list.itemAtIndex(lastIndex).height;

        _find.commentTextArea(control).text = _longComment;
        tryVerify(() => list.itemAtIndex(lastIndex).height > heightBefore, timeout, `Editor must grow (heightBefore=${heightBefore})`);

        const bottom = _delegateBottomInViewport(list, lastIndex);
        verify(bottom <= list.height + 1, `Last delegate bottom (${bottom}) should remain within viewport (${list.height})`);
    }

    function test_lastDelegateBottomStaysVisibleWhenTypingIntoEditor(): void {
        const list = control.commentList;
        const lastIndex = control.commentCount - 1;

        list.positionViewAtEnd();
        waitForRendering(control);

        _openEditorAt(lastIndex);
        const heightBefore = list.itemAtIndex(lastIndex).height;

        for (const ch of _longComment) {
            keyClick(ch);
        }

        tryVerify(() => list.itemAtIndex(lastIndex).height > heightBefore, timeout, `Editor must grow (heightBefore=${heightBefore})`);

        const bottom = _delegateBottomInViewport(list, lastIndex);
        verify(bottom <= list.height + 1, `Last delegate bottom (${bottom}) should remain within viewport (${list.height})`);
    }

    function test_lastDelegateContentYReachesScrollTargetAfterGrow(): void {
        const list = control.commentList;
        const lastIndex = control.commentCount - 1;

        list.positionViewAtEnd();
        waitForRendering(control);

        _openEditorAt(lastIndex);
        waitForRendering(control);

        const delegate = list.itemAtIndex(lastIndex);
        const contentYBefore = list.contentY;
        const yBefore = delegate.y;
        const heightBefore = delegate.height;

        _find.commentTextArea(control).text = _longComment;
        tryVerify(() => delegate.height > heightBefore, timeout);
        waitForRendering(control);

        const heightAfter = delegate.height;
        const overflow = (yBefore - contentYBefore + heightAfter) - list.height;
        const expectedScroll = Math.max(0, overflow);

        compare(list.contentY, contentYBefore + expectedScroll, `contentY should advance by ${expectedScroll}px (overflow=${overflow})`);
    }

    function test_lastDelegateSurvivesManySmallTextGrows(): void {
        const list = control.commentList;
        const lastIndex = control.commentCount - 1;

        list.positionViewAtEnd();
        waitForRendering(control);

        _openEditorAt(lastIndex);

        const textArea = _find.commentTextArea(control);
        textArea.text = "";
        for (let i = 0; i < 80; i++) {
            textArea.text = textArea.text + "word ";
        }
        waitForRendering(control);

        const bottom = _delegateBottomInViewport(list, lastIndex);
        verify(bottom <= list.height + 1, `Last delegate bottom (${bottom}) should remain within viewport (${list.height})`);
    }

    function test_lastDelegateAfterDeletingPreviousLastRowStaysVisible(): void {
        const list = control.commentList;

        list.positionViewAtEnd();
        waitForRendering(control);

        // Mimic the live repro: edit the soon-to-be-deleted last row first
        // (so its delegate hits the editing path and grows), then delete it,
        // then jump back to the bottom and edit the new last row.
        const oldLastIndex = control.commentCount - 1;
        _openEditorAt(oldLastIndex);
        keyClick(Qt.Key_Escape);
        _wait.editControlClosed(control);
        waitForRendering(control);

        control.viewModel.removeRow(oldLastIndex);
        tryVerify(() => control.commentCount === oldLastIndex, timeout, "Row should have been removed");
        waitForRendering(control);

        // Push the delegate that just rendered the deleted row out of the pool
        // by scrolling far away and back — forces ListView to reuse a fresh
        // delegate for the new last row.
        list.positionViewAtBeginning();
        waitForRendering(control);
        list.positionViewAtEnd();
        waitForRendering(control);

        const newLastIndex = control.commentCount - 1;
        list.currentIndex = newLastIndex;
        waitForRendering(control);
        control.viewModel.startEditingComment(newLastIndex);
        _wait.editControlOpened(control);
        waitForRendering(control);

        const bottomOnOpen = _delegateBottomInViewport(list, newLastIndex);
        verify(bottomOnOpen <= list.height + 1, `After deletion: last delegate bottom on open (${bottomOnOpen}) within viewport (${list.height})`);

        // Force the editor to grow by setting the text area's content directly
        // (matches the live repro: user types and the row grows beyond viewport).
        _find.commentTextArea(control).text = _longComment;
        waitForRendering(control);

        const bottomAfterTyping = _delegateBottomInViewport(list, newLastIndex);
        verify(bottomAfterTyping <= list.height + 1, `After typing: last delegate bottom (${bottomAfterTyping}) within viewport (${list.height})`);
    }
}
