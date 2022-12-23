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
            property int windowRadius: 12
            property var mpvqcSettings: QtObject {
                property bool backupEnabled: false
                property int backupInterval: 90
                property int theme: Material.Dark
                property int accent: Material.Teal
                property string nickname: 'nickname'
                property bool writeHeaderDate: false
                property bool writeHeaderGenerator: false
                property bool writeHeaderNickname: false
                property bool writeHeaderVideoPath: false
            }
            property var contentItem: Item {}
            property var mpvqcApplicationPathsPyObject: QtObject {
                property url dir_backup: 'file:///hello.txt'
            }
            property var mpvqcFileSystemHelperPyObject: QtObject {
                function url_to_absolute_path(url) { return `${url}-as-abs-path` }
            }
        }
    }

    TestCase {
        name: "MpvqcMenuOptions"
        when: windowShown

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

        function init() {
            _factoryMock.createObjectCalled = false
            _dialogMock.openCalled = false

            objectUnderTest.appearanceAction.factory = undefined
            objectUnderTest.commentTypesAction.factory = undefined
            objectUnderTest.exportAction.factory = undefined
            objectUnderTest.importAction.factory = undefined
            objectUnderTest.backupAction.factory = undefined
        }

        function test_appearance() {
            objectUnderTest.appearanceAction.factory = _factoryMock
            objectUnderTest.appearanceAction.trigger()
            verify(_factoryMock.createObjectCalled)
            verify(_dialogMock.openCalled)
        }

        function test_commentTypes() {
            objectUnderTest.commentTypesAction.factory = _factoryMock
            objectUnderTest.commentTypesAction.trigger()
            verify(_factoryMock.createObjectCalled)
            verify(_dialogMock.openCalled)
        }

        function test_export() {
            objectUnderTest.exportAction.factory = _factoryMock
            objectUnderTest.exportAction.trigger()
            verify(_factoryMock.createObjectCalled)
            verify(_dialogMock.openCalled)
        }

        function test_import() {
            objectUnderTest.importAction.factory = _factoryMock
            objectUnderTest.importAction.trigger()
            verify(_factoryMock.createObjectCalled)
            verify(_dialogMock.openCalled)
        }

        function test_backup() {
            objectUnderTest.backupAction.factory = _factoryMock
            objectUnderTest.backupAction.trigger()
            verify(_factoryMock.createObjectCalled)
            verify(_dialogMock.openCalled)
        }

    }

}
