// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

TestCase {
    id: testCase

    width: 400
    height: 200
    visible: true
    when: windowShown
    name: "MpvqcAboutListItem"

    Component {
        id: objectUnderTest

        MpvqcAboutListItem {
            width: 360
            text: "headline"
        }
    }

    Component {
        id: spyComponent

        SignalSpy {}
    }

    function makeControl(properties = {}): Item {
        const control = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(control);
        return control;
    }

    function makeSpy(target, signalName): SignalSpy {
        const spy = createTemporaryObject(spyComponent, testCase, {
            target: target,
            signalName: signalName
        });
        verify(spy);
        return spy;
    }

    function test_linkControlsInteractivityAndIndicator_data(): var {
        return [
            {
                tag: "with-link",
                link: "https://mpvqc.github.io",
                expectedEnabled: true,
                expectedIndicator: true
            },
            {
                tag: "without-link",
                link: "",
                expectedEnabled: false,
                expectedIndicator: false
            },
        ];
    }

    function test_linkControlsInteractivityAndIndicator(data): void {
        const control = makeControl({
            link: data.link
        });
        const indicator = findChild(control, "linkIndicator");
        verify(indicator);

        compare(control.enabled, data.expectedEnabled);
        compare(indicator.visible, data.expectedIndicator);
    }

    function test_supportingLabelHiddenWhenEmpty_data(): var {
        return [
            {
                tag: "empty",
                supportingText: "",
                expectedVisible: false
            },
            {
                tag: "present",
                supportingText: "0.1.0 · GPL-2.0+",
                expectedVisible: true
            },
        ];
    }

    function test_supportingLabelHiddenWhenEmpty(data): void {
        const control = makeControl({
            supportingText: data.supportingText
        });
        const supporting = findChild(control, "supportingLabel");
        verify(supporting);

        compare(supporting.visible, data.expectedVisible);
    }

    function test_clickedEmitsOnlyWhenLinked_data(): var {
        return [
            {
                tag: "linked-is-clickable",
                link: "https://mpvqc.github.io",
                expectedCount: 1
            },
            {
                tag: "unlinked-is-inert",
                link: "",
                expectedCount: 0
            },
        ];
    }

    function test_clickedEmitsOnlyWhenLinked(data): void {
        const control = makeControl({
            link: data.link
        });
        const spy = makeSpy(control, "clicked");

        mouseClick(control);

        compare(spy.count, data.expectedCount);
    }
}
