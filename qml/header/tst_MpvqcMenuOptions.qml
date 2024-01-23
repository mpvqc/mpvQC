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


TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: 'MpvqcMenuOptions'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: dialogMock

        QtObject {
            property bool openCalled: false
            signal closed()
            function open() { openCalled = true }
        }
    }

    Component {
        id: factoryMock

        QtObject {
            property bool createObjectCalled: false
            property var dialog
            function createObject() {
                createObjectCalled = true
                dialog = createTemporaryObject(dialogMock, testCase)
                verify(dialog)
                return dialog
            }
        }
    }

    Component {
        id: objectUnderTest

        MpvqcMenuOptions {
            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject {
                    property bool backupEnabled: false
                    property int backupInterval: 90
                    property int theme: Material.Dark
                    property int primary: Material.Teal
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
    }

    function test_clicks() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        let factory

        factory = createTemporaryObject(factoryMock, testCase)
        verify(factory)

        control.appearanceAction.factory = factory
        control.appearanceAction.trigger()
        verify(factory.createObjectCalled)
        verify(factory.dialog.openCalled)


        factory = createTemporaryObject(factoryMock, testCase)
        verify(factory)

        control.commentTypesAction.factory = factory
        control.commentTypesAction.trigger()
        verify(factory.createObjectCalled)
        verify(factory.dialog.openCalled)


        factory = createTemporaryObject(factoryMock, testCase)
        verify(factory)

        control.backupAction.factory = factory
        control.backupAction.trigger()
        verify(factory.createObjectCalled)
        verify(factory.dialog.openCalled)


        factory = createTemporaryObject(factoryMock, testCase)
        verify(factory)

        control.exportAction.factory = factory
        control.exportAction.trigger()
        verify(factory.createObjectCalled)
        verify(factory.dialog.openCalled)


        factory = createTemporaryObject(factoryMock, testCase)
        verify(factory)

        control.importAction.factory = factory
        control.importAction.trigger()
        verify(factory.createObjectCalled)
        verify(factory.dialog.openCalled)


        factory = createTemporaryObject(factoryMock, testCase)
        verify(factory)

        control.editMpvAction.factory = factory
        control.editMpvAction.trigger()
        verify(factory.createObjectCalled)
        verify(factory.dialog.openCalled)


        factory = createTemporaryObject(factoryMock, testCase)
        verify(factory)

        control.editInputAction.factory = factory
        control.editInputAction.trigger()
        verify(factory.createObjectCalled)
        verify(factory.dialog.openCalled)
    }

}
