// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

TestCase {
    id: testCase

    name: "MpvqcAppearanceDialog"
    width: 600
    height: 600
    visible: true
    when: windowShown

    readonly property var preferences: ["system", "light", "dark"]

    function openDialog(mirrored: bool): Dialog {
        const dlg = createTemporaryObject(_dialog, testCase, {
            highlightMoveDuration: 0
        });
        verify(dlg);
        dlg.open();
        tryCompare(dlg, "opened", true);
        if (mirrored) {
            for (const property of ["LayoutMirroring.enabled", "LayoutMirroring.childrenInherit"]) {
                const binding = createTemporaryObject(_mirror, testCase, {
                    target: dlg.contentItem,
                    property: property
                });
                verify(binding);
            }
        }
        waitForRendering(dlg.contentItem);
        return dlg;
    }

    function section(dlg: Dialog): Item {
        const item = findChild(dlg.contentItem, "colorSchemePreferenceSection");
        verify(item);
        return item;
    }

    function swatch(dlg: Dialog, preference: string): Item {
        const item = findChild(dlg.contentItem, `colorSchemePreferenceSwatch_${preference}`);
        verify(item);
        return item;
    }

    function swatchCenterX(dlg: Dialog, preference: string): real {
        const item = testCase.swatch(dlg, preference);
        return testCase.section(dlg).mapFromItem(item, item.width / 2, 0).x;
    }

    function ringCenterX(dlg: Dialog): real {
        const ring = findChild(dlg.contentItem, "colorSchemePreferenceSelectionRing");
        verify(ring);
        return testCase.section(dlg).mapFromItem(ring, ring.width / 2, 0).x;
    }

    function closeRestoringSettings(dlg: Dialog): void {
        dlg.reject();
        tryCompare(dlg, "visible", false);
    }

    function test_rtlSwatchRowMirrorsTheLtrOne(): void {
        const ltr = testCase.openDialog(false);
        const width = testCase.section(ltr).width;
        const ltrCenters = testCase.preferences.map(preference => testCase.swatchCenterX(ltr, preference));
        testCase.closeRestoringSettings(ltr);

        const rtl = testCase.openDialog(true);
        compare(testCase.section(rtl).width, width);

        for (let i = 0; i < testCase.preferences.length; i++) {
            const preference = testCase.preferences[i];
            const actual = testCase.swatchCenterX(rtl, preference);
            const expected = width - ltrCenters[i];
            fuzzyCompare(actual, expected, 1);
        }
    }

    function test_theRingSurroundsTheSelectedSwatch_data() {
        return [
            {
                tag: "ltr",
                mirrored: false
            },
            {
                tag: "rtl",
                mirrored: true
            },
        ];
    }

    function test_theRingSurroundsTheSelectedSwatch(data): void {
        const dlg = testCase.openDialog(data.mirrored);

        mouseClick(testCase.swatch(dlg, "dark"));

        tryCompare(dlg.viewModel, "colorSchemePreferenceIndex", 2);
        tryVerify(() => Math.abs(testCase.ringCenterX(dlg) - testCase.swatchCenterX(dlg, "dark")) <= 1);

        testCase.closeRestoringSettings(dlg);
    }

    Component {
        id: _dialog

        MpvqcAppearanceDialog {}
    }

    Component {
        id: _mirror

        Binding {
            value: true
        }
    }
}
