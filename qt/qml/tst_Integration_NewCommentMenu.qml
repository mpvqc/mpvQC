// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest
import pyobjects

TestCase {
    id: testCase

    name: "Integration::NewCommentMenu"
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

    function test_mouseClick_addsCommentOfChosenType(): void {
        const control = it.makeControl();
        const tableView = findChild(control, "tableView");
        verify(tableView, "tableView not found");
        const commentTypes = it.settings.commentTypes();

        const menu = it.openNewCommentMenu(control);
        const firstItem = menu.itemAt(0);
        verify(firstItem, "expected at least one menu item");
        mouseClick(firstItem);

        tryVerify(() => tableView.commentCount === 1);
        tryVerify(() => tableView.commentList.itemAtIndex(0).commentType === commentTypes[0]);
        tryVerify(() => findChild(control, "commentTextArea")?.activeFocus);
    }

    function test_keyboardNavigation_addsCommentOfHighlightedType(): void {
        const control = it.makeControl();
        const tableView = findChild(control, "tableView");
        verify(tableView, "tableView not found");
        const commentTypes = it.settings.commentTypes();

        it.openNewCommentMenu(control);
        keyClick(Qt.Key_Down);
        keyClick(Qt.Key_Down);
        keyClick(Qt.Key_Return);

        tryVerify(() => tableView.commentCount === 1);
        tryVerify(() => tableView.commentList.itemAtIndex(0).commentType === commentTypes[1]);
        tryVerify(() => findChild(control, "commentTextArea")?.activeFocus);
    }

    function test_escape_closesMenuWithoutAddingComment(): void {
        const control = it.makeControl();
        const tableView = findChild(control, "tableView");
        verify(tableView, "tableView not found");

        const menu = it.openNewCommentMenu(control);
        keyClick(Qt.Key_Escape);

        tryVerify(() => !menu.opened);
        compare(tableView.commentCount, 0);
        tryVerify(() => tableView.commentList.activeFocus);
    }
}
