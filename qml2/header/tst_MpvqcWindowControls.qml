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


import QtQuick.Controls
import QtTest


MpvqcWindowControls {
    id: objectUnderTest

    width: 400
    height: 400

    property bool minimizeFuncCalled: false
    property bool toggleMaximizedFuncCalled: false
    property bool closeFuncCalled: false

    mpvqcApplication: ApplicationWindow {
        property alias maximized: objectUnderTest.toggleMaximizedFuncCalled

        function showMinimized() { objectUnderTest.minimizeFuncCalled = true }
        function toggleMaximized() { objectUnderTest.toggleMaximizedFuncCalled = !objectUnderTest.toggleMaximizedFuncCalled }
        function close() { objectUnderTest.closeFuncCalled = true }
    }

    TestCase {
        name: "MpvqcWindowControls"
        when: windowShown

        function cleanup() {
            objectUnderTest.minimizeFuncCalled = false
            objectUnderTest.toggleMaximizedFuncCalled = false
            objectUnderTest.closeFuncCalled = false
        }

        function test_minimize() {
            mouseClick(objectUnderTest.minimizeButton)
            verify(objectUnderTest.minimizeFuncCalled)
        }

        function test_maximize_data() {
            return [
                { maximizedInitial: false, iconSubstring: 'open_in_full_black', tag: 'maximize' },
                { maximizedInitial: true, iconSubstring: 'close_fullscreen_black', tag: 'minimize' },
            ]
        }

        function test_maximize(data) {
            objectUnderTest.mpvqcApplication.maximized = data.maximizedInitial
            compare(objectUnderTest.mpvqcApplication.maximized, data.maximizedInitial)
            verify(objectUnderTest.maximizeButton.icon.source.toString().includes(data.iconSubstring))
        }

        function test_close() {
            mouseClick(objectUnderTest.closeButton)
            verify(objectUnderTest.closeFuncCalled)
        }

    }

}
