// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    width: 1280
    height: 720
    visible: true
    when: windowShown
    name: "MpvqcMessageBoxLoader"

    Component {
        id: objectUnderTest

        MpvqcMessageBoxLoader {}
    }

    function makeControl(): MpvqcMessageBoxLoader {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        return control;
    }

    function waitUntilOpened(control: Item): void {
        tryVerify(() => control.item);
        waitForRendering(control.item?.contentItem);
        tryVerify(() => control.item.opened);
    }

    function test_openQuitMessageBox() {
        const control = makeControl();
        control.openQuitMessageBox();
        waitUntilOpened(control);
    }
}
