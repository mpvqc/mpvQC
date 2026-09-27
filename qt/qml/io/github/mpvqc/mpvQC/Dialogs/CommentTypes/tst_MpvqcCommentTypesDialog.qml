// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

TestCase {
    id: testCase

    name: "MpvqcCommentTypesDialog"
    width: 600
    height: 900
    visible: true
    when: windowShown

    readonly property TestHelpers helper: TestHelpers {
        testCase: testCase
    }

    function init(): void {
        failOnWarning(/.*(TypeError|Unable to assign|Binding loop).*/);
        helper.bridge.resetState();
    }

    function test_addAppendsRevealsClearsAndRefocuses_data(): var {
        return [
            {
                tag: "button",
                viaButton: true
            },
            {
                tag: "enter",
                viaButton: false
            }
        ];
    }

    function test_addAppendsRevealsClearsAndRefocuses(data): void {
        const dialog = helper.makeDialog();
        for (let i = 1; i <= 4; i++) {
            helper.addType(dialog, `ZZZ Filler ${i}`);
        }
        const list = helper.listView(dialog);
        const field = helper.textField(dialog);
        const addButton = helper.addButton(dialog);
        list.positionViewAtBeginning();
        const before = list.count;

        field.forceActiveFocus();
        field.text = "ZZZ Appended Type";
        tryVerify(() => addButton.enabled);
        if (data.viaButton) {
            mouseClick(addButton);
        } else {
            keyClick(Qt.Key_Return);
        }

        tryCompare(list, "count", before + 1);
        compare(field.text, "");
        tryVerify(() => field.activeFocus);
        compare(helper.rowPart(list, before, "commentTypeLabel").text, "ZZZ Appended Type");
        tryVerify(() => {
            const row = list.itemAtIndex(before);
            return row !== null && helper.verticallyInside(row, list);
        }, 5000, "the new row should be revealed");
    }

    function test_deleteRemovesTheClickedRow(): void {
        const dialog = helper.makeDialog();
        const expected = helper.dialogDraft(dialog);

        helper.deleteRow(dialog, 3);

        expected.splice(3, 1);
        compare(helper.shownTypes(helper.listView(dialog)), expected);
    }

    function test_lastTypeCannotBeDeleted(): void {
        const dialog = helper.makeDialog();
        const list = helper.listView(dialog);
        while (list.count > 1) {
            dialog.viewModel.remove(0);
        }
        helper.waitForDropToSettle(list);
        const button = helper.rowPart(list, 0, "commentTypeDeleteButton");

        verify(!button.enabled);
        mouseClick(button);
        compare(list.count, 1);
    }

    function test_invalidInputCannotBeAdded(): void {
        const dialog = helper.makeDialog();
        const list = helper.listView(dialog);
        const field = helper.textField(dialog);
        const addButton = helper.addButton(dialog);
        const error = helper.validationLabel(dialog);
        const before = list.count;
        compare(field.Accessible.name, "Add comment type");
        verify(!addButton.enabled, "an empty field cannot be added");
        compare(error.text, "");

        field.forceActiveFocus();
        field.text = "Sign [placement]";
        tryVerify(() => error.text !== "");
        verify(!addButton.enabled);
        verify(dialog.standardButton(Dialog.Ok).enabled);
        keyClick(Qt.Key_Return);
        compare(list.count, before);
    }

    function test_unsubmittedInputIsNotAddedOnOk(): void {
        const dialog = helper.makeDialog();
        const saved = helper.settings.commentTypes();
        helper.textField(dialog).text = "ZZZ Never Submitted";
        tryVerify(() => helper.addButton(dialog).enabled);

        helper.closeWith(dialog, Dialog.Ok);

        compare(helper.settings.commentTypes(), saved);
    }

    function test_cancelAndEscapeDiscardTheDraft_data(): var {
        return [
            {
                tag: "cancel",
                action: Dialog.Cancel
            },
            {
                tag: "escape",
                action: Dialog.NoButton
            }
        ];
    }

    function test_cancelAndEscapeDiscardTheDraft(data): void {
        const saved = helper.settings.commentTypes();
        const dialog = helper.makeDialog();
        helper.deleteRow(dialog, 0);
        helper.addType(dialog, "ZZZ Discarded Type");
        helper.dragAndDrop(helper.listView(dialog), 0, 3);

        helper.closeWith(dialog, data.action);

        compare(helper.settings.commentTypes(), saved);
        compare(helper.shownTypes(helper.listView(helper.makeDialog())), saved);
    }

    function test_restoreDefaultsResetsTheDraft(): void {
        const defaults = helper.settings.commentTypes();
        const dialog = helper.makeDialog();
        helper.deleteRow(dialog, 0);
        helper.addType(dialog, "ZZZ Custom Type");

        mouseClick(dialog.standardButton(Dialog.RestoreDefaults));

        tryCompare(helper.listView(dialog), "count", defaults.length);
        compare(helper.shownTypes(helper.listView(dialog)), defaults);
    }
}
