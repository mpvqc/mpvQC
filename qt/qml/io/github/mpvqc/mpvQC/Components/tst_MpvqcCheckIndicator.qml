// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    name: "MpvqcCheckIndicator"
    width: 400
    height: 400
    visible: true
    when: windowShown

    function buildControl(properties = {}): Item {
        const control = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(control);
        return control;
    }

    function makeControl(properties = {}): Item {
        const control = buildControl(properties);
        waitForRendering(control);
        return control;
    }

    function test_states_data(): list<var> {
        return [
            {
                tag: "unchecked",
                checked: false,
                partial: false,
                checkMarkScale: 0,
                dashScale: 0,
                outlineWidth: 2
            },
            {
                tag: "checked",
                checked: true,
                partial: false,
                checkMarkScale: 1,
                dashScale: 0,
                outlineWidth: 0
            },
            {
                tag: "partial",
                checked: false,
                partial: true,
                checkMarkScale: 0,
                dashScale: 1,
                outlineWidth: 0
            },
            {
                tag: "checked and partial",
                checked: true,
                partial: true,
                checkMarkScale: 1,
                dashScale: 0,
                outlineWidth: 0
            },
        ];
    }

    function test_states(data): void {
        const control = makeControl({
            checked: data.checked,
            partial: data.partial
        });
        const checkMark = findChild(control, "checkMark");
        verify(checkMark);
        const dash = findChild(control, "partialDash");
        verify(dash);

        compare(checkMark.scale, data.checkMarkScale);
        compare(dash.scale, data.dashScale);
        compare(control.border.width, data.outlineWidth);
    }

    function test_uncheckedTheSquareIsHollow(): void {
        const control = makeControl();
        tryCompare(control, "color", Qt.color("transparent"));
        tryCompare(control.border, "color", MpvqcAppearance.palette.hint);
    }

    function test_filledStates_data(): list<var> {
        return [
            {
                tag: "checked",
                checked: true,
                partial: false
            },
            {
                tag: "partial",
                checked: false,
                partial: true
            },
        ];
    }

    function test_filledStates(data): void {
        const control = makeControl({
            checked: data.checked,
            partial: data.partial
        });
        tryCompare(control, "color", MpvqcAppearance.palette.accent);
    }

    function test_checkingShowsTheCheckMark(): void {
        const control = makeControl();
        const checkMark = findChild(control, "checkMark");
        verify(checkMark);

        control.checked = true;

        tryCompare(checkMark, "scale", 1);
        tryCompare(control, "color", MpvqcAppearance.palette.accent);
    }

    function test_uncheckingHidesTheCheckMark(): void {
        const control = makeControl({
            checked: true
        });
        const checkMark = findChild(control, "checkMark");
        verify(checkMark);

        control.checked = false;

        tryCompare(checkMark, "scale", 0);
        tryCompare(control, "color", Qt.color("transparent"));
    }

    function test_theCheckMarkReplacesTheDash(): void {
        const control = makeControl({
            partial: true
        });
        const checkMark = findChild(control, "checkMark");
        verify(checkMark);
        const dash = findChild(control, "partialDash");
        verify(dash);

        control.checked = true;

        tryCompare(checkMark, "scale", 1);
        tryCompare(dash, "scale", 0);
    }

    function test_clearingThePartialStateEmptiesTheSquare(): void {
        const control = makeControl({
            partial: true
        });
        const dash = findChild(control, "partialDash");
        verify(dash);

        control.partial = false;

        tryCompare(dash, "scale", 0);
        tryCompare(control, "color", Qt.color("transparent"));
        compare(control.border.width, 2);
    }

    function test_nothingAnimatesOnConstruction_data(): list<var> {
        return [
            {
                tag: "unchecked",
                checked: false,
                partial: false
            },
            {
                tag: "checked",
                checked: true,
                partial: false
            },
            {
                tag: "partial",
                checked: false,
                partial: true
            },
        ];
    }

    function test_nothingAnimatesOnConstruction(data): void {
        const control = buildControl({
            checked: data.checked,
            partial: data.partial
        });
        const pop = findChild(control, "popAnimation");
        verify(pop);
        const checkMark = findChild(control, "checkMark");
        verify(checkMark);
        const dash = findChild(control, "partialDash");
        verify(dash);

        verify(!pop.running);
        compare(control.scale, 1);
        compare(checkMark.scale, data.checked ? 1 : 0);
        compare(dash.scale, !data.checked && data.partial ? 1 : 0);
    }

    Component {
        id: objectUnderTest

        MpvqcCheckIndicator {}
    }
}
