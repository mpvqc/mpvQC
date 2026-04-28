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
    name: "MpvqcTableView::ContextMenu"

    function initTestCase(): void {
        _helpers.initTestCase();
    }

    property var control: null

    function init(): void {
        control = _helpers.makeControl();
        control.commentList.currentIndex = 2;
        waitForRendering(control);
        const pt = _clickHelper.topLeftOfCommentLabel(control, 2);
        testCase.mouseClick(control, pt.x, pt.y, Qt.RightButton);
        _wait.contextMenuOpened(control);
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
        _wait.contextMenuClosed(control);
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
        _wait.contextMenuClosed(control);
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
        _wait.contextMenuClosed(control);
        _expect.hasCurrentIndex(control, data.expectedIndex);
        _expect.isNotEditing(control);
        _expect.hasContextMenuClosed(control);
    }

    function test_keyEventsAreNotHandled(): void {
        _expect.isNotInteractive(control);
    }

    function test_selectEditComment(): void {
        _clickHelper.clickEditCommentAction(control);
        _wait.contextMenuClosed(control);
        _wait.editControlOpened(control);
        _expect.isEditing(control);
        _expect.hasContextMenuClosed(control);
    }

    function test_selectCopyToClipboard(): void {
        const spy = createTemporaryObject(_helpers.signalSpy, control, {
            target: control.viewModel,
            signalName: "copiedToClipboard"
        });
        verify(spy);

        _clickHelper.clickCopyCommentAction(control);
        _wait.contextMenuClosed(control);
        _expect.hasContextMenuClosed(control);

        tryVerify(() => spy.count === 1);
        compare(spy.signalArguments[0][0], "[00:00:03] [Comment Type 3] Comment 3");
        _expect.isNotEditing(control);
    }

    function test_selectDeleteComment(): void {
        const countAtBeginning = control.commentCount;
        _clickHelper.clickDeleteCommentAction(control);
        _wait.messageBoxOpened(control);
        _expect.hasContextMenuClosed(control);

        keyPress(Qt.Key_Tab);
        keyPress(Qt.Key_Return);

        tryVerify(() => control.commentCount === countAtBeginning - 1);
    }

    function test_escapeClosesMenu(): void {
        keyPress(Qt.Key_Escape);

        _wait.contextMenuClosed(control);
        _expect.hasCurrentIndex(control, 2);
        _expect.isNotEditing(control);
        _expect.hasContextMenuClosed(control);
    }

    function test_contextMenuCanBeReopened(): void {
        keyPress(Qt.Key_Escape);
        _wait.contextMenuClosed(control);
        _expect.hasContextMenuClosed(control);
        _expect.hasActiveFocus(control);

        const pt = _clickHelper.centerOfCommentLabel(control, 2);
        testCase.mouseClick(control, pt.x, pt.y, Qt.RightButton);
        _wait.contextMenuOpened(control);
        _expect.hasContextMenuOpen(control);

        keyPress(Qt.Key_Escape);
        _wait.contextMenuClosed(control);
        _expect.hasContextMenuClosed(control);
        _expect.hasActiveFocus(control);
    }

    function test_importClosesContextMenu(): void {
        _expect.hasContextMenuOpen(control);

        control.commentList.model.import_comments([
            {
                "time": 99,
                "commentType": "Comment Type 1",
                "comment": "Imported"
            },
        ]);

        _wait.contextMenuClosed(control);
        _expect.hasContextMenuClosed(control);
        _expect.hasActiveFocus(control);
    }
}
