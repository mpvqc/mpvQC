// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest
import pyobjects

TestCase {
    id: testCase

    name: "Integration::Shortcuts"
    width: 1280
    height: 720
    visible: true
    when: windowShown

    TestHelpers {
        id: it

        testCase: testCase
    }

    function init(): void {
        it.resetState();
    }

    function test_shortcutOpensDialog_data() {
        return [
            {
                tag: "open",
                key: Qt.Key_O,
                modifiers: Qt.ControlModifier,
                dialogName: "importDocumentsFileDialog"
            },
            {
                tag: "save",
                key: Qt.Key_S,
                modifiers: Qt.ControlModifier,
                dialogName: "saveDocumentFileDialog"
            },
            {
                tag: "saveAs",
                key: Qt.Key_S,
                modifiers: Qt.ControlModifier | Qt.ShiftModifier,
                dialogName: "saveDocumentFileDialog"
            },
            {
                tag: "openVideo",
                key: Qt.Key_O,
                modifiers: Qt.ControlModifier | Qt.AltModifier,
                dialogName: "importVideoFileDialog"
            },
            {
                tag: "shortcuts",
                key: Qt.Key_Question,
                modifiers: Qt.NoModifier,
                dialogName: "shortcutsDialog"
            },
        ];
    }

    function test_shortcutOpensDialog(data): void {
        const control = it.makeControl();
        keyClick(data.key, data.modifiers);
        tryVerify(() => findChild(control, data.dialogName)?.visible);
        findChild(control, data.dialogName).close();
    }

    function test_shortcutEmitsContentSignal_data() {
        return [
            {
                tag: "exit",
                key: Qt.Key_Q,
                modifiers: Qt.ControlModifier,
                signalName: "closeRequested"
            },
            {
                tag: "resize",
                key: Qt.Key_R,
                modifiers: Qt.ControlModifier,
                signalName: "appWindowSizeRequested"
            },
        ];
    }

    function test_shortcutEmitsContentSignal(data): void {
        const control = it.makeControl();
        const spy = it.makeSpy(control, data.signalName);
        keyClick(data.key, data.modifiers);
        tryVerify(() => spy.count === 1);
    }
}
