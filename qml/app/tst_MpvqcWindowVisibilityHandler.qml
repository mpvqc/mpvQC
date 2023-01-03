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
import QtTest


TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: 'MpvqcWindowVisibilityHandler'



    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcWindowVisibilityHandler {
            readonly property int cNORMAL: 1
            readonly property int cMAXIMIZED: 2
            readonly property int cFULLSCREEN: 3
            property int visibility: -1

            mpvqcApplication: QtObject {
                property bool fullscreen: false
                property bool maximized: false
                property bool wasMaximizedBefore: false
                function showNormal() { visibility = cNORMAL }
                function showMaximized() { visibility = cMAXIMIZED }
                function showFullScreen() { visibility = cFULLSCREEN }
            }
        }
    }

    function test_toggleMaximized() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.maximized = false
        control.toggleMaximized()
        compare(control.visibility, control.cMAXIMIZED)

        control.maximized = true
        control.toggleMaximized()
        compare(control.visibility, control.cNORMAL)
    }

    function test_toggleFullScreen() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.fullscreen = false
        control.wasMaximizedBefore = false
        control.toggleFullScreen()
        compare(control.visibility, control.cFULLSCREEN)

        control.fullscreen = true
        control.wasMaximizedBefore = false
        control.toggleFullScreen()
        compare(control.visibility, control.cNORMAL)

        control.fullscreen = false
        control.wasMaximizedBefore = true
        control.toggleFullScreen()
        compare(control.visibility, control.cFULLSCREEN)

        control.fullscreen = true
        control.wasMaximizedBefore = true
        control.toggleFullScreen()
        compare(control.visibility, control.cMAXIMIZED)
    }

}
