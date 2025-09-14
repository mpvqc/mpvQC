// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

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
