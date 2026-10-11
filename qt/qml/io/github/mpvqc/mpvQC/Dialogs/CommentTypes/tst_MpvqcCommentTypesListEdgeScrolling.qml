// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    name: "MpvqcCommentTypesListEdgeScrolling"
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

    function test_holdingNearAnEdgeReachesTheEnd_data(): var {
        return [
            {
                tag: "down",
                down: true,
                overshoot: false,
                mirrored: false
            },
            {
                tag: "up",
                down: false,
                overshoot: false,
                mirrored: false
            },
            {
                tag: "past-the-bottom",
                down: true,
                overshoot: true,
                mirrored: false
            },
            {
                tag: "past-the-top",
                down: false,
                overshoot: true,
                mirrored: false
            },
            {
                tag: "down-mirrored",
                down: true,
                overshoot: false,
                mirrored: true
            }
        ];
    }

    function test_holdingNearAnEdgeReachesTheEnd(data): void {
        const list = helper.makeList(data.mirrored, 20);
        list.y = 100;
        if (!data.down) {
            list.positionViewAtEnd();
        }
        verify(waitForRendering(list));
        const last = data.down ? list.count - 1 : 0;
        const from = list.indexAt(list.width / 2, list.contentY + list.height / 2);
        const draft = helper.draftTypes(list);
        const start = helper.pressHandle(list, from);
        const grab = helper.rowPart(list, from, "commentTypeDragHandle").mapFromItem(list, start.x, start.y);
        const inset = data.overshoot ? -40 : 8;
        const pointer = Qt.point(start.x, data.down ? list.height - inset : inset);
        helper.movePointer(list, start.x, start.y, pointer.y);

        helper.waitForScrollPast(list, 3, data.down);
        helper.verifyGrabbedAt(list, grab, pointer);
        tryVerify(() => Math.abs(helper.shownIndexOf(list, draft[from]) - from) >= 3, 5000, "the gap should follow the scroll while the pointer holds still");
        const indicator = helper.find(list, "commentTypesDropIndicator");
        const gapTop = indicator.mapToItem(list, 0, 0).y;
        verify(gapTop > -MpvqcConstants.listRowHeight && gapTop < list.height, `the gap should stay in view, not at ${gapTop}`);

        helper.waitForScrollBound(list, data.down);
        helper.verifyGrabbedAt(list, grab, pointer);
        tryVerify(() => helper.bridge.nearlyEqual(indicator.mapToItem(list, 0, 0).y, helper.slotTop(list, last)), 5000, "the gap should mark the end");
        helper.waitForShownTypes(list, helper.moved(draft, from, last));

        helper.drop(list, pointer);

        compare(helper.draftTypes(list), helper.moved(draft, from, last));
        verify(data.down ? helper.bridge.atScrollEnd(list) : helper.bridge.atScrollStart(list), "the drop should keep the list at the bound");
    }

    function test_pressNearAnEdgeKeepsTheListStill_data(): var {
        return [
            {
                tag: "bottom",
                down: true
            },
            {
                tag: "top",
                down: false
            }
        ];
    }

    function test_pressNearAnEdgeKeepsTheListStill(data): void {
        const list = helper.makeList(false, 20);
        if (!data.down) {
            list.positionViewAtEnd();
            verify(waitForRendering(list));
        }
        const draft = helper.draftTypes(list);
        const atOpeningEdge = () => data.down ? helper.bridge.atScrollStart(list) : helper.bridge.atScrollEnd(list);
        verify(atOpeningEdge(), "the list should open at the edge away from the press");
        const from = list.indexAt(list.width / 2, list.contentY + (data.down ? list.height - 1 : 1));
        const start = helper.pressHandle(list, from);
        verify(data.down ? start.y > list.height - 48 : start.y < 48, "the handle should sit in the edge zone");
        const nudge = Application.styleHints.startDragDistance - 1;
        mouseMove(list, start.x, start.y + (data.down ? nudge : -nudge), -1, Qt.LeftButton);

        helper.verifyScrollHoldsStill(list);

        verify(helper.liftedRow(list) === null, "the row lifts only past the drag threshold");
        verify(atOpeningEdge(), "a press must not scroll the list");
        mouseRelease(list, start.x, start.y);
        helper.verifyScrollHoldsStill(list);
        verify(atOpeningEdge(), "a release must not scroll the list");
        compare(helper.draftTypes(list), draft);
    }

    function test_leavingTheEdgeZoneStopsScrolling_data(): var {
        return [
            {
                tag: "bottom",
                down: true
            },
            {
                tag: "top",
                down: false
            }
        ];
    }

    function test_leavingTheEdgeZoneStopsScrolling(data): void {
        const list = helper.makeList(false, 20);
        if (!data.down) {
            list.positionViewAtEnd();
            verify(waitForRendering(list));
        }
        const from = data.down ? 3 : list.count - 4;
        const draft = helper.draftTypes(list);
        const edge = helper.holdNearEdge(list, from, data.down);
        helper.waitForScrollPast(list, 2, data.down);

        const pointer = Qt.point(edge.x, list.height / 2);
        helper.movePointer(list, edge.x, edge.y, pointer.y);

        helper.verifyScrollHoldsStill(list);
        verify(helper.liftedRow(list) !== null, "the row should still be lifted");
        const scroll = helper.scrollPosition(list);
        helper.drop(list, pointer);
        const to = list.indexAt(pointer.x, list.contentY + pointer.y);
        compare(helper.rowPart(list, to, "commentTypeLabel").text, draft[from], "the row should settle under the pointer");
        compare(helper.draftTypes(list), helper.moved(draft, from, to));
        verify(helper.bridge.nearlyEqual(helper.scrollPosition(list), scroll), `the drop should keep the list at ${scroll}, not ${helper.scrollPosition(list)}`);
    }

    function test_shortListDoesNotScroll_data(): var {
        return [
            {
                tag: "five-down",
                count: 5,
                down: true
            },
            {
                tag: "seven-down",
                count: 7,
                down: true
            },
            {
                tag: "seven-up",
                count: 7,
                down: false
            }
        ];
    }

    function test_shortListDoesNotScroll(data): void {
        const list = helper.makeList(false, data.count);
        const draft = helper.draftTypes(list);
        const from = data.down ? 1 : data.count - 2;
        const pointer = helper.holdNearEdge(list, from, data.down);

        helper.verifyScrollHoldsStill(list);

        verify(helper.bridge.atScrollStart(list), "a short list must not scroll");
        helper.drop(list, pointer);
        compare(helper.draftTypes(list), helper.moved(draft, from, data.down ? data.count - 1 : 0));
        verify(helper.bridge.atScrollStart(list), "the drop must not scroll a short list");
    }

    function test_cancellingStopsScrolling_data(): var {
        return [
            {
                tag: "down",
                down: true
            },
            {
                tag: "up",
                down: false
            }
        ];
    }

    function test_cancellingStopsScrolling(data): void {
        const list = helper.makeList(false, 20);
        if (!data.down) {
            list.positionViewAtEnd();
            verify(waitForRendering(list));
        }
        const draft = helper.draftTypes(list);
        const pointer = helper.holdNearEdge(list, data.down ? 3 : list.count - 4, data.down);
        helper.waitForScrollPast(list, 2, data.down);

        helper.bridge.deactivateWindow(list.Window.window);
        helper.waitForDropToSettle(list);

        helper.verifyScrollHoldsStill(list);
        helper.waitForTypesInView(list, draft);
        mouseRelease(list, pointer.x, pointer.y);
        compare(helper.draftTypes(list), draft);
    }

    function test_wheelScrollsAfterAnEdgeScrolledDrop(): void {
        const list = helper.makeList(false, 20);
        helper.dragPastEdge(list, 3, true);

        mouseWheel(list, list.width / 2, list.height / 2, 0, 120);

        tryVerify(() => !helper.bridge.atScrollEnd(list), 5000, "the wheel should scroll the list again");
    }
}
