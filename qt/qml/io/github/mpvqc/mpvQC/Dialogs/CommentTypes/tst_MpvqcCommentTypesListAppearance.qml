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

    name: "MpvqcCommentTypesListAppearance"
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

    function test_liftedRowMatchesAnOrdinaryRow(): void {
        const list = helper.makeList();
        const end = helper.dragPointer(list, 2, 1.5);
        const lifted = helper.liftedRow(list);
        verify(lifted);
        const row = helper.rowPart(list, 0, "commentTypeRow");

        for (const name of ["commentTypeDragHandle", "commentTypeLabel", "commentTypeDeleteButton"]) {
            const ordinary = helper.rowPart(list, 0, name).mapToItem(row, 0, 0);
            const liftedPoint = helper.liftedPart(list, name).mapToItem(lifted, 0, 0);
            compare(liftedPoint.x, ordinary.x, `${name} x`);
            compare(liftedPoint.y, ordinary.y, `${name} y`);
        }
        verify(Qt.colorEqual(helper.liftedPart(list, "commentTypeRowBase").color, MpvqcAppearance.palette.sectionCard));
        verify(Qt.colorEqual(helper.liftedPart(list, "commentTypeRowBackground").color, helper.hoverColor));
        verify(helper.liftedPart(list, "commentTypeDeleteButton").enabled, "the lifted delete icon keeps its colour");

        helper.drop(list, end);
    }

    function test_longListsLeaveAGutterForTheScrollBar_data(): var {
        return helper.mirroringData();
    }

    function test_longListsLeaveAGutterForTheScrollBar(data): void {
        const list = helper.makeList(data.mirrored);
        const scrollBar = list.ScrollBar.vertical;
        verify(!scrollBar.visible, "seven rows need no scroll bar");
        for (let i = 0; i < 3; i++) {
            list.draft.append({
                display: `Extra ${i}`
            });
        }
        tryVerify(() => scrollBar.visible);

        const row = helper.rowPart(list, 0, "commentTypeRow");
        const body = helper.rowPart(list, 0, "commentTypeRowBackground");
        compare(body.width, row.width - 20);
        compare(body.mapToItem(row, 0, 0).x, data.mirrored ? 20 : 0);
    }
}
