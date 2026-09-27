// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    name: "MpvqcCommentTypesListViewport"
    width: 600
    height: 900
    visible: true
    when: windowShown

    readonly property TestHelpers helper: TestHelpers {
        testCase: testCase
    }

    function init(): void {
        failOnWarning(/.*(TypeError|Unable to assign|Binding loop).*/);
    }

    function test_dropInPlaceKeepsOrderAndViewport_data(): var {
        return [
            {
                tag: "press-and-release",
                rows: 0
            },
            {
                tag: "there-and-back",
                rows: 2
            }
        ];
    }

    function test_dropInPlaceKeepsOrderAndViewport(data): void {
        const list = helper.makeList(false, 13);
        list.contentY = list.originY + 3 * MpvqcConstants.listRowHeight;
        verify(waitForRendering(list));
        const draft = helper.draftTypes(list);
        const scroll = helper.scrollPosition(list);
        const index = list.indexAt(list.width / 2, list.contentY + list.height / 2);
        const row = list.itemAtIndex(index);
        const start = helper.pressHandle(list, index);
        const away = start.y + data.rows * MpvqcConstants.listRowHeight;
        helper.movePointer(list, start.x, start.y, away);
        helper.movePointer(list, start.x, away, start.y);
        helper.drop(list, start);

        compare(helper.draftTypes(list), draft);
        compare(helper.scrollPosition(list), scroll);
        verify(list.itemAtIndex(index) === row, "the row must keep its identity");
    }

    function test_partlyVisibleRowStaysUnderThePointer_data(): var {
        return helper.mirroringData();
    }

    function test_partlyVisibleRowStaysUnderThePointer(data): void {
        const list = helper.makeList(data.mirrored, 13);
        const index = 3;
        list.contentY = list.originY + (index + 0.6) * MpvqcConstants.listRowHeight;
        const handle = helper.rowPart(list, index, "commentTypeDragHandle");
        tryVerify(() => handle.mapToItem(list, 0, 0).y < 0);
        const grab = Qt.point(handle.width / 2, handle.height * 0.8);
        const pointer = handle.mapToItem(list, grab.x, grab.y);
        verify(pointer.y > 0, "the grab point should be visible");
        const draft = helper.draftTypes(list);

        mousePress(list, pointer.x, pointer.y);
        mouseMove(list, pointer.x, pointer.y + 4, -1, Qt.LeftButton);
        verify(helper.liftedRow(list) === null, "the row lifts only past the drag threshold");
        for (const dy of [12, 24, 40, 60]) {
            mouseMove(list, pointer.x, pointer.y + dy, -1, Qt.LeftButton);
            const rendered = helper.liftedPart(list, "commentTypeDragHandle").mapToItem(list, grab.x, grab.y);
            verify(Math.abs(rendered.x - pointer.x) <= 0.5, "the grab point x must follow the pointer");
            verify(Math.abs(rendered.y - (pointer.y + dy)) <= 0.5, "the grab point y must follow the pointer");
        }
        helper.drop(list, Qt.point(pointer.x, pointer.y + 60));

        compare(helper.draftTypes(list), helper.moved(draft, index, index + 1));
    }
}
