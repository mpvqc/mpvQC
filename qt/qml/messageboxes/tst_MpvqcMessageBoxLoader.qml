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
    name: "MpvqcMessageBoxLoader"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcMessageBoxLoader {}
    }

    function makeControl(): MpvqcMessageBoxLoader {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        return control;
    }

    function makeSpy(target: MpvqcMessageBoxLoader, signalName: string): SignalSpy {
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: target,
            signalName: signalName
        });
        verify(spy);
        return spy;
    }

    function waitUntilOpened(control: Item): void {
        tryVerify(() => control.item);
        waitForRendering(control.item?.contentItem);
        tryVerify(() => control.item.opened);
    }

    function test_openDocumentNotCompatibleMessageBox() {
        const control = makeControl();
        control.openDocumentNotCompatibleMessageBox(["doc1", "doc2"]);
        waitUntilOpened(control);
    }

    function test_openExtendedExportsMessageBox() {
        const control = makeControl();
        control.openExtendedExportsMessageBox();
        waitUntilOpened(control);
    }

    function test_openExtendedExportFailedMessageBox() {
        const control = makeControl();
        control.openExtendedExportFailedMessageBox("message", 1);
        waitUntilOpened(control);
    }

    function test_openQuitMessageBox() {
        const control = makeControl();
        control.openQuitMessageBox();
        waitUntilOpened(control);
    }

    function test_openResetMessageBox() {
        const control = makeControl();
        control.openResetMessageBox();
        waitUntilOpened(control);
    }

    function test_messageBoxClosed() {
        const control = makeControl();
        const spy = makeSpy(control, "messageBoxClosed");

        control.openExtendedExportsMessageBox();
        waitUntilOpened(control);
        control.item.close();

        tryVerify(() => !control.item, 1000);
        compare(spy.count, 1);
    }
}
