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
    name: "MpvqcTableView::SearchBox"

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
        control.commentList.currentIndex = 0;
        waitForRendering(control);

        control.commentList.model.import_comments([
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
        const comments = control.commentList.model.comments();
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
        tryVerify(() => control.commentList.currentIndex === reviewRows[0]);
        compare(statusLabel.text, "1/3");

        for (const step of data.expected) {
            data.action(control);
            tryVerify(() => control.commentList.currentIndex === reviewRows[step.index]);
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
        tryVerify(() => control.commentList.currentIndex === reviewRows[0]);
        compare(statusLabel.text, "1/3");

        for (const step of data.expected) {
            data.action(control);
            tryVerify(() => control.commentList.currentIndex === reviewRows[step.index]);
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

        tryVerify(() => _find.searchBoxPopup(control)?.searchQuery === "review");

        const delegate = control.commentList.itemAtIndex(control.commentList.currentIndex);
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
        tryVerify(() => control.commentList.currentIndex === _reviewRows()[0]);

        const pt = _clickHelper.centerOfCommentLabel(control, control.commentList.currentIndex);
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
        tryVerify(() => _find.searchBoxPopup(control)?.searchQuery === "review");

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
        tryVerify(() => control.commentList.currentIndex === reviewRows[0]);

        const pt = _clickHelper.centerOfCommentLabel(control, control.commentList.currentIndex);
        testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
        testCase.waitUntilEditControlOpened(control);

        keyPress(Qt.Key_Escape);
        testCase.waitUntilEditControlClosed(control);
        _expect.isEventuallySearchBoxOpen(control);
        waitForRendering(control);

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
