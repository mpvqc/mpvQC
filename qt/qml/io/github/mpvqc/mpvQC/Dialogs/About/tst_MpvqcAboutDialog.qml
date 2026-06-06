// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

TestCase {
    id: testCase

    width: 600
    height: 700
    visible: true
    when: windowShown
    name: "MpvqcAboutDialog"

    Component {
        id: objectUnderTest

        MpvqcAboutDialog {}
    }

    function makeDialog(): Dialog {
        const dialog = createTemporaryObject(objectUnderTest, testCase);
        verify(dialog, "dialog not created");
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
        verify(find(dialog, "aboutNavigationButton").highlighted);
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
        verify(button.highlighted);
        tryVerify(() => find(dialog, data.page).visible);
    }

    function test_clickingCurrentTabIsNoop(): void {
        const dialog = makeDialog();

        mouseClick(find(dialog, "aboutNavigationButton"));

        compare(dialog.currentIndex, 0);
    }
}
