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

    function test_headerForwardsSignal_data() {
        return [
            {
                tag: "toggleMaximize",
                signalName: "toggleMaximizeRequested"
            },
            {
                tag: "windowDrag",
                signalName: "windowDragRequested",
                expectedRootSignal: "startSystemMoveRequested"
            }
        ];
    }

    // Verifies the wiring from MpvqcHeaderView to the composition root.
    // The trigger paths (TapHandler.onDoubleTapped, DragHandler.onActiveChanged)
    // are owned by Qt and not driven through here.
    function test_headerForwardsSignal(data): void {
        const control = it.makeControl();
        const header = findChild(control, "headerView");
        verify(header, "headerView not found");
        const rootSignal = data.expectedRootSignal ?? data.signalName;
        const spy = it.makeSpy(control, rootSignal);

        header[data.signalName]();

        tryVerify(() => spy.count === 1);
    }

    function test_playerDoubleClick_emitsToggleFullScreenRequested(): void {
        const control = it.makeControl();
        const inputArea = findChild(control, "playerInputArea");
        verify(inputArea, "playerInputArea not found");
        tryVerify(() => inputArea.width > 0 && inputArea.height > 0);
        const spy = it.makeSpy(control, "toggleFullScreenRequested");

        mouseDoubleClickSequence(inputArea, inputArea.width / 2, inputArea.height / 2, Qt.LeftButton);

        tryVerify(() => spy.count === 1);
    }
}
