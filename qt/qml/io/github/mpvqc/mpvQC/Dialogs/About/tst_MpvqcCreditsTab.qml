// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

TestCase {
    id: testCase

    width: 500
    height: 600
    visible: true
    when: windowShown
    name: "MpvqcCreditsTab"

    Component {
        id: objectUnderTest

        MpvqcCreditsTab {
            anchors.fill: parent
        }
    }

    function makeTab(mirrored = false): Item {
        const tab = createTemporaryObject(objectUnderTest, testCase, {
            "LayoutMirroring.enabled": mirrored,
            "LayoutMirroring.childrenInherit": true
        });
        verify(tab);
        return tab;
    }

    function collect(item, objectName, accumulator): var {
        const result = accumulator ?? [];
        if (!item) {
            return result;
        }
        const children = item.children;
        for (let i = 0; children && i < children.length; ++i) {
            const child = children[i];
            if (child.objectName === objectName) {
                result.push(child);
            }
            collect(child, objectName, result);
        }
        return result;
    }

    function test_joinNamesFollowsLayoutDirection_data(): var {
        return [
            {
                tag: "ltr-keeps-order",
                mirrored: false,
                expected: "Anna, Bo, Cy"
            },
            {
                tag: "rtl-reverses-order",
                mirrored: true,
                expected: "Cy, Bo, Anna"
            },
        ];
    }

    function test_joinNamesFollowsLayoutDirection(data): void {
        const tab = makeTab(data.mirrored);
        compare(tab.joinNames(["Anna", "Bo", "Cy"]), data.expected);
    }

    function test_languagesWithoutTranslatorsAreHidden(): void {
        const tab = makeTab(false);
        waitForRendering(tab);

        const rows = collect(tab, "languageCredit");
        verify(rows.length > 0, "no language rows rendered");
        verify(rows.some(row => !row.visible), "expected at least one hidden language");

        for (let i = 0; i < rows.length; ++i) {
            compare(rows[i].visible, rows[i].supportingText !== "");
        }
    }
}
