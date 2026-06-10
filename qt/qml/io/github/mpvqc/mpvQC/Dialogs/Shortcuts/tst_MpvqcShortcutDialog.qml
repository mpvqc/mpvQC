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
    name: "MpvqcShortcutDialog"

    Component {
        id: objectUnderTest

        MpvqcShortcutDialog {}
    }

    function makeDialog(): Dialog {
        const dialog = createTemporaryObject(objectUnderTest, testCase, {
            contentHeight: 540
        });
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

    function visibleSectionTexts(listView): list<string> {
        const headers = [];
        for (let i = 0; i < listView.contentItem.children.length; i++) {
            const child = listView.contentItem.children[i];
            if (child.objectName === "sectionHeader" && child.visible) {
                headers.push(child);
            }
        }
        headers.sort((left, right) => left.y - right.y);
        return headers.map(header => header.text);
    }

    function test_showsAllShortcutsInitially(): void {
        const dialog = makeDialog();
        const listView = find(dialog, "shortcutsListView");

        verify(listView.count > 0);
        compare(visibleSectionTexts(listView)[0], "mpvQC");
    }

    function test_searchFiltersList(): void {
        const dialog = makeDialog();
        const listView = find(dialog, "shortcutsListView");
        const searchField = find(dialog, "searchField");
        const initialCount = listView.count;

        searchField.text = "fullscreen";
        tryCompare(listView, "count", 1);

        searchField.text = "";
        tryCompare(listView, "count", initialCount);
    }

    function test_sectionHeadersFollowFilter(): void {
        const dialog = makeDialog();
        const listView = find(dialog, "shortcutsListView");
        const searchField = find(dialog, "searchField");

        searchField.text = "screenshot";
        tryCompare(listView, "count", 2);

        tryVerify(() => {
            const sections = visibleSectionTexts(listView);
            return sections.length === 1 && sections[0] === "Video";
        });
    }

    function test_emptyStateShownWhenNothingMatches(): void {
        const dialog = makeDialog();
        const searchField = find(dialog, "searchField");
        const emptyState = find(dialog, "emptyState");

        verify(!emptyState.visible);

        searchField.text = "does not exist";
        tryVerify(() => emptyState.visible);

        const listView = find(dialog, "shortcutsListView");
        const position = emptyState.mapToItem(listView, 0, 0);
        verify(position.y > 0);
        verify(position.y + emptyState.height < listView.height);

        searchField.text = "";
        tryVerify(() => !emptyState.visible);
    }

    function test_searchMatchesChords(): void {
        const dialog = makeDialog();
        const listView = find(dialog, "shortcutsListView");
        const searchField = find(dialog, "searchField");

        searchField.text = "ctrl+n";
        tryCompare(listView, "count", 1);
    }
}
