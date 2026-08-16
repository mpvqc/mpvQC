// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    width: 600
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcTableView::CommentTypes"

    readonly property alias _clickHelper: _helpers.clickHelper
    readonly property alias _wait: _helpers.wait

    readonly property int timeout: 2000

    function initTestCase(): void {
        _helpers.initTestCase();
    }

    function test_commentTypeMenuReceivesPythonCommentTypes(): void {
        const control = _helpers.makeRealCommentTypesControl();

        const expected = control.viewModel.commentTypes;
        verify(expected.length > 0);

        const pt = _clickHelper.centerOfCommentTypeLabel(control, 0);
        testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
        _wait.editControlOpened(control);

        const offered = [];
        for (const item of _helpers.getCommentTypeItems(control)) {
            offered.push(item.commentType);
        }
        verify(offered.length >= expected.length);

        for (const commentType of expected) {
            verify(offered.includes(commentType), `Missing comment type: ${commentType}. Menu offers: ${offered.join(", ")}`);
        }
    }

    TestHelpers {
        id: _helpers

        testCase: testCase
    }
}
