// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

QtObject {
    id: root

    required property TestCase testCase

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}
    readonly property MpvqcTestSettings settings: MpvqcTestSettings {}

    readonly property color hoverColor: Qt.alpha(MpvqcAppearance.palette.foreground, MpvqcAppearance.isDark ? 0.08 : 0.12)

    readonly property FrameAnimation _frames: FrameAnimation {}

    readonly property Component _dialogComponent: Component {
        MpvqcCommentTypesDialog {
            enter: null
            exit: null
        }
    }

    readonly property Component _listComponent: Component {
        MpvqcCommentTypesListView {
            id: list

            readonly property ListModel draft: ListModel {}

            width: MpvqcConstants.smallDialogContentWidth
            height: 7 * MpvqcConstants.listRowHeight
            commentTypes: draft
            applyMove: (from, to) => list.draft.move(from, to, 1)
        }
    }

    function mirroringData(): var {
        return [
            {
                tag: "ltr",
                mirrored: false
            },
            {
                tag: "rtl",
                mirrored: true
            }
        ];
    }

    function makeDialog(mirrored = false): MpvqcCommentTypesDialog {
        const dialog = testCase.createTemporaryObject(_dialogComponent, testCase);
        testCase.verify(dialog, "dialog not created");
        dialog.contentItem.LayoutMirroring.enabled = mirrored;
        dialog.contentItem.LayoutMirroring.childrenInherit = true;
        dialog.open();
        testCase.tryVerify(() => dialog.opened);
        testCase.verify(testCase.waitForPolish(dialog.contentItem.Window.window));
        return dialog;
    }

    function makeList(mirrored = false, count = 7): var {
        const list = testCase.createTemporaryObject(_listComponent, testCase);
        testCase.verify(list, "list not created");
        list.LayoutMirroring.enabled = mirrored;
        list.LayoutMirroring.childrenInherit = true;
        for (let i = 0; i < count; i++) {
            list.draft.append({
                display: `Type ${i}`
            });
        }
        testCase.verify(testCase.waitForRendering(list));
        return list;
    }

    function find(parent: QtObject, name: string): var {
        const item = testCase.findChild(parent, name);
        testCase.verify(item, `${name} not found`);
        return item;
    }

    function listView(dialog: Dialog): MpvqcCommentTypesListView {
        return find(dialog.contentItem, "commentTypesListView");
    }

    function textField(dialog: Dialog): var {
        return find(dialog.contentItem, "commentTypeTextField");
    }

    function addButton(dialog: Dialog): var {
        return find(dialog.contentItem, "commentTypeAddButton");
    }

    function validationLabel(dialog: Dialog): var {
        return find(dialog.contentItem, "commentTypeValidationLabel");
    }

    function rowPart(list: ListView, index: int, name: string): var {
        testCase.tryVerify(() => list.itemAtIndex(index) !== null, 5000, `row ${index} not created`);
        const row = list.itemAtIndex(index);
        return row.objectName === name ? row : find(row, name);
    }

    function liftedRow(list: ListView): var {
        return list.children.find(child => child.objectName === "commentTypeRow") ?? null;
    }

    function liftedPart(list: ListView, name: string): var {
        const row = liftedRow(list);
        testCase.verify(row, "no row is lifted");
        return find(row, name);
    }

    function verifyGrabbedAt(list: ListView, grab: point, pointer: point): void {
        const rendered = liftedPart(list, "commentTypeDragHandle").mapToItem(list, grab.x, grab.y);
        testCase.verify(Math.abs(rendered.x - pointer.x) <= 0.5, "the grab point x must follow the pointer");
        testCase.verify(Math.abs(rendered.y - pointer.y) <= 0.5, "the grab point y must follow the pointer");
    }

    function shownTypes(list: ListView): var {
        const types = [];
        for (let i = 0; i < list.count; i++) {
            types.push(rowPart(list, i, "commentTypeLabel").text);
        }
        return types;
    }

    function shownIndexOf(list: ListView, type: string): int {
        return shownTypes(list).indexOf(type);
    }

    function draftTypes(list): var {
        return Array.from({
            length: list.draft.count
        }, (_, i) => list.draft.get(i).display);
    }

    function dialogDraft(dialog: MpvqcCommentTypesDialog): var {
        const model = dialog.viewModel.commentTypesModel;
        return Array.from({
            length: model.rowCount()
        }, (_, i) => model.data(model.index(i, 0)));
    }

    function moved(types: var, from: int, to: int): var {
        const copy = Array.from(types);
        copy.splice(to, 0, copy.splice(from, 1)[0]);
        return copy;
    }

    function verticallyInside(item: Item, viewport: Item): bool {
        const top = item.mapToItem(viewport, 0, 0).y;
        return top >= -0.5 && top + item.height <= viewport.height + 0.5;
    }

    function scrollPosition(list: ListView): real {
        return list.contentY - list.originY;
    }

    function maximumScrollPosition(list: ListView): real {
        return Math.max(0, list.contentHeight - list.height);
    }

    function slotTop(list: ListView, index: int): real {
        return index * MpvqcConstants.listRowHeight - scrollPosition(list);
    }

    function renderedTop(list: ListView, index: int): real {
        return rowPart(list, index, "commentTypeRowBackground").mapToItem(list, 0, 0).y;
    }

    function waitForFrames(count: int): void {
        _frames.reset();
        _frames.start();
        testCase.tryVerify(() => _frames.currentFrame >= count, 5000, `${count} frames should render`);
        _frames.stop();
    }

    function verifyScrollHoldsStill(list: ListView): void {
        const scroll = scrollPosition(list);
        waitForFrames(10);
        testCase.verify(Math.abs(scrollPosition(list) - scroll) < 1, `the list should hold still at ${scroll}, not ${scrollPosition(list)}`);
    }

    function holdNearEdge(list: ListView, from: int, down: bool): point {
        const start = pressHandle(list, from);
        const pointer = Qt.point(start.x, down ? list.height - 8 : 8);
        movePointer(list, start.x, start.y, pointer.y);
        return pointer;
    }

    function waitForScrollPast(list: ListView, rows: real, down = true): void {
        const start = scrollPosition(list);
        const distance = rows * MpvqcConstants.listRowHeight;
        testCase.tryVerify(() => down ? scrollPosition(list) >= start + distance : scrollPosition(list) <= start - distance, 5000, `the list should scroll ${rows} rows`);
    }

    function waitForScrollBound(list: ListView, down: bool): void {
        const bound = down ? maximumScrollPosition(list) : 0;
        testCase.tryVerify(() => Math.abs(scrollPosition(list) - bound) <= 0.5, 5000, "holding near the edge should scroll to the bound");
    }

    function dragPastEdge(list: ListView, from: int, down: bool): void {
        const pointer = holdNearEdge(list, from, down);
        waitForScrollBound(list, down);
        drop(list, pointer);
    }

    function waitForShownTypes(list: ListView, expected: var): void {
        testCase.tryVerify(() => JSON.stringify(shownTypes(list)) === JSON.stringify(expected), 5000, "preview order should match");
    }

    function waitForTypesInView(list: ListView, expected: var): void {
        const rowHeight = MpvqcConstants.listRowHeight;
        testCase.tryVerify(() => {
            const first = Math.floor(scrollPosition(list) / rowHeight);
            const last = Math.min(list.count - 1, Math.floor((scrollPosition(list) + list.height - 1) / rowHeight));
            for (let i = first; i <= last; i++) {
                if (rowPart(list, i, "commentTypeLabel").text !== expected[i]) {
                    return false;
                }
            }
            return true;
        }, 5000, "the rows in view should match");
    }

    function waitForDropToSettle(list: ListView): void {
        testCase.tryVerify(() => !list.reordering, 5000, "the lifted row should settle");
        testCase.tryVerify(() => {
            const rows = list.contentItem.children.filter(child => child.objectName === "commentTypeDelegate" && child.visible);
            if (rows.length === 0 || rows.some(row => row.opacity !== 1 || row.index < 0)) {
                return false;
            }
            for (let i = 0; i < list.count; i++) {
                if (list.itemAtIndex(i) && Math.abs(renderedTop(list, i) - slotTop(list, i)) > 0.5) {
                    return false;
                }
            }
            return true;
        }, 5000, "every row should rest in its slot");
    }

    function pressHandle(list: ListView, index: int): point {
        const handle = rowPart(list, index, "commentTypeDragHandle");
        const point = handle.mapToItem(list, handle.width / 2, handle.height / 2);
        testCase.mousePress(list, point.x, point.y);
        return point;
    }

    function movePointer(list: ListView, x: real, fromY: real, toY: real): void {
        const steps = Math.max(2, Math.ceil(Math.abs(toY - fromY) / 8));
        for (let i = 1; i <= steps; i++) {
            testCase.mouseMove(list, x, fromY + (toY - fromY) * i / steps, -1, Qt.LeftButton);
        }
    }

    function dragPointer(list: ListView, from: int, rows: real): point {
        const start = pressHandle(list, from);
        const endY = start.y + rows * MpvqcConstants.listRowHeight;
        movePointer(list, start.x, start.y, endY);
        return Qt.point(start.x, endY);
    }

    function drop(list: ListView, at: point): void {
        testCase.mouseRelease(list, at.x, at.y);
        waitForDropToSettle(list);
    }

    function dragAndDrop(list: ListView, from: int, to: int): void {
        drop(list, dragPointer(list, from, to - from));
    }

    function addType(dialog: Dialog, text: string): void {
        const field = textField(dialog);
        const list = listView(dialog);
        const before = list.count;
        field.forceActiveFocus();
        field.text = text;
        testCase.keyClick(Qt.Key_Return);
        testCase.tryCompare(list, "count", before + 1);
        testCase.verify(testCase.waitForPolish(dialog.contentItem.Window.window));
    }

    function addTypes(dialog: Dialog, count: int): void {
        for (let i = 1; i <= count; i++) {
            addType(dialog, `ZZZ Long List ${i}`);
        }
    }

    function deleteRow(dialog: Dialog, index: int): void {
        const list = listView(dialog);
        const before = list.count;
        list.positionViewAtIndex(index, ListView.Contain);
        waitForDropToSettle(list);
        testCase.mouseClick(rowPart(list, index, "commentTypeDeleteButton"));
        testCase.tryCompare(list, "count", before - 1);
        waitForDropToSettle(list);
    }

    function closeWith(dialog: Dialog, action: int): void {
        if (action === Dialog.NoButton) {
            testCase.keyClick(Qt.Key_Escape);
        } else {
            testCase.mouseClick(dialog.standardButton(action));
        }
        testCase.tryVerify(() => !dialog.visible);
        bridge.waitForBackgroundJobs();
    }
}
