// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    name: "MpvqcAccentColorSwatch"
    width: 200
    height: 200
    visible: true
    when: windowShown

    function makeControl(properties = {}): Item {
        const control = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(control);
        waitForRendering(control);
        return control;
    }

    function makeSpy(target: Item, signalName: string): SignalSpy {
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: target,
            signalName: signalName
        });
        verify(spy);
        return spy;
    }

    function test_theSwatchWearsItsDisplayColor(): void {
        const control = makeControl({
            displayColor: "#00ff00"
        });
        const swatch = findChild(control, "swatch");
        verify(swatch);
        tryCompare(swatch, "color", "#00ff00");
    }

    function test_selectionGrowsAndMorphsTheSwatch(): void {
        const control = makeControl();
        const swatch = findChild(control, "swatch");
        verify(swatch);
        tryCompare(swatch, "width", control.circleSize);
        tryCompare(swatch, "radius", control.circleSize / 2);

        control.selected = true;

        tryCompare(swatch, "width", control.frameSize);
        tryCompare(swatch, "radius", control.selectedRadius);
        verify(swatch.radius < swatch.width / 2, "the selected swatch should read as a rounded square");
    }

    function test_tappingPicksTheAccentColor(): void {
        const control = makeControl({
            accentColor: "#3f51b5"
        });
        const spy = makeSpy(control, "picked");

        mouseClick(control);

        compare(spy.count, 1);
        compare(spy.signalArguments[0][0], "#3f51b5");
    }

    Component {
        id: objectUnderTest

        MpvqcAccentColorSwatch {
            index: 0
            accentColor: "#f44336"
            displayColor: "#f44336"
            selected: false
        }
    }

    Component {
        id: signalSpy

        SignalSpy {}
    }
}
