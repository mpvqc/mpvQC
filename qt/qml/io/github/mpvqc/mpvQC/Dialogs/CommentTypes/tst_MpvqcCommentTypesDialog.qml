// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

import io.github.mpvqc.mpvQC.Python

TestCase {
    id: testCase

    width: 500
    height: 600
    visible: true
    when: windowShown
    name: "MpvqcCommentTypesDialog"

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}

    readonly property Component _dialogComponent: Component {
        MpvqcCommentTypesDialog {}
    }

    function makeDialog(): Dialog {
        const dialog = createTemporaryObject(_dialogComponent, testCase);
        verify(dialog, "dialog not created");
        dialog.open();
        tryVerify(() => dialog.opened);
        waitForRendering(dialog.contentItem);
        return dialog;
    }

    function test_emptyDraftDisablesAdd(): void {
        const dialog = makeDialog();
        const field = findChild(dialog.contentItem, "commentTypeTextField");
        const addButton = findChild(dialog.contentItem, "commentTypeAddButton");

        compare(field.text, "");
        verify(!addButton.enabled);
    }

    function test_duplicateDraftDisablesAddAndShowsError(): void {
        const dialog = makeDialog();
        const field = findChild(dialog.contentItem, "commentTypeTextField");
        const addButton = findChild(dialog.contentItem, "commentTypeAddButton");
        const error = findChild(dialog.contentItem, "commentTypeValidationLabel");

        field.text = "ZZZ Unique Type";
        tryVerify(() => addButton.enabled);
        mouseClick(addButton);

        field.text = "ZZZ Unique Type";
        tryVerify(() => !addButton.enabled);
        verify(error.text !== "");
    }

    function test_addAppendsSelectsAndClears(): void {
        const dialog = makeDialog();
        const field = findChild(dialog.contentItem, "commentTypeTextField");
        const addButton = findChild(dialog.contentItem, "commentTypeAddButton");
        const listView = findChild(dialog.contentItem, "commentTypesListView");

        const before = listView.count;
        field.text = "ZZZ Appended Type";
        tryVerify(() => addButton.enabled);
        mouseClick(addButton);

        tryCompare(listView, "count", before + 1);
        compare(listView.currentIndex, listView.count - 1);
        compare(field.text, "");
    }

    function test_deleteRemovesSelectedRow(): void {
        const dialog = makeDialog();
        const listView = findChild(dialog.contentItem, "commentTypesListView");
        const deleteButton = findChild(dialog.contentItem, "commentTypeDeleteButton");

        const before = listView.count;
        verify(before > 1);
        listView.currentIndex = 0;
        tryVerify(() => deleteButton.enabled);
        mouseClick(deleteButton);

        tryCompare(listView, "count", before - 1);
    }

    function test_okStaysEnabledWithInvalidDraft(): void {
        const dialog = makeDialog();
        const field = findChild(dialog.contentItem, "commentTypeTextField");
        const addButton = findChild(dialog.contentItem, "commentTypeAddButton");
        const okButton = dialog.standardButton(Dialog.Ok);

        verify(okButton.enabled);

        field.text = "ZZZ Duplicated Type";
        tryVerify(() => addButton.enabled);
        mouseClick(addButton);

        field.text = "ZZZ Duplicated Type";
        tryVerify(() => !addButton.enabled);
        verify(okButton.enabled);
    }

    function test_reorderKeepsSelection(): void {
        const dialog = makeDialog();
        const listView = findChild(dialog.contentItem, "commentTypesListView");
        const moveUp = findChild(dialog.contentItem, "commentTypeMoveUpButton");
        const moveDown = findChild(dialog.contentItem, "commentTypeMoveDownButton");

        verify(listView.count > 1);
        listView.currentIndex = 0;

        tryVerify(() => moveDown.enabled);
        mouseClick(moveDown);
        tryCompare(listView, "currentIndex", 1);

        tryVerify(() => moveUp.enabled);
        mouseClick(moveUp);
        tryCompare(listView, "currentIndex", 0);
    }
}
