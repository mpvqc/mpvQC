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

    property bool resetCalled: false
    property bool saveCalled: false
    property bool saveAsCalled: false
    property bool closeCalled: false

    MpvqcMenuFile {
        id: objectUnderTest

        mpvqcApplication: QtObject {
            property int windowRadius: 12
            property var mpvqcManager: QtObject {
                function reset() { testHelper.resetCalled = true }
                function save() { testHelper.saveCalled = true }
                function saveAs() { testHelper.saveAsCalled = true }
            }
            property var mpvqcSettings: QtObject {
                property string lastDirectoryDocuments: 'initial directory'
            }
            function close() { closeCalled = true }
        }
    }

    TestCase {
        name: "MpvqcMenuFile"
        when: windowShown

        function test_reset() {
            objectUnderTest.resetAction.trigger()
            verify(testHelper.resetCalled)
        }

        QtObject {
            id: _dialogMock
            property bool openCalled: false
            function open() { openCalled = true }
        }

        function test_import_documents() {
            objectUnderTest.openDocumentsAction.dialog = _dialogMock
            objectUnderTest.openDocumentsAction.trigger()
            verify(_dialogMock.openCalled)
        }

        function test_save() {
            objectUnderTest.saveAction.trigger()
            verify(testHelper.saveCalled)
        }

        function test_saveAs() {
            objectUnderTest.saveAsAction.trigger()
            verify(testHelper.saveAsCalled)
        }

        function close() {
            objectUnderTest.quitAction.trigger()
            verify(testHelper.closeCalled)
        }

    }

}
