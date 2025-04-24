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

    name: "MpvqcMenuFile"
    width: 400
    height: 400
    visible: true
    when: windowShown

    Component {
        id: dialogMock

        QtObject {
            id: __dialogMock

            property bool openCalled: false

            function open() {
                __dialogMock.openCalled = true;
            }
        }
    }

    Component {
        id: objectUnderTest

        MpvqcMenuFile {
            id: __objectUnderTest

            property bool resetCalled: false
            property bool saveCalled: false
            property bool saveAsCalled: false
            property bool closeCalled: false

            mpvqcApplication: QtObject {
                property var mpvqcManager: QtObject {
                    function reset() {
                        __objectUnderTest.resetCalled = true;
                    }

                    function save() {
                        __objectUnderTest.saveCalled = true;
                    }

                    function saveAs() {
                        __objectUnderTest.saveAsCalled = true;
                    }
                }
                property var mpvqcSettings: QtObject {
                    property string lastDirectoryDocuments: "initial directory"
                }

                function close(): void {
                    __objectUnderTest.closeCalled = true;
                }
            }
            extendedExportTemplateModel: []
        }
    }

    function test_reset() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.resetAction.trigger();
        verify(control.resetCalled);
    }

    function test_openDocuments() {
        const dialog = createTemporaryObject(dialogMock, testCase);
        verify(dialog);

        const control = createTemporaryObject(objectUnderTest, testCase, {
            "dialogImportDocuments": dialog
        });
        verify(control);

        control.openDocumentsAction.trigger();
        verify(dialog.openCalled);
    }

    function test_save() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.saveAction.trigger();
        verify(control.saveCalled);
    }

    function test_saveAs() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.saveAsAction.trigger();
        verify(control.saveAsCalled);
    }

    function test_close() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.closeAction.trigger();
        verify(control.closeCalled);
    }
}
