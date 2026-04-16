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
    name: "MpvqcTableView::EditingTime"

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
        _expect.isNotInteractive(control);
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

        control.commentList.model.import_comments([
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

        tryVerify(() => control.commentList.currentIndex === 4);
        _expect.hasItemComment(control, 4, "Comment 3");
    }
}
