// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Python

TestCase {
    id: testCase

    width: 1280
    height: 720
    visible: true
    when: windowShown
    name: "MpvqcMessageBoxLoader"

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}

    Component {
        id: objectUnderTest

        MpvqcMessageBoxLoader {}
    }

    function makeControl(): MpvqcMessageBoxLoader {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        return control;
    }

    function waitUntilOpened(control: Item): void {
        tryVerify(() => control.item);
        waitForRendering(control.item?.contentItem);
        tryVerify(() => control.item.opened);
    }

    function test_openMessageBox_data(): var {
        return [
            {
                tag: "custom-export",
                open: control => control.openMessageBox(MpvqcMessageBoxKind.MessageBoxKind.CUSTOM_EXPORT),
                objectName: "customExportMessageBox"
            },
            {
                tag: "export-error",
                open: control => control.openExportErrorMessageBox("message", 1),
                objectName: "exportErrorMessageBox"
            },
            {
                tag: "quit",
                open: control => control.openMessageBox(MpvqcMessageBoxKind.MessageBoxKind.QUIT),
                objectName: "quitMessageBox"
            },
            {
                tag: "reset",
                open: control => control.openMessageBox(MpvqcMessageBoxKind.MessageBoxKind.RESET),
                objectName: "resetMessageBox"
            },
            {
                tag: "version-check",
                open: control => control.openMessageBox(MpvqcMessageBoxKind.MessageBoxKind.VERSION_CHECK),
                objectName: "versionCheckMessageBox"
            }
        ];
    }

    function test_openMessageBox(data): void {
        const control = makeControl();

        data.open(control);

        waitUntilOpened(control);
        compare(control.item.objectName, data.objectName);
        testCase.bridge.waitForBackgroundJobs();
    }
}
