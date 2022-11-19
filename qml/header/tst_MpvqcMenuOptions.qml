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
import QtQuick.Controls.Material
import QtTest


Item {
    id: testHelper
    width: 400
    height: 400

    MpvqcMenuOptions {
        id: objectUnderTest

        mpvqcApplication: QtObject {
            property var mpvqcSettings: QtObject {
                property int theme: Material.Dark
                property int accent: Material.Teal
            }
            property var contentItem: Item {}
        }
    }

    TestCase {
        name: "MpvqcMenuOptions"
        when: windowShown

        QtObject {
            id: _dialogMock
            property bool openCalled: false
            function open() { openCalled = true }
        }

        function cleanup() {
            _dialogMock.openCalled = false
        }

        function test_appearance() {
            objectUnderTest.appearanceAction.dialog = _dialogMock
            objectUnderTest.appearanceAction.trigger()
            verify(_dialogMock.openCalled)
        }

        function test_commentTypes() {
            objectUnderTest.commentTypesAction.dialog = _dialogMock
            objectUnderTest.commentTypesAction.trigger()
            verify(_dialogMock.openCalled)
        }

        function test_export() {
            objectUnderTest.exportAction.dialog = _dialogMock
            objectUnderTest.exportAction.trigger()
            verify(_dialogMock.openCalled)
        }

        function test_backup() {
            objectUnderTest.backupAction.dialog = _dialogMock
            objectUnderTest.backupAction.trigger()
            verify(_dialogMock.openCalled)
        }

    }

}
