// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    name: "MpvqcCommentTypesRow"
    width: 600
    height: 200
    visible: true
    when: windowShown

    readonly property TestHelpers helper: TestHelpers {
        testCase: testCase
    }

    readonly property Component _rowComponent: Component {
        MpvqcCommentTypesRow {
            width: MpvqcConstants.smallDialogContentWidth
            height: implicitHeight
            commentType: "Type"
            gutter: 0
        }
    }

    function init(): void {
        failOnWarning(/.*(TypeError|Unable to assign|Binding loop).*/);
        mouseMove(testCase, width - 1, height - 1);
    }

    function makeRow(properties = {}): MpvqcCommentTypesRow {
        const row = createTemporaryObject(_rowComponent, testCase, properties);
        verify(row);
        verify(waitForRendering(row));
        return row;
    }

    function test_deleteButtonHasEqualInsets_data(): var {
        return helper.mirroringData();
    }

    function test_deleteButtonHasEqualInsets(data): void {
        const row = makeRow();
        row.LayoutMirroring.enabled = data.mirrored;
        row.LayoutMirroring.childrenInherit = true;
        verify(waitForPolish(row.Window.window));
        const button = helper.find(row, "commentTypeDeleteButton");
        const label = helper.find(row, "commentTypeLabel");
        const topLeft = button.mapToItem(row, 0, 0);

        compare(topLeft.y, 4);
        compare(row.height - topLeft.y - button.height, 4);
        compare(data.mirrored ? topLeft.x : row.width - topLeft.x - button.width, 4);
        compare(label.effectiveHorizontalAlignment, data.mirrored ? Text.AlignRight : Text.AlignLeft);
    }

    function test_longLabelsElideBeforeTheDeleteButton(): void {
        const row = makeRow({
            commentType: "ZZZ A comment type with a label much too long to fit the row of this narrow dialog"
        });
        const label = helper.find(row, "commentTypeLabel");
        const button = helper.find(row, "commentTypeDeleteButton");

        verify(label.truncated);
        verify(label.mapToItem(row, label.width, 0).x <= button.mapToItem(row, 0, 0).x);
    }

    function test_hoverTintsTheRowButKeepsTextAndIconColours(): void {
        const row = makeRow();
        const background = helper.find(row, "commentTypeRowBackground");
        const label = helper.find(row, "commentTypeLabel");
        const button = helper.find(row, "commentTypeDeleteButton");
        verify(Qt.colorEqual(background.color, "transparent"));

        mouseMove(label, label.width / 2, label.height / 2);
        tryVerify(() => Qt.colorEqual(background.color, helper.hoverColor));
        verify(Qt.colorEqual(label.color, MpvqcAppearance.palette.foreground));
        verify(Qt.colorEqual(button.contentItem.defaultIconColor, MpvqcAppearance.palette.error));

        mouseMove(button, button.width / 2, button.height / 2);
        verify(Qt.colorEqual(background.color, helper.hoverColor));
        verify(Qt.colorEqual(label.color, MpvqcAppearance.palette.foreground));
        verify(Qt.colorEqual(button.contentItem.defaultIconColor, MpvqcAppearance.palette.error));
    }
}
