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

    readonly property Component objectWithRealViewModel: _helpers.objectWithRealViewModel

    width: 600
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcTableView::RealViewModel"

    function initTestCase(): void {
        _helpers.initTestCase();
    }

    function test_commentTypeMenuReceivesPythonCommentTypes(): void {
        const control = createTemporaryObject(objectWithRealViewModel, testCase);
        verify(control);
        waitForRendering(control);

        const expected = control.viewModel.commentTypes;
        verify(expected.length > 0);

        const pt = _clickHelper.centerOfCommentTypeLabel(control, 0);
        testCase.mouseDoubleClickSequence(control, pt.x, pt.y);
        _helpers.waitUntilEditControlOpened(control);

        const menu = _find.editCommentTypeMenu(control);
        verify(menu.commentTypes.length >= expected.length);

        for (const commentType of expected) {
            verify(menu.commentTypes.includes(commentType), `Missing comment type: ${commentType}. Menu has types: ${menu.commentTypes.join(", ")} includes`);
        }
    }
}
