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


Item {
    id: testHelper
    width: 400
    height: 400

    property bool updateActionCalled: false

    MpvqcMenuHelp {
        id: objectUnderTest

        mpvqcApplication: QtObject {}
    }

    TestCase {
        name: "MpvqcMenuHelp"
        when: windowShown

        function cleanup() {
            _dialogMock.openCalled = false
        }

        QtObject {
            id: _dialogMock
            property bool openCalled: false
            function open() { openCalled = true }
        }

        function test_update() {
            objectUnderTest.updateAction.dialog = _dialogMock
            objectUnderTest.updateAction.trigger()
            verify(_dialogMock.openCalled)
        }

        function test_shortcuts() {
            objectUnderTest.shortcutAction.dialog = _dialogMock
            objectUnderTest.shortcutAction.trigger()
            verify(_dialogMock.openCalled)
        }

        function test_about() {
            objectUnderTest.aboutAction.dialog = _dialogMock
            objectUnderTest.aboutAction.trigger()
            verify(_dialogMock.openCalled)
        }

    }

}
