// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    name: "MpvqcColorSchemeSwatch"
    width: 200
    height: 200
    visible: true
    when: windowShown

    readonly property var systemRow: ({
            preference: "system",
            caption: "System",
            preview: "#f5f2fa",
            alternatePreview: "#121318",
            accent: "",
            selected: false
        })

    readonly property var lightRow: ({
            preference: "light",
            caption: "Light",
            preview: "#f5f2fa",
            alternatePreview: "",
            accent: "#00ff00",
            selected: false
        })

    function makeControl(properties): Item {
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

    function test_captionIsShown(): void {
        const control = makeControl(testCase.systemRow);
        const caption = findChild(control, "caption");
        verify(caption);
        compare(caption.text, "System");
    }

    function test_splitPreviewOnlyWithASecondPreview_data() {
        return [
            {
                tag: "system",
                properties: testCase.systemRow,
                expectSplit: true
            },
            {
                tag: "light",
                properties: testCase.lightRow,
                expectSplit: false
            },
        ];
    }

    function test_splitPreviewOnlyWithASecondPreview(data): void {
        const control = makeControl(data.properties);
        const split = findChild(control, "splitPreview");
        verify(split);
        compare(control.split, data.expectSplit);
        compare(split.visible, data.expectSplit);
    }

    function test_badgeOnlyWithAnAccent_data() {
        return [
            {
                tag: "system",
                properties: testCase.systemRow,
                expectBadge: false
            },
            {
                tag: "light",
                properties: testCase.lightRow,
                expectBadge: true
            },
        ];
    }

    function test_badgeOnlyWithAnAccent(data): void {
        const control = makeControl(data.properties);
        const badge = findChild(control, "accentBadge");
        verify(badge);
        compare(control.badged, data.expectBadge);
        compare(badge.visible, data.expectBadge);
    }

    function test_badgeWearsTheStoredAccent(): void {
        const control = makeControl(testCase.lightRow);
        const badge = findChild(control, "accentBadge");
        verify(badge);
        tryCompare(badge, "color", "#00ff00");
    }

    function test_badgeCrossFadesToANewAccent(): void {
        const control = makeControl(testCase.lightRow);
        const badge = findChild(control, "accentBadge");
        verify(badge);
        tryCompare(badge, "color", "#00ff00");

        control.accent = "#0000ff";

        tryCompare(badge, "color", "#0000ff");
    }

    function test_selectionEmphasizesTheCaption(): void {
        const unselected = makeControl(testCase.lightRow);
        const selected = makeControl(Object.assign({}, testCase.lightRow, {
            selected: true
        }));

        const unselectedCaption = findChild(unselected, "caption");
        const selectedCaption = findChild(selected, "caption");
        verify(unselectedCaption);
        verify(selectedCaption);
        verify(selectedCaption.color !== unselectedCaption.color, "the selected caption should stand out");
        verify(selectedCaption.font.weight > unselectedCaption.font.weight);
    }

    function test_tappingPicksThePreference(): void {
        const control = makeControl(testCase.lightRow);
        const spy = makeSpy(control, "picked");

        mouseClick(control);

        compare(spy.count, 1);
        compare(spy.signalArguments[0][0], "light");
    }

    Component {
        id: objectUnderTest

        MpvqcColorSchemeSwatch {}
    }

    Component {
        id: signalSpy

        SignalSpy {}
    }
}
