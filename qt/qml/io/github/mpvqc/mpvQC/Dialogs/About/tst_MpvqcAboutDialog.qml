// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    width: 600
    height: 700
    visible: true
    when: windowShown
    name: "MpvqcAboutDialog"

    function makeDialog(mirrored = false): MpvqcAboutDialog {
        const dialog = createTemporaryObject(objectUnderTest, testCase);
        verify(dialog, "dialog not created");
        dialog.contentItem.LayoutMirroring.enabled = mirrored;
        dialog.contentItem.LayoutMirroring.childrenInherit = true;
        dialog.open();
        tryVerify(() => dialog.opened);
        waitForRendering(dialog.contentItem);
        return dialog;
    }

    function find(dialog, objectName): Item {
        const item = findChild(dialog.contentItem, objectName);
        verify(item, objectName + " not found");
        return item;
    }

    function test_initiallyShowsAboutPage(): void {
        const dialog = makeDialog();

        compare(dialog.currentIndex, 0);
        verify(find(dialog, "aboutNavigationButton").checked);
        verify(find(dialog, "aboutPage").visible);
    }

    function test_clickingTabSelectsItsPage_data(): var {
        return [
            {
                tag: "credits",
                button: "creditsNavigationButton",
                page: "creditsPage",
                expectedIndex: 1
            },
            {
                tag: "licenses",
                button: "licensesNavigationButton",
                page: "licensesPage",
                expectedIndex: 2
            },
        ];
    }

    function test_clickingTabSelectsItsPage(data): void {
        const dialog = makeDialog();
        const button = find(dialog, data.button);

        mouseClick(button);

        compare(dialog.currentIndex, data.expectedIndex);
        verify(button.checked);
        tryVerify(() => find(dialog, data.page).visible);
    }

    function test_switchingPagesKeepsNavigationInPlace(): void {
        const dialog = makeDialog();
        const buttons = ["aboutNavigationButton", "creditsNavigationButton", "licensesNavigationButton"].map(name => find(dialog, name));
        const bounds = buttons.map(button => Qt.rect(button.x, button.y, button.width, button.height));

        for (const index of [1, 2, 0, 2, 1, 0]) {
            mouseClick(buttons[index]);
            waitForRendering(dialog.contentItem);

            compare(dialog.currentIndex, index);
            for (let i = 0; i < buttons.length; ++i) {
                const button = buttons[i];
                compare(Qt.rect(button.x, button.y, button.width, button.height), bounds[i]);
            }
        }
    }

    function test_clickingCurrentTabIsNoop(): void {
        const dialog = makeDialog();

        mouseClick(find(dialog, "aboutNavigationButton"));

        compare(dialog.currentIndex, 0);
    }

    function test_navigationFollowsReadingDirection_data(): var {
        return [
            {
                tag: "ltr",
                mirrored: false,
                forwardKey: Qt.Key_Right,
                backwardKey: Qt.Key_Left
            },
            {
                tag: "rtl",
                mirrored: true,
                forwardKey: Qt.Key_Left,
                backwardKey: Qt.Key_Right
            },
        ];
    }

    function test_navigationFollowsReadingDirection(data): void {
        const dialog = makeDialog(data.mirrored);
        const buttons = ["aboutNavigationButton", "creditsNavigationButton", "licensesNavigationButton"].map(name => find(dialog, name));
        const positions = buttons.map(button => button.mapToItem(dialog.contentItem, 0, 0).x);

        for (let i = 0; i < buttons.length - 1; ++i) {
            compare(buttons[i].mirrored, data.mirrored);
            verify(data.mirrored ? positions[i] > positions[i + 1] : positions[i] < positions[i + 1], "Tabs must follow the reading direction");
        }

        buttons[0].forceActiveFocus(Qt.TabFocusReason);
        tryVerify(() => buttons[0].activeFocus);
        keyClick(data.forwardKey);
        compare(dialog.currentIndex, 1);
        verify(buttons[1].checked);
        verify(find(dialog, "creditsPage").visible);

        keyClick(data.backwardKey);
        compare(dialog.currentIndex, 0);
        verify(buttons[0].checked);
        verify(find(dialog, "aboutPage").visible);
    }

    Component {
        id: objectUnderTest

        MpvqcAboutDialog {}
    }
}
