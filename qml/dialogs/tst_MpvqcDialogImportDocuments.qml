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
    name: "MpvqcDialogImportDocuments"

    Component {
        id: objectUnderTest

        MpvqcDialogImportDocuments {
            id: __objectUnderTest

            property bool openDocumentsCalled: false

            mpvqcApplication: QtObject {
                property var mpvqcManager: QtObject {
                    function openDocuments(files) {
                        __objectUnderTest.openDocumentsCalled = true;
                    }
                }
                property var mpvqcSettings: QtObject {
                    property string lastDirectoryDocuments: "initial directory"
                }
            }
        }
    }

    function test_import() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.currentFolder = "some directory";
        control.accepted();

        verify(control.openDocumentsCalled);
        verify(!control.mpvqcSettings.lastDirectoryDocuments.toString().includes("initial directory"));
    }
}
