// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcOverlayLoader"

    readonly property url stubUrl: Qt.resolvedUrl("MpvqcOverlayStub.qml")

    function makeControl(properties = {}): MpvqcOverlayLoader {
        const control = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(control);
        return control;
    }

    function makeSpy(control, signalName): SignalSpy {
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: signalName
        });
        verify(spy);
        return spy;
    }

    function openStub(control, properties): void {
        control.open(testCase.stubUrl, properties);
        tryVerify(() => control.item);
    }

    function test_openLoadsAndOpensItem(): void {
        const control = makeControl();
        openStub(control);
        compare(control.item.openCalls, 1);
    }

    function test_propertyPassing_data(): var {
        return [
            {
                tag: "with-properties",
                properties: {
                    passedValue: "from-test"
                },
                expected: "from-test"
            },
            {
                tag: "without-properties",
                properties: undefined,
                expected: "initial"
            }
        ];
    }

    function test_propertyPassing(data): void {
        const control = makeControl();
        openStub(control, data.properties);
        compare(control.item.passedValue, data.expected);
    }

    function test_teardown_data(): var {
        return [
            {
                tag: "closed-synchronous",
                trigger: MpvqcOverlayLoader.TeardownTrigger.Closed,
                delay: 0,
                signalName: "closed"
            },
            {
                tag: "closed-delayed",
                trigger: MpvqcOverlayLoader.TeardownTrigger.Closed,
                delay: 25,
                signalName: "closed"
            },
            {
                tag: "accepted-synchronous",
                trigger: MpvqcOverlayLoader.TeardownTrigger.AcceptedOrRejected,
                delay: 0,
                signalName: "accepted"
            },
            {
                tag: "accepted-delayed",
                trigger: MpvqcOverlayLoader.TeardownTrigger.AcceptedOrRejected,
                delay: 25,
                signalName: "accepted"
            },
            {
                tag: "rejected-synchronous",
                trigger: MpvqcOverlayLoader.TeardownTrigger.AcceptedOrRejected,
                delay: 0,
                signalName: "rejected"
            },
            {
                tag: "rejected-delayed",
                trigger: MpvqcOverlayLoader.TeardownTrigger.AcceptedOrRejected,
                delay: 25,
                signalName: "rejected"
            }
        ];
    }

    function test_teardown(data): void {
        const control = makeControl({
            teardownTrigger: data.trigger,
            teardownDelay: data.delay
        });
        const spy = makeSpy(control, "closed");
        openStub(control);
        const item = control.item;

        item.emitTrigger(data.signalName);
        verify(item.aliveAfterEmission);

        if (data.delay === 0) {
            compare(spy.count, 1);
            verify(!control.active);
        } else {
            compare(spy.count, 0);
            verify(control.active);
            tryVerify(() => spy.count === 1);
        }

        compare(spy.count, 1);
        tryVerify(() => !control.item);
        verify(!control.active);
        compare(control.source.toString(), "");
    }

    function test_ignoresNonConfiguredSignals_data(): var {
        return [
            {
                tag: "closed-trigger-ignores-accepted-and-rejected",
                trigger: MpvqcOverlayLoader.TeardownTrigger.Closed,
                signalNames: ["accepted", "rejected"]
            },
            {
                tag: "accepted-or-rejected-trigger-ignores-closed",
                trigger: MpvqcOverlayLoader.TeardownTrigger.AcceptedOrRejected,
                signalNames: ["closed"]
            }
        ];
    }

    function test_ignoresNonConfiguredSignals(data): void {
        const control = makeControl({
            teardownTrigger: data.trigger
        });
        const spy = makeSpy(control, "closed");
        openStub(control);

        for (const signalName of data.signalNames) {
            control.item.emitTrigger(signalName);
        }

        compare(spy.count, 0);
        verify(control.active);
        verify(control.item);
    }

    function test_visibleOnlyWhenFullyLoaded(): void {
        const control = makeControl();
        verify(!control.visible);

        control.open(testCase.stubUrl);
        compare(control.visible, control.status === Loader.Ready);

        tryVerify(() => control.status === Loader.Ready);
        verify(control.visible);

        control.item.emitTrigger("closed");
        verify(!control.visible);
    }

    function test_openCancelsPendingDelayedTeardown(): void {
        const control = makeControl({
            teardownDelay: 25
        });
        const spy = makeSpy(control, "closed");

        openStub(control);
        control.item.emitTrigger("closed");
        compare(spy.count, 0);

        control.open(testCase.stubUrl);

        const guard = createTemporaryObject(timerFactory, testCase, {
            interval: 75,
            running: true
        });
        const guardSpy = makeSpy(guard, "triggered");
        tryVerify(() => guardSpy.count === 1);

        compare(spy.count, 0);
        verify(control.active);
        verify(control.item);
        verify(control.visible);
    }

    function test_reopensAfterTeardown(): void {
        const control = makeControl();
        const spy = makeSpy(control, "closed");

        openStub(control);
        control.item.emitTrigger("closed");
        tryVerify(() => !control.item);

        openStub(control);
        compare(control.item.openCalls, 1);
        control.item.emitTrigger("closed");
        compare(spy.count, 2);
    }

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcOverlayLoader {}
    }

    Component {
        id: timerFactory

        Timer {}
    }
}
