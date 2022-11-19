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


Item {
    id: testHelper
    width: 400
    height: 400

    readonly property int withSameInputDevice: 42

    property bool toggleMaximizedCalled: false

    property var mpvqcApplication: ApplicationWindow {
        function toggleMaximized() { testHelper.toggleMaximizedCalled = true }
    }

    MpvqcHeaderTapHandler {
        id: objectUnderTest

        mpvqcApplication: testHelper.mpvqcApplication
    }

    TestCase {
        name: "MpvqcWindowMoveHandler"
        when: windowShown

        function cleanup() {
            testHelper.toggleMaximizedCalled = false
        }

        function test_tap_data() {
            return [
                { taps: 1, called: false, tag: '1x', exec: () => mouseClick(testHelper) },
                { taps: 2, called: true, tag: '2x', exec: () => objectUnderTest.handleDoubleTap() }
                // fixme https://stackoverflow.com/questions/74424370/how-to-unit-test-double-tap-in-taphandler
            ]
        }

        function test_tap(data) {
            data.exec()
            compare(testHelper.toggleMaximizedCalled, data.called)
        }

    }

}
