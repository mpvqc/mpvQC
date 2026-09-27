// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    name: "MpvqcCommentTypesListView"
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

    function test_dragReorders_data(): var {
        return [
            {
                tag: "down",
                from: 1,
                rows: 3,
                to: 4,
                mirrored: false
            },
            {
                tag: "up",
                from: 5,
                rows: -3,
                to: 2,
                mirrored: false
            },
            {
                tag: "to-first",
                from: 3,
                rows: -3,
                to: 0,
                mirrored: false
            },
            {
                tag: "to-last",
                from: 2,
                rows: 4,
                to: 6,
                mirrored: false
            },
            {
                tag: "mirrored",
                from: 1,
                rows: 3,
                to: 4,
                mirrored: true
            }
        ];
    }

    function test_dragReorders(data): void {
        const list = helper.makeList(data.mirrored);
        const draft = helper.draftTypes(list);
        const expected = helper.moved(draft, data.from, data.to);
        const end = helper.dragPointer(list, data.from, data.rows);

        compare(helper.liftedPart(list, "commentTypeLabel").text, draft[data.from]);
        const indicator = helper.find(list, "commentTypesDropIndicator");
        tryVerify(() => Math.abs(indicator.mapToItem(list, 0, 0).y - helper.slotTop(list, data.to)) <= 0.5);
        helper.waitForShownTypes(list, expected);
        for (let i = 0; i < expected.length; i++) {
            if (i !== data.to) {
                tryVerify(() => Math.abs(helper.renderedTop(list, i) - helper.slotTop(list, i)) <= 0.5, 5000, `row ${i} should rest in its preview slot`);
            }
        }
        compare(helper.draftTypes(list), draft, "previewing must not reorder the draft");

        mouseRelease(list, end.x, end.y);
        compare(helper.draftTypes(list), expected, "release must commit before settling");
        helper.waitForDropToSettle(list);
        compare(helper.draftTypes(list), expected, "settling must not apply a second move");
        compare(helper.rowPart(list, data.to, "commentTypeLabel").text, draft[data.from]);
    }

    function test_cancelledDragKeepsOrder(): void {
        const list = helper.makeList();
        const draft = helper.draftTypes(list);
        const end = helper.dragPointer(list, 1, 3);
        helper.waitForShownTypes(list, helper.moved(draft, 1, 4));

        helper.bridge.deactivateWindow(list.Window.window);

        helper.waitForDropToSettle(list);
        helper.waitForShownTypes(list, draft);
        verify(!helper.find(list, "commentTypesDropIndicator").visible);
        mouseRelease(list, end.x, end.y);
        compare(helper.draftTypes(list), draft);
    }

    function test_cancellingSettleKeepsAcceptedMove(): void {
        const list = helper.makeList();
        const expected = helper.moved(helper.draftTypes(list), 1, 4);
        const end = helper.dragPointer(list, 1, 3);
        mouseRelease(list, end.x, end.y);
        verify(list.reordering);

        list.cancelReorder();
        list.cancelReorder();

        helper.waitForDropToSettle(list);
        compare(helper.draftTypes(list), expected);
        helper.waitForShownTypes(list, expected);
        helper.dragAndDrop(list, 2, 5);
        compare(helper.draftTypes(list), helper.moved(expected, 2, 5));
    }
}
