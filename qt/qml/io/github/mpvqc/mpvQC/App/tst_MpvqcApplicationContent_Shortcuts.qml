// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    name: "MpvqcApplicationContent::Shortcuts"
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
        const dialog = it.find.openedDialog(control, data.dialogName);
        dialog.close();
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

    function test_questionMarkInTextInputDoesNotOpenShortcutsDialog(): void {
        const control = it.makeControl();
        it.comment.add(control, "Translation", "hello");

        const tableView = it.find.tableView(control);
        tableView.forceActiveFocus();
        keyClick(Qt.Key_F, Qt.ControlModifier);

        const searchField = findChild(control, "searchTextField");
        tryVerify(() => searchField?.activeFocus);

        keyClick(Qt.Key_Question);

        tryVerify(() => searchField.text === "?");
        verify(!findChild(control, "shortcutsDialog"), "shortcuts dialog should not open while a text input has focus");
    }

    function test_questionMarkInCommentEditorDoesNotOpenShortcutsDialog(): void {
        const control = it.makeControl();
        const tableView = it.find.tableView(control);
        tableView.addNewComment("Translation");

        tryVerify(() => it.find.commentTextArea(control)?.activeFocus);
        const textArea = it.find.commentTextArea(control);

        keyClick(Qt.Key_Question);

        tryVerify(() => textArea.text === "?");
        verify(!findChild(control, "shortcutsDialog"), "shortcuts dialog should not open while editing a comment");
    }

    function test_escapeClosesAppearanceDialogThenSearchBox(): void {
        const control = it.makeControl();
        it.comment.add(control, "Translation", "hello");

        const tableView = it.find.tableView(control);
        tableView.forceActiveFocus();
        keyClick(Qt.Key_F, Qt.ControlModifier);
        tryVerify(() => findChild(control, "searchBoxPopup")?.searchActive);

        it.menu.trigger(control, "optionsMenu", "openAppearanceDialogMenuItem");
        it.find.openedDialog(control, "appearanceDialog");

        keyClick(Qt.Key_Escape);
        it.expect.dialogClosed(control, "appearanceDialog");
        verify(findChild(control, "searchBoxPopup")?.searchActive, "search box should remain open after first Escape");
        tryVerify(() => it.find.tableView(control).commentList.activeFocus);

        keyClick(Qt.Key_Escape);
        tryVerify(() => !findChild(control, "searchBoxPopup")?.searchActive);
    }
}
