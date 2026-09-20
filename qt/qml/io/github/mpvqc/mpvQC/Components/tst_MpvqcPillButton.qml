// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    name: "MpvqcPillButton"
    width: 400
    height: 400
    visible: true
    when: windowShown

    function init(): void {
        failOnWarning(/.*/);
    }

    function makeControl(component: Component, properties = {}): AbstractButton {
        const control = createTemporaryObject(component, testCase, properties);
        verify(control);
        verify(waitForRendering(control));
        return control;
    }

    function variants(): var {
        return [
            {
                tag: "choice",
                component: _choice
            },
            {
                tag: "tab",
                component: _tab
            }
        ];
    }

    function test_sharedGeometryAndTypography(): void {
        const choice = makeControl(_choice);
        const tab = makeControl(_tab);
        compare(choice.height, 48);
        compare(tab.height, choice.height);
        compare(tab.implicitWidth, choice.implicitWidth);
        compare(tab.contentItem.font, choice.contentItem.font);
        compare(choice.contentItem.font.weight, Font.Normal);
        compare(choice.contentItem.padding, 10);
        compare(tab.contentItem.padding, choice.contentItem.padding);
        compare(choice.background.height, choice.height);
        compare(tab.background.height, tab.height);
    }

    function test_labelsWrapAndGrow_data(): var {
        return variants();
    }

    function test_labelsWrapAndGrow(data): void {
        const control = makeControl(data.component, {
            width: 100
        });
        const originalHeight = control.height;
        control.text = "AnUnbrokenTranslatedLabelThatMustWrapAcrossSeveralLines";
        tryVerify(() => control.height > originalHeight);
        verify(control.contentItem.lineCount > 1);
        verify(control.contentItem.contentWidth <= control.contentItem.width - 2 * control.contentItem.padding + 1);
        verify(control.contentItem.contentHeight <= control.contentItem.height - 2 * control.contentItem.padding + 1);
    }

    function test_stateColorsAndKeyboardFocus_data(): var {
        return variants();
    }

    function test_stateColorsAndKeyboardFocus(data): void {
        const control = makeControl(data.component);
        compare(control.contentItem.color, MpvqcAppearance.palette.foreground);
        compare(control.background.color, Qt.rgba(0, 0, 0, 0));
        control.checked = true;
        tryCompare(control.contentItem, "color", MpvqcAppearance.palette.accent);
        compare(control.background.color, Qt.alpha(MpvqcAppearance.palette.accent, 0.15));

        control.forceActiveFocus(Qt.TabFocusReason);
        tryCompare(control, "visualFocus", true);
        compare(control.background.border.width, 2);

        control.enabled = false;
        tryCompare(control.contentItem, "color", MpvqcAppearance.palette.hint);
    }

    function test_labelsRenderLiterally_data(): var {
        return variants();
    }

    function test_labelsRenderLiterally(data): void {
        const control = makeControl(data.component, {
            text: "<b>Choice</b>"
        });
        compare(control.contentItem.textFormat, Text.PlainText);
        compare(control.contentItem.text, "<b>Choice</b>");
    }

    Component {
        id: _choice

        MpvqcPillButton {
            text: "Choice"
        }
    }

    Component {
        id: _tab

        MpvqcPillTabButton {
            text: "Choice"
        }
    }
}
