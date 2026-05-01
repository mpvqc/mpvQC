// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    name: "MpvqcApplicationContent::WindowChrome"
    width: 1280
    height: 720
    visible: true
    when: windowShown

    TestHelpers {
        id: it

        testCase: testCase
    }

    function init(): void {
        it.resetState();
    }

    function test_headerButtonEmitsSignal_data() {
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

    function test_headerButtonEmitsSignal(data): void {
        const control = it.makeControl();
        const button = findChild(control, data.buttonName);
        verify(button, `${data.buttonName} not found`);
        const spy = it.makeSpy(control, data.signalName);

        button.clicked();

        tryVerify(() => spy.count === 1);
    }

    function test_keyEmitsFullScreenSignal_data() {
        return [
            {
                tag: "fkey-toggles-fullscreen",
                key: Qt.Key_F,
                signalName: "toggleFullScreenRequested"
            },
            {
                tag: "esc-disables-fullscreen",
                key: Qt.Key_Escape,
                signalName: "disableFullScreenRequested"
            }
        ];
    }

    function test_keyEmitsFullScreenSignal(data): void {
        const control = it.makeControl();
        const spy = it.makeSpy(control, data.signalName);

        keyClick(data.key);

        tryVerify(() => spy.count === 1);
    }
}
