// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    name: "MpvqcApplicationContent::NewCommentMenu"
    width: 1280
    height: 720
    visible: true
    when: windowShown

    TestHelpers {
        id: it

        testCase: testCase
    }

    function init(): void {
        it.resetState();
    }

    function test_mouseClick_addsCommentOfChosenType_data() {
        return [
            {
                tag: "keyboard"
            },
            {
                tag: "rightClick"
            },
        ];
    }

    function test_mouseClick_addsCommentOfChosenType(data): void {
        const control = it.makeControl();
        const commentTypes = it.settings.commentTypes();

        const menu = data.tag === "rightClick" ? it.menu.openNewCommentMenuViaRightClick(control) : it.menu.openNewCommentMenu(control);
        const firstItem = menu.itemAt(0);
        verify(firstItem, "expected at least one menu item");
        mouseClick(firstItem);

        it.expect.commentCount(control, 1);
        it.expect.commentTypeAt(control, 0, commentTypes[0]);
        it.expect.commentEditorHasFocus(control);
    }

    function test_keyboardNavigation_addsCommentOfHighlightedType(): void {
        const control = it.makeControl();
        const commentTypes = it.settings.commentTypes();

        it.menu.openNewCommentMenu(control);
        keyClick(Qt.Key_Down);
        keyClick(Qt.Key_Down);
        keyClick(Qt.Key_Return);

        it.expect.commentCount(control, 1);
        it.expect.commentTypeAt(control, 0, commentTypes[1]);
        it.expect.commentEditorHasFocus(control);
    }

    function test_escape_closesMenuWithoutAddingComment(): void {
        const control = it.makeControl();

        const menu = it.menu.openNewCommentMenu(control);
        keyClick(Qt.Key_Escape);

        tryVerify(() => !menu.opened);
        it.expect.commentCount(control, 0);
        it.expect.commentListHasFocus(control);
    }
}
