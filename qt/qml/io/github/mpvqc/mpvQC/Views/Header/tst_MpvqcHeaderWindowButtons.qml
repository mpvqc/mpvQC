// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    width: 600
    height: 200
    visible: true
    when: windowShown
    name: "MpvqcHeaderWindowButtons"

    Component {
        id: objectUnderTest

        MpvqcHeaderWindowButtons {
            height: 40
            width: testCase.width
        }
    }

    Component {
        id: signalSpy

        SignalSpy {}
    }

    function makeControl(initProperties = {}) {
        const control = createTemporaryObject(objectUnderTest, testCase, initProperties);
        verify(control);
        return control;
    }

    function makeSpy(target, signalName) {
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: target,
            signalName: signalName
        });
        verify(spy);
        return spy;
    }

    function test_clickEmitsSignal_data(): var {
        return [
            {
                tag: "minimize",
                buttonName: "minimizeButton",
                signalName: "minimizeRequested"
            },
            {
                tag: "maximize",
                buttonName: "maximizeButton",
                signalName: "toggleMaximizeRequested"
            },
            {
                tag: "close",
                buttonName: "closeButton",
                signalName: "closeRequested"
            }
        ];
    }

    function test_clickEmitsSignal(data) {
        const control = makeControl();
        const button = findChild(control, data.buttonName);
        const spy = makeSpy(control, data.signalName);

        button.clicked();

        compare(spy.count, 1);
    }

    function test_closeButtonBackgroundColor_data(): var {
        return [
            {
                tag: "windows",
                isWindows: true,
                expected: "#c42c1e"
            },
            {
                tag: "nonWindows",
                isWindows: false,
                expected: MpvqcTheme.control
            }
        ];
    }

    function test_closeButtonBackgroundColor(data) {
        const control = makeControl({
            isWindows: data.isWindows
        });
        const button = findChild(control, "closeButton");

        compare(button.backgroundColor, data.expected);
    }

    function test_closeButtonHoverIconColor_data(): var {
        return [
            {
                tag: "windows",
                isWindows: true,
                expected: "#fffffd"
            },
            {
                tag: "nonWindows",
                isWindows: false,
                expected: MpvqcTheme.background
            }
        ];
    }

    function test_closeButtonHoverIconColor(data) {
        const control = makeControl({
            isWindows: data.isWindows
        });
        const button = findChild(control, "closeButton");

        compare(button.hoverIconColor, data.expected);
    }

    function test_closeButtonIdleIconColor_data(): var {
        return [
            {
                tag: "windows",
                isWindows: true
            },
            {
                tag: "nonWindows",
                isWindows: false
            }
        ];
    }

    function test_closeButtonIdleIconColor(data) {
        const control = makeControl({
            isWindows: data.isWindows
        });
        const button = findChild(control, "closeButton");

        compare(button.idleIconColor, MpvqcTheme.foreground);
    }
}
