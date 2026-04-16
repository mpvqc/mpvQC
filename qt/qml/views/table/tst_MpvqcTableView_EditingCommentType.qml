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
    name: "MpvqcTableView::EditingCommentType"

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
        _expect.isNotInteractive(control);
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

        control.commentList.model.import_comments([
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
