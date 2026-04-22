// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtTest
import QtQuick

TestCase {
    id: testCase

    width: 1280
    height: 720
    visible: true
    when: windowShown
    name: "MpvqcFileDialogLoader"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcFileDialogLoader {}
    }

    function makeControl(): MpvqcFileDialogLoader {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            cleanupDelay: 0
        });
        verify(control);
        return control;
    }

    function makeSpy(target: MpvqcFileDialogLoader, signalName: string): SignalSpy {
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: target,
            signalName: signalName
        });
        verify(spy);
        return spy;
    }

    function waitUntilOpened(control: Item): void {
        tryVerify(() => control.item);
        tryVerify(() => control.item.visible);
    }

    function test_openDocumentSaveDialog() {
        const control = makeControl();
        control.openDocumentSaveDialog();
        waitUntilOpened(control);
    }

    function test_openExtendedDocumentExportDialog() {
        const control = makeControl();
        control.openExtendedDocumentExportDialog("file:///tmp/template.txt");
        waitUntilOpened(control);
    }

    function test_openImportQcDocumentsDialog() {
        const control = makeControl();
        control.openImportQcDocumentsDialog();
        waitUntilOpened(control);
    }

    function test_openImportSubtitlesDialog() {
        const control = makeControl();
        control.openImportSubtitlesDialog();
        waitUntilOpened(control);
    }

    function test_openImportVideoDialog() {
        const control = makeControl();
        control.openImportVideoDialog();
        waitUntilOpened(control);
    }

    function test_dialogClosed() {
        const control = makeControl();
        const spy = makeSpy(control, "dialogClosed");

        control.openImportQcDocumentsDialog();
        waitUntilOpened(control);
        if (Qt.platform.os === "windows") {
            // We run into crashs on Windows if we close the dialog immediately after it has been opened.
            wait(1000);
        }
        control.item.close();

        tryVerify(() => !control.item, 1000);
        compare(spy.count, 1);
    }
}
