// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    width: 500
    height: 600
    visible: true
    when: windowShown
    name: "MpvqcAboutTab"

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}

    Component {
        id: objectUnderTest

        MpvqcAboutTab {
            anchors.fill: parent
            viewModel: MpvqcAboutDialogViewModel {}
        }
    }

    function makeTab(): Item {
        const tab = createTemporaryObject(objectUnderTest, testCase);
        verify(tab);
        waitForRendering(tab);
        return tab;
    }

    function find(tab, objectName): Item {
        const item = findChild(tab, objectName);
        verify(item, objectName + " not found");
        return item;
    }

    function test_clickingWebsiteRowOpensProjectUrl(): void {
        const tab = makeTab();
        const before = bridge.openedDesktopUrls().length;

        mouseClick(find(tab, "websiteRow"));

        const opened = bridge.openedDesktopUrls();
        compare(opened.length, before + 1);
        compare(opened[opened.length - 1], "https://mpvqc.github.io");
    }

    function test_clickingCopyRowFlipsIconToConfirm(): void {
        const tab = makeTab();
        const copyRow = find(tab, "copyVersionRow");

        compare(copyRow.icon.source, MpvqcIcons.contentCopy);
        mouseClick(copyRow);
        compare(copyRow.icon.source, MpvqcIcons.check);
    }
}
