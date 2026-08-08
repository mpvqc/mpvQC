// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls // qmllint disable unused-imports
import QtTest

TestCase {
    id: testCase

    name: "MpvqcWizardStepPager"
    width: 400
    height: 200
    visible: true
    when: windowShown

    readonly property var stepNames: ["Errors", "Session", "Video", "Subtitles"]

    function makeControl(properties = {}): Item {
        const control = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(control);
        waitForRendering(control);
        return control;
    }

    function makeSpy(target, signalName: string): SignalSpy {
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: target,
            signalName: signalName
        });
        verify(spy);
        return spy;
    }

    function dots(control: Item): var {
        const found = [];
        for (let index = 0; index < control.children.length; index++) {
            const child = control.children[index];
            if (child.objectName === "pagerDot") {
                found.push(child);
            }
        }
        return found;
    }

    function test_thePagerShowsOneDotPerStep(): void {
        const control = makeControl({
            currentStepIndex: 0
        });
        compare(dots(control).length, testCase.stepNames.length);
    }

    function test_eachDotIsNamedByItsTooltip(): void {
        const control = makeControl({
            currentStepIndex: 0
        });
        const names = dots(control).map(dot => dot.ToolTip.text);
        compare(names, testCase.stepNames);
    }

    function test_clickingADotRequestsThatStep_data(): var {
        return [
            {
                tag: "first",
                currentStepIndex: 2,
                clicked: 0
            },
            {
                tag: "behind",
                currentStepIndex: 3,
                clicked: 1
            },
            {
                tag: "ahead",
                currentStepIndex: 0,
                clicked: 2
            },
            {
                tag: "current",
                currentStepIndex: 3,
                clicked: 3
            },
        ];
    }

    function test_clickingADotRequestsThatStep(data): void {
        const control = makeControl({
            currentStepIndex: data.currentStepIndex
        });
        const spy = makeSpy(control, "stepClicked");

        mouseClick(dots(control)[data.clicked]);

        compare(spy.count, 1);
        compare(spy.signalArguments[0][0], data.clicked);
    }

    Component {
        id: objectUnderTest

        MpvqcWizardStepPager {
            stepNames: testCase.stepNames
        }
    }

    Component {
        id: signalSpy

        SignalSpy {}
    }
}
