// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcImportDocumentsFileDialog"

    Component {
        id: objectUnderTest

        MpvqcImportDocumentsFileDialog {
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
