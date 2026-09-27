// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    name: "MpvqcCommentTypesDialogEdgeScrolling"
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

    function test_movingToTheEndAndBackIsSavedOnOk(): void {
        const dialog = helper.makeDialog();
        helper.addTypes(dialog, 8);
        const list = helper.listView(dialog);
        const initial = helper.dialogDraft(dialog);
        const last = initial.length - 1;
        list.positionViewAtBeginning();

        helper.dragPastEdge(list, 0, true);
        helper.closeWith(dialog, Dialog.Ok);

        compare(helper.settings.commentTypes(), helper.moved(initial, 0, last));

        const reopened = helper.makeDialog();
        const reopenedList = helper.listView(reopened);
        reopenedList.positionViewAtEnd();
        helper.dragPastEdge(reopenedList, last, false);
        helper.closeWith(reopened, Dialog.Ok);

        compare(helper.settings.commentTypes(), initial);
    }

    function test_movingAcrossTheViewportIsDiscarded_data(): var {
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

    function test_movingAcrossTheViewportIsDiscarded(data): void {
        const saved = helper.settings.commentTypes();
        const dialog = helper.makeDialog();
        helper.addTypes(dialog, 8);
        const list = helper.listView(dialog);
        list.positionViewAtBeginning();
        helper.dragPastEdge(list, 0, true);

        helper.closeWith(dialog, data.action);

        compare(helper.settings.commentTypes(), saved);
        compare(helper.shownTypes(helper.listView(helper.makeDialog())), saved);
    }

    function test_closingWhileEdgeScrollingStopsIt(): void {
        const saved = helper.settings.commentTypes();
        const dialog = helper.makeDialog();
        helper.addTypes(dialog, 8);
        const list = helper.listView(dialog);
        list.positionViewAtBeginning();
        const pointer = list.mapToItem(testCase, helper.holdNearEdge(list, 1, true));
        helper.waitForScrollPast(list, 2);

        keyClick(Qt.Key_Escape);
        tryVerify(() => !dialog.visible);
        helper.bridge.waitForBackgroundJobs();
        mouseRelease(testCase, pointer.x, pointer.y);

        verify(!list.reordering);
        verify(helper.liftedRow(list) === null);
        helper.verifyScrollHoldsStill(list);
        compare(helper.settings.commentTypes(), saved);
    }

    function test_edgeDragAfterListEdits_data(): var {
        return [
            {
                tag: "after-moves",
                edit: dialog => {
                    const list = helper.listView(dialog);
                    helper.dragAndDrop(list, 0, 3);
                    helper.dragPastEdge(list, 5, true);
                    list.positionViewAtBeginning();
                    helper.dragAndDrop(list, 6, 1);
                    return dialog;
                }
            },
            {
                tag: "after-deletions-while-scrolled",
                edit: dialog => {
                    const list = helper.listView(dialog);
                    list.positionViewAtEnd();
                    for (let i = 0; i < 2; i++) {
                        const first = list.indexAt(list.width / 2, list.contentY + 1);
                        mouseClick(helper.rowPart(list, first, "commentTypeDeleteButton"));
                        helper.waitForDropToSettle(list);
                    }
                    return dialog;
                }
            },
            {
                tag: "after-restore-defaults",
                edit: dialog => {
                    const list = helper.listView(dialog);
                    helper.dragPastEdge(list, 1, true);
                    mouseClick(dialog.standardButton(Dialog.RestoreDefaults));
                    helper.waitForDropToSettle(list);
                    helper.addTypes(dialog, 8);
                    return dialog;
                }
            },
            {
                tag: "after-reopening",
                edit: dialog => {
                    helper.dragPastEdge(helper.listView(dialog), 1, true);
                    helper.closeWith(dialog, Dialog.Ok);
                    return helper.makeDialog();
                }
            }
        ];
    }

    function test_edgeDragAfterListEdits(data): void {
        const original = helper.makeDialog();
        helper.addTypes(original, 8);
        helper.listView(original).positionViewAtBeginning();
        const dialog = data.edit(original);
        const list = helper.listView(dialog);
        const index = 2;
        list.contentY = list.originY + (index + 0.6) * MpvqcConstants.listRowHeight;
        const handle = helper.rowPart(list, index, "commentTypeDragHandle");
        tryVerify(() => handle.mapToItem(list, 0, 0).y < 0);
        const requestedPress = handle.mapToItem(null, handle.width / 2, handle.height * 0.8);
        const press = Qt.point(Math.round(requestedPress.x), Math.round(requestedPress.y));
        const grab = handle.mapFromItem(null, press);
        const pointer = list.mapFromItem(null, press);
        verify(pointer.y > 0, "the grab point should be visible");
        const draft = helper.dialogDraft(dialog);

        mousePress(list, pointer.x, pointer.y);
        mouseMove(list, pointer.x, pointer.y + 12, -1, Qt.LeftButton);
        helper.verifyGrabbedAt(list, grab, Qt.point(pointer.x, pointer.y + 12));
        const requestedEdge = list.mapToItem(null, pointer.x, list.height - 8);
        const edge = list.mapFromItem(null, Math.round(requestedEdge.x), Math.round(requestedEdge.y));
        helper.movePointer(list, pointer.x, pointer.y + 12, edge.y);
        helper.waitForScrollBound(list, true);
        helper.verifyGrabbedAt(list, grab, edge);
        helper.drop(list, edge);

        compare(helper.dialogDraft(dialog), helper.moved(draft, index, draft.length - 1));
    }
}
