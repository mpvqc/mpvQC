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

    readonly property Component emptyControl: Component {
        MpvqcTableView {
            backupEnabled: false

            height: testCase.height
            width: testCase.width
        }
    }

    width: 600
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcTableView::Integration"

    function initTestCase(): void {
        _helpers.initTestCase();
    }

    function makeControl(): var {
        const control = createTemporaryObject(emptyControl, testCase);
        verify(control);
        waitForRendering(control);
        return control;
    }

    function _placeholder(control: MpvqcTableView): Item {
        return findChild(control, "placeholder");
    }

    function test_showsPlaceholderWhenEmpty(): void {
        const control = makeControl();

        compare(control.commentCount, 0);
        verify(_placeholder(control).visible);
        verify(!control.commentList.visible);
    }

    function test_hidesPlaceholderAfterAddNewComment(): void {
        const control = makeControl();

        control.addNewComment("Comment Type 1");

        tryVerify(() => control.commentCount === 1);
        verify(!_placeholder(control).visible);
        verify(control.commentList.visible);
    }

    function test_showsPlaceholderAgainAfterDeletingLastRow(): void {
        const control = makeControl();

        control.addNewComment("Comment Type 1");
        tryVerify(() => control.commentCount === 1);
        verify(!_placeholder(control).visible);

        control.commentList.model.clear_comments();

        tryVerify(() => control.commentCount === 0);
        verify(_placeholder(control).visible);
        verify(!control.commentList.visible);
    }

    function test_addNewCommentAppendsRowToModel(): void {
        const control = makeControl();

        control.addNewComment("Comment Type 1");
        tryVerify(() => control.commentCount === 1);

        control.addNewComment("Comment Type 2");
        tryVerify(() => control.commentCount === 2);

        const rows = control.commentList.model.comments();
        compare(rows[0].commentType, "Comment Type 1");
        compare(rows[1].commentType, "Comment Type 2");
    }

    function test_forceActiveFocusFocusesInnerList(): void {
        const control = makeControl();

        control.forceActiveFocus();

        tryVerify(() => control.commentList.activeFocus);
    }
}
