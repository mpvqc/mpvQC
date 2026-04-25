// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    name: "MpvqcApplicationContent"
    width: 1280
    height: 720
    visible: true
    when: windowShown

    Component {
        id: contentComponent

        MpvqcApplicationContent {
            anchors.fill: parent
            windowActive: true
            windowWidth: testCase.width
        }
    }

    function test_aboutDialogOpensFromHelpMenu(): void {
        const content = createTemporaryObject(contentComponent, testCase);
        verify(content);

        const helpMenu = findChild(content, "helpMenu");
        verify(helpMenu, "helpMenu not found");
        helpMenu.open();
        tryVerify(() => helpMenu.opened);

        const aboutItem = findChild(helpMenu, "openAboutDialogMenuItem");
        verify(aboutItem, "openAboutDialogMenuItem not found");
        mouseClick(aboutItem);

        const dialogLoader = findChild(content, "dialogLoader");
        verify(dialogLoader, "dialogLoader not found");
        tryVerify(() => dialogLoader.item?.objectName === "aboutDialog");
    }
}
