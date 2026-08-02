// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    name: "MpvqcAppearanceSection"
    width: 400
    height: 400
    visible: true
    when: windowShown

    function makeControl(properties = {}): Item {
        const control = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(control);
        waitForRendering(control);
        return control;
    }

    function test_theTitleIsShown(): void {
        const control = makeControl({
            title: "Color scheme"
        });
        const title = findChild(control, "sectionTitle");
        verify(title);
        compare(title.text, "Color scheme");
    }

    function test_theCardWearsTheSectionCardColorRole(): void {
        const control = makeControl();
        const card = findChild(control, "sectionCard");
        verify(card);
        tryCompare(card, "color", MpvqcAppearance.palette.sectionCard);
    }

    function test_foldingAwayCollapsesTheSection(): void {
        const control = makeControl();
        tryVerify(() => control.implicitHeight > 0);

        control.expanded = false;

        tryCompare(control, "implicitHeight", 0);
        tryCompare(control, "opacity", 0);
        tryVerify(() => !control.visible);
    }

    function test_unfoldingRestoresTheSection(): void {
        const control = makeControl({
            expanded: false
        });
        const content = findChild(control, "sectionContent");
        verify(content);
        tryCompare(control, "implicitHeight", 0);

        control.expanded = true;

        tryVerify(() => control.implicitHeight > content.height);
        tryCompare(control, "opacity", 1);
        verify(control.visible);
    }

    Component {
        id: objectUnderTest

        MpvqcAppearanceSection {
            width: 300

            Rectangle {
                objectName: "sectionContent"

                implicitHeight: 40

                Layout.fillWidth: true
            }
        }
    }
}
