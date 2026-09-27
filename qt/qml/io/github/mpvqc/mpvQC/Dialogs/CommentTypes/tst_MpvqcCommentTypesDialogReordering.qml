// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

TestCase {
    id: testCase

    name: "MpvqcCommentTypesDialogReordering"
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

    function test_draggingBlocksConflictingEdits_data(): var {
        return [
            {
                tag: "add",
                edit: (dialog, list) => keyClick(Qt.Key_Return)
            },
            {
                tag: "delete",
                edit: (dialog, list) => {
                    const deleteButton = helper.rowPart(list, 5, "commentTypeDeleteButton");
                    verify(deleteButton.enabled, "delete buttons stay enabled while dragging");
                    deleteButton.forceActiveFocus(Qt.TabFocusReason);
                    keyClick(Qt.Key_Space);
                }
            },
            {
                tag: "restore-defaults",
                edit: (dialog, list) => {
                    dialog.standardButton(Dialog.RestoreDefaults).forceActiveFocus(Qt.TabFocusReason);
                    keyClick(Qt.Key_Space);
                }
            }
        ];
    }

    function test_draggingBlocksConflictingEdits(data): void {
        const dialog = helper.makeDialog();
        const list = helper.listView(dialog);
        helper.deleteRow(dialog, 6);
        const saved = helper.dialogDraft(dialog);
        const field = helper.textField(dialog);
        field.forceActiveFocus();
        field.text = "ZZZ Blocked Type";
        tryVerify(() => helper.addButton(dialog).enabled);

        const end = helper.dragPointer(list, 0, 2);
        data.edit(dialog, list);
        compare(helper.dialogDraft(dialog), saved, "the edit must wait for the drop");

        mouseRelease(list, end.x, end.y);
        compare(helper.dialogDraft(dialog), helper.moved(saved, 0, 2), "release accepts the draft move");
        helper.waitForDropToSettle(list);
    }

    function test_closingDuringReorder_data(): var {
        // The pointer is grabbed mid-drag, so the dialog closes without a click.
        return [
            {
                tag: "escape-while-dragging",
                released: false,
                close: dialog => keyClick(Qt.Key_Escape)
            },
            {
                tag: "ok-while-settling",
                released: true,
                close: dialog => dialog.accept()
            }
        ];
    }

    function test_closingDuringReorder(data): void {
        const saved = helper.settings.commentTypes();
        const dialog = helper.makeDialog();
        const list = helper.listView(dialog);
        const reordered = helper.moved(saved, 1, 4);
        const end = list.mapToItem(testCase, helper.dragPointer(list, 1, 3));
        if (data.released) {
            mouseRelease(testCase, end.x, end.y);
            compare(helper.dialogDraft(dialog), reordered);
        }
        verify(list.reordering, "close must happen before the gesture settles");

        data.close(dialog);
        tryVerify(() => !dialog.visible);
        helper.bridge.waitForBackgroundJobs();
        if (!data.released) {
            mouseRelease(testCase, end.x, end.y);
        }
        const draft = data.released ? reordered : saved;
        compare(helper.settings.commentTypes(), draft);

        dialog.open();
        tryVerify(() => dialog.opened);
        verify(!list.reordering);
        verify(helper.liftedRow(list) === null);
        verify(!helper.find(list, "commentTypesDropIndicator").visible);
        helper.waitForShownTypes(list, draft);
        // A new gesture outlasts the old settle animation and exposes stale callbacks.
        helper.dragAndDrop(list, 3, 3);
        compare(helper.dialogDraft(dialog), draft);
    }

    function test_reorderingIsSavedOnOk(): void {
        const saved = helper.settings.commentTypes();
        const dialog = helper.makeDialog();
        const list = helper.listView(dialog);
        helper.dragAndDrop(list, 6, 0);
        const expected = helper.moved(saved, 6, 0);

        helper.closeWith(dialog, Dialog.Ok);

        compare(helper.settings.commentTypes(), expected);
        compare(helper.shownTypes(helper.listView(helper.makeDialog())), expected);
    }
}
