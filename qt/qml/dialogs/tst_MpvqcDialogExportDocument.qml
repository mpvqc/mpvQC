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

    readonly property url selectedFile: "file:///selectedFile.txt"
    readonly property url currentFile: "file:///currentFile.txt"
    readonly property url exportTemplate: "file:///exportTemplate.txt"

    name: "MpvqcDialogExportDocument"
    when: windowShown

    Component {
        id: objectUnderTest

        MpvqcDialogExportDocument {}
    }

    Component {
        id: signalSpy

        SignalSpy {}
    }

    function test_normalSave(): void {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            "isExtendedExport": false,
            "selectedFile": testCase.selectedFile
        });
        verify(control);

        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "savePressed"
        });
        verify(spy);

        control.currentFile = testCase.currentFile;
        control.accepted();

        compare(spy.count, 1);
        compare(spy.signalArguments[0][0], testCase.currentFile);
    }

    function test_extendedSave() {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            "isExtendedExport": true,
            "exportTemplate": testCase.exportTemplate
        });
        verify(control);

        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "extendedSavePressed"
        });
        verify(spy);

        control.currentFile = testCase.currentFile;
        control.accepted();

        compare(spy.count, 1);
        compare(spy.signalArguments[0][0], testCase.currentFile);
        compare(spy.signalArguments[0][1], testCase.exportTemplate);
    }
}
