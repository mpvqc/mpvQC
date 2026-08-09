// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    name: "MpvqcRadioIndicator"
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

    function test_states_data(): list<var> {
        return [
            {
                tag: "unselected",
                selected: false,
                dotSize: 0,
                outlineWidth: 2
            },
            {
                tag: "selected",
                selected: true,
                dotSize: 8,
                outlineWidth: 0
            },
        ];
    }

    function test_states(data): void {
        const control = makeControl({
            selected: data.selected
        });
        const dot = findChild(control, "radioDot");
        verify(dot);

        compare(dot.width, data.dotSize);
        compare(dot.height, data.dotSize);
        compare(control.border.width, data.outlineWidth);
    }

    function test_unselectedTheCircleIsHollow(): void {
        const control = makeControl();
        tryCompare(control, "color", Qt.color("transparent"));
        tryCompare(control.border, "color", MpvqcAppearance.palette.hint);
    }

    function test_selectedTheCircleWearsTheAccent(): void {
        const control = makeControl({
            selected: true
        });
        tryCompare(control, "color", MpvqcAppearance.palette.accent);
    }

    function test_selectingGrowsTheDot(): void {
        const control = makeControl();
        const dot = findChild(control, "radioDot");
        verify(dot);

        control.selected = true;

        tryCompare(dot, "width", 8);
        tryCompare(control, "color", MpvqcAppearance.palette.accent);
        compare(control.border.width, 0);
    }

    function test_deselectingRemovesTheDot(): void {
        const control = makeControl({
            selected: true
        });
        const dot = findChild(control, "radioDot");
        verify(dot);

        control.selected = false;

        tryCompare(dot, "width", 0);
        tryCompare(control, "color", Qt.color("transparent"));
        compare(control.border.width, 2);
    }

    Component {
        id: objectUnderTest

        MpvqcRadioIndicator {}
    }
}
