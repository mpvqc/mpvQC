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

        mpvqcApplication: QtObject {
            property int windowRadius: 12
            property var mpvqcMpvPlayerPropertiesPyObject: QtObject {
                property string mpv_version: 'any-version'
                property string ffmpeg_version: 'any-version'
            }
        }
    }

    TestCase {
        name: "MpvqcMenuHelp"
        when: windowShown

        function cleanup() {
            _factoryMock.createObjectCalled = false
            _dialogMock.openCalled = false

            objectUnderTest.updateAction.factory = undefined
            objectUnderTest.shortcutAction.factory = undefined
            objectUnderTest.aboutAction.factory = undefined
        }

        QtObject {
            id: _factoryMock
            property bool createObjectCalled: false
            function createObject() { createObjectCalled = true; return _dialogMock }
        }

        QtObject {
            id: _dialogMock
            property bool openCalled: false
            signal closed()
            function open() { openCalled = true }
        }

        function test_update() {
            objectUnderTest.updateAction.factory = _factoryMock
            objectUnderTest.updateAction.trigger()
            verify(_factoryMock.createObjectCalled)
            verify(_dialogMock.openCalled)
        }

        function test_shortcuts() {
            objectUnderTest.shortcutAction.factory = _factoryMock
            objectUnderTest.shortcutAction.trigger()
            verify(_factoryMock.createObjectCalled)
            verify(_dialogMock.openCalled)
        }

        function test_about() {
            objectUnderTest.aboutAction.factory = _factoryMock
            objectUnderTest.aboutAction.trigger()
            verify(_factoryMock.createObjectCalled)
            verify(_dialogMock.openCalled)
        }

    }

}
