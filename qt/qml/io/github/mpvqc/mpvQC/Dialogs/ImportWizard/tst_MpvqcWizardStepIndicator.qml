// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Python

TestCase {
    id: testCase

    width: 600
    height: 80
    visible: true
    when: windowShown
    name: "MpvqcWizardStepIndicator"

    Component {
        id: objectUnderTest

        MpvqcWizardStepIndicator {
            anchors.fill: parent
        }
    }

    Component {
        id: signalSpy

        SignalSpy {}
    }

    function makeControl(properties = {}): Item {
        const indicator = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(indicator);
        return indicator;
    }

    function makeSpy(target: Item, signalName: string): SignalSpy {
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: target,
            signalName: signalName
        });
        verify(spy);
        return spy;
    }

    readonly property var allKinds: [MpvqcImportWizardStepKind.StepKind.ERRORS, MpvqcImportWizardStepKind.StepKind.SESSION, MpvqcImportWizardStepKind.StepKind.VIDEO, MpvqcImportWizardStepKind.StepKind.SUBTITLES,]

    function collect(root: Item, objectName: string): list<Item> {
        const found = [];
        function visit(item: Item): void {
            if (!item) {
                return;
            }
            if (item.objectName === objectName) {
                found.push(item);
            }
            const kids = item.children;
            if (kids) {
                for (let i = 0; i < kids.length; i++) {
                    visit(kids[i]);
                }
            }
        }
        visit(root);
        return found;
    }

    function test_hiddenWhenFewerThanTwoSteps_data() {
        return [
            {
                tag: "zero",
                kinds: [],
                expectVisible: false
            },
            {
                tag: "one",
                kinds: [MpvqcImportWizardStepKind.StepKind.ERRORS],
                expectVisible: false
            },
            {
                tag: "two",
                kinds: [MpvqcImportWizardStepKind.StepKind.ERRORS, MpvqcImportWizardStepKind.StepKind.VIDEO],
                expectVisible: true
            },
            {
                tag: "four",
                kinds: testCase.allKinds,
                expectVisible: true
            },
        ];
    }

    function test_hiddenWhenFewerThanTwoSteps(data): void {
        const indicator = makeControl({
            stepKinds: data.kinds,
            currentStepIndex: 0
        });
        compare(indicator.visible, data.expectVisible);
    }

    function test_activeStateIconCountsReflectStepState_data() {
        return [
            {
                tag: "first-current",
                currentStepIndex: 0,
                expectCompleted: 0,
                expectUpcoming: 2
            },
            {
                tag: "middle-current",
                currentStepIndex: 1,
                expectCompleted: 1,
                expectUpcoming: 1
            },
            {
                tag: "last-current",
                currentStepIndex: 2,
                expectCompleted: 2,
                expectUpcoming: 0
            },
        ];
    }

    function test_activeStateIconCountsReflectStepState(data): void {
        const indicator = makeControl({
            stepKinds: [MpvqcImportWizardStepKind.StepKind.ERRORS, MpvqcImportWizardStepKind.StepKind.SESSION, MpvqcImportWizardStepKind.StepKind.VIDEO],
            currentStepIndex: data.currentStepIndex
        });
        waitForRendering(indicator);
        function activeCount(objectName: string): int {
            return collect(indicator, objectName).filter(i => i.active).length;
        }
        compare(activeCount("currentStateIcon"), 1);
        compare(activeCount("completedStateIcon"), data.expectCompleted);
        compare(activeCount("upcomingStateIcon"), data.expectUpcoming);
    }

    function test_clickingEntryEmitsStepClicked(): void {
        const indicator = makeControl({
            stepKinds: testCase.allKinds,
            currentStepIndex: 0
        });
        waitForRendering(indicator);
        const spy = makeSpy(indicator, "stepClicked");
        const entries = collect(indicator, "stepEntry");
        compare(entries.length, 4);
        mouseClick(entries[2]);
        compare(spy.count, 1);
        compare(spy.signalArguments[0][0], 2);
    }

    function test_connectorHiddenOnLastEntryOnly(): void {
        const indicator = makeControl({
            stepKinds: [MpvqcImportWizardStepKind.StepKind.ERRORS, MpvqcImportWizardStepKind.StepKind.SESSION, MpvqcImportWizardStepKind.StepKind.VIDEO],
            currentStepIndex: 0
        });
        waitForRendering(indicator);
        const connectors = collect(indicator, "stepConnector");
        compare(connectors.length, 3);
        verify(connectors[0].visible);
        verify(connectors[1].visible);
        verify(!connectors[2].visible);
    }
}
