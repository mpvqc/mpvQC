// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcPlayerInputArea"

    Component {
        id: objectUnderTest

        MpvqcPlayerInputArea {
            width: 200
            height: 200
        }
    }

    Component {
        id: signalSpy

        SignalSpy {
            function invocation(invocation: int): var {
                const inv = signalArguments[invocation];
                return {
                    arg: index => inv[index]
                };
            }
        }
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

    function test_leftClickEmitsPressedAndReleased() {
        const control = makeControl();
        const pressed = makeSpy(control, "leftMousePressed");
        const released = makeSpy(control, "leftMouseReleased");

        mouseClick(control, 50, 50, Qt.LeftButton);

        compare(pressed.count, 1);
        compare(released.count, 1);
    }

    function test_middleClickEmitsMiddlePressed() {
        const control = makeControl();
        const spy = makeSpy(control, "middleMousePressed");

        mouseClick(control, 50, 50, Qt.MiddleButton);

        compare(spy.count, 1);
    }

    function test_backClickEmitsBackPressed() {
        const control = makeControl();
        const spy = makeSpy(control, "backMousePressed");

        mouseClick(control, 50, 50, Qt.BackButton);

        compare(spy.count, 1);
    }

    function test_forwardClickEmitsForwardPressed() {
        const control = makeControl();
        const spy = makeSpy(control, "forwardMousePressed");

        mouseClick(control, 50, 50, Qt.ForwardButton);

        compare(spy.count, 1);
    }

    function test_rightClickEmitsAddNewCommentMenuRequestedAndNothingElse() {
        const control = makeControl();
        const menuSpy = makeSpy(control, "addNewCommentMenuRequested");
        const leftSpy = makeSpy(control, "leftMousePressed");
        const middleSpy = makeSpy(control, "middleMousePressed");

        mouseClick(control, 50, 50, Qt.RightButton);

        compare(menuSpy.count, 1);
        compare(leftSpy.count, 0);
        compare(middleSpy.count, 0);
    }

    function test_wheelUpEmitsWheelScrolledUp() {
        const control = makeControl();
        const spy = makeSpy(control, "wheelScrolledUp");

        mouseWheel(control, 50, 50, 0, 120);

        compare(spy.count, 1);
    }

    function test_wheelDownEmitsWheelScrolledDown() {
        const control = makeControl();
        const spy = makeSpy(control, "wheelScrolledDown");

        mouseWheel(control, 50, 50, 0, -120);

        compare(spy.count, 1);
    }

    function test_mouseMoveEmitsMouseMovedWithPayload() {
        const control = makeControl();
        const spy = makeSpy(control, "mouseMoved");

        mouseMove(control, 42, 17);

        compare(spy.count, 1);
        compare(spy.invocation(0).arg(0), 42);
        compare(spy.invocation(0).arg(1), 17);
    }

    function test_doubleLeftClickEmitsToggleFullScreenRequested() {
        const control = makeControl();
        const spy = makeSpy(control, "toggleFullScreenRequested");

        mouseDoubleClickSequence(control, 50, 50, Qt.LeftButton);

        compare(spy.count, 1);
    }

    function test_pressOnWindowsWithInactiveWindowEmitsActivationRequested() {
        const control = makeControl({
            isWindows: true,
            isWindowActive: false
        });
        const spy = makeSpy(control, "windowActivationRequested");

        mousePress(control, 50, 50, Qt.LeftButton);

        compare(spy.count, 1);
    }

    function test_pressOnWindowsWithActiveWindowDoesNotEmitActivation() {
        const control = makeControl({
            isWindows: true,
            isWindowActive: true
        });
        const spy = makeSpy(control, "windowActivationRequested");

        mousePress(control, 50, 50, Qt.LeftButton);

        compare(spy.count, 0);
    }

    function test_pressOnNonWindowsDoesNotEmitActivation() {
        const control = makeControl({
            isWindows: false,
            isWindowActive: false
        });
        const spy = makeSpy(control, "windowActivationRequested");

        mousePress(control, 50, 50, Qt.LeftButton);

        compare(spy.count, 0);
    }

    function test_cursorHidesAfterTimerWhenFullscreen() {
        const control = makeControl({
            isFullScreen: true
        });
        control.cursorTimer.interval = 5;

        mouseMove(control, 50, 50);
        compare(control.showCursor, true);

        tryCompare(control, "showCursor", false);
        compare(control.cursorShape, Qt.BlankCursor);

        mouseMove(control, 60, 60);
        compare(control.showCursor, true);
        compare(control.cursorShape, Qt.ArrowCursor);
    }

    function test_cursorTimerDoesNotRunWhenNotFullscreen() {
        const control = makeControl({
            isFullScreen: false
        });
        control.cursorTimer.interval = 5;

        mouseMove(control, 50, 50);

        compare(control.cursorTimer.running, false);
        compare(control.showCursor, true);
        compare(control.cursorShape, Qt.ArrowCursor);
    }
}
