// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest
import pyobjects

TestCase {
    id: testCase

    name: "Integration::HelpMenu"
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

    function test_aboutDialogOpensFromHelpMenu(): void {
        const control = it.makeControl();

        it.triggerMenuItem(control, "helpMenu", "openAboutDialogMenuItem");

        tryVerify(() => findChild(control, "aboutDialog"));
    }
}
