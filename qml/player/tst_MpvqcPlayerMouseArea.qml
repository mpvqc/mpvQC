/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick
import QtQuick.Controls
import QtTest


Label {
    id: testHelper

    width: 400
    height: 400

    property int moveMouseX: -1;
    property int moveMouseY: -1;
    property bool wheelUp: false
    property bool wheelDown: false
    property bool pressedLeft: false
    property bool pressedMiddle: false
    property bool releasedLeft: false
    property bool toggleFullscreen: false

    MpvqcPlayerMouseArea {
        id: objectUnderTest

        anchors.fill: testHelper
        showCursor: true

        mpvqcApplication: QtObject {
            property bool fullscreen: false
            property var mpvqcMpvPlayerPyObject: QtObject {
                function move_mouse(x, y) { testHelper.moveMouseX = x; testHelper.moveMouseY = y }
                function scroll_up() { testHelper.wheelUp = true }
                function scroll_down() { testHelper.wheelDown = true }
                function press_mouse_left() { testHelper.pressedLeft = true }
                function press_mouse_middle() { testHelper.pressedMiddle = true }
                function release_mouse_left() { testHelper.releasedLeft = true }
            }
            function toggleFullScreen() { testHelper.toggleFullscreen = true }
        }

        TestCase {
            name: "MpvqcPlayerMouseArea"
            when: windowShown

            SignalSpy { id: rightMouseButtonPressedSpy; target: objectUnderTest; signalName: 'rightMouseButtonPressed' }

            function init() {
                objectUnderTest.showCursor = true
                objectUnderTest.mpvqcApplication.fullscreen = false
                objectUnderTest.cursorTimer.interval = 1

                testHelper.moveMouseX = -1
                testHelper.moveMouseY = -1
                testHelper.wheelUp = false
                testHelper.wheelDown = false
                testHelper.pressedLeft = false
                testHelper.pressedMiddle = false
                testHelper.releasedLeft = false
                testHelper.toggleFullscreen = false

                rightMouseButtonPressedSpy.clear()
            }

            function test_hideCursor() {
                verify(objectUnderTest.showCursor)

                objectUnderTest.mpvqcApplication.fullscreen = true

                mouseMove(objectUnderTest, 1, 1)
                mouseMove(objectUnderTest, 2, 2)
                wait(25)

                verify(!objectUnderTest.showCursor)
            }

            function test_mouse_move() {
                mouseMove(objectUnderTest, 1, 1)
                mouseMove(objectUnderTest, 2, 2)
                compare(testHelper.moveMouseX, 2)
                compare(testHelper.moveMouseY, 2)
            }

            function test_scroll_data() {
                return [
                    { tag: 'up', deltaX: 0, deltaY: 1, expectedUp: true, expectedDown: false },
                    { tag: 'down', deltaX: 0, deltaY: -1, expectedUp: false, expectedDown: true },
                ]
            }

            function test_scroll(data) {
                mouseWheel(objectUnderTest, 1, 1, data.deltaX, data.deltaY)
                compare(testHelper.wheelUp, data.expectedUp)
                compare(testHelper.wheelDown, data.expectedDown)
            }

            function test_press_data() {
                return [
                    {
                        tag: 'left',
                        button: Qt.LeftButton,
                        expect: () => { verify(testHelper.pressedLeft) },
                    },
                    {
                        tag: 'middle',
                        button: Qt.MiddleButton,
                        expect: () => { verify(testHelper.pressedMiddle) },
                    },
                    {
                        tag: 'right',
                        button: Qt.RightButton,
                        expect: () => { compare(rightMouseButtonPressedSpy.count, 1) },
                    },
                ]
            }

            function test_press(data) {
                mousePress(objectUnderTest, 1, 1, data.button)
                data.expect()
            }

            function test_release() {
                mouseRelease(objectUnderTest, 1, 1, Qt.LeftButton)
                verify(testHelper.releasedLeft)
            }

            function test_doubleClick() {
                mouseDoubleClickSequence(objectUnderTest)
                verify(testHelper.toggleFullscreen)
            }

        }

    }
}
