// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

import io.github.mpvqc.mpvQC.Python

TestCase {
    id: testCase

    width: 500
    height: 600
    visible: true
    when: windowShown
    name: "MpvqcLicensesTab"

    Component {
        id: objectUnderTest

        MpvqcLicensesTab {
            anchors.fill: parent
            viewModel: MpvqcAboutDialogViewModel {}
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

    function test_joinDetailsFollowsLayoutDirection_data(): var {
        return [
            {
                tag: "ltr-version-first",
                mirrored: false,
                expected: "1.0 · GPL-2.0+"
            },
            {
                tag: "rtl-licence-first",
                mirrored: true,
                expected: "GPL-2.0+ · 1.0"
            },
        ];
    }

    function test_joinDetailsFollowsLayoutDirection(data): void {
        const tab = makeTab(data.mirrored);
        compare(tab.joinDetails(["1.0", "GPL-2.0+"]), data.expected);
    }
}
